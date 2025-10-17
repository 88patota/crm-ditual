"""
Cliente HTTP para comunicação com o User Service
"""

import httpx
import os
from typing import Optional, Dict, Any
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class UserInfo(BaseModel):
    """Informações do usuário obtidas do User Service"""
    id: int
    email: str
    username: str
    full_name: str
    role: str
    is_active: bool


class UserClient:
    """Cliente para comunicação com o User Service"""
    
    def __init__(self):
        # URL do user service - usar variável de ambiente ou padrão
        self.user_service_url = os.getenv("USER_SERVICE_URL", "http://user_service:8000")
        self.timeout = 10.0
    
    async def get_user_by_username(self, username: str, auth_token: str) -> Optional[UserInfo]:
        """
        Obter informações do usuário pelo username
        
        Args:
            username: Nome do usuário
            auth_token: Token JWT para autenticação
            
        Returns:
            UserInfo ou None se não encontrado
        """
        try:
            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Primeiro, obter o perfil do usuário atual através do endpoint /me
                response = await client.get(
                    f"{self.user_service_url}/api/v1/users/me",
                    headers=headers
                )
                
                if response.status_code == 200:
                    user_data = response.json()
                    return UserInfo(**user_data)
                else:
                    logger.warning(f"Failed to get user info for {username}: {response.status_code}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error(f"Timeout when getting user info for {username}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Request error when getting user info for {username}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error when getting user info for {username}: {e}")
            return None
    
    async def health_check(self) -> bool:
        """
        Verificar se o User Service está disponível
        
        Returns:
            True se o serviço estiver disponível
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.user_service_url}/health")
                return response.status_code == 200
        except Exception:
            return False


# Instância global do cliente
user_client = UserClient()