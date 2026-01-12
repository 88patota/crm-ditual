#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
COMPOSE_FILE="${COMPOSE_FILE:-${ROOT_DIR}/docker-compose.prod.yml}"
ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env.prod}"
SSL_DIR="${SSL_DIR:-${ROOT_DIR}/nginx/ssl}"

DRY_RUN="0"
STOP_MODE="auto"

usage() {
  cat <<'EOF'
Uso:
  renew-letsencrypt-prod.sh [--dry-run] [--stop-nginx|--no-stop-nginx]

Variáveis opcionais:
  COMPOSE_FILE=/caminho/docker-compose.prod.yml
  ENV_FILE=/caminho/.env.prod
  SSL_DIR=/caminho/nginx/ssl
EOF
}

while [ "${#}" -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN="1" ;;
    --stop-nginx) STOP_MODE="stop" ;;
    --no-stop-nginx) STOP_MODE="no-stop" ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "Argumento inválido: $1" >&2
      usage
      exit 2
      ;;
  esac
  shift
done

if [ -f "$ENV_FILE" ]; then
  set -a
  . "$ENV_FILE"
  set +a
fi

CERTBOT=(certbot)
if [ "$(id -u)" -ne 0 ]; then
  if command -v sudo >/dev/null 2>&1; then
    CERTBOT=(sudo certbot)
  fi
fi

compose() {
  if docker compose version >/dev/null 2>&1; then
    docker compose -f "$COMPOSE_FILE" "$@"
    return
  fi
  if command -v docker-compose >/dev/null 2>&1; then
    docker-compose -f "$COMPOSE_FILE" "$@"
    return
  fi
  return 127
}

nginx_stop() {
  if [ -f "$COMPOSE_FILE" ] && compose ps >/dev/null 2>&1; then
    compose stop nginx >/dev/null
    return 0
  fi
  if docker ps --format '{{.Names}}' | grep -qx 'crm_nginx'; then
    docker stop crm_nginx >/dev/null
    return 0
  fi
  return 0
}

nginx_start() {
  if [ -f "$COMPOSE_FILE" ] && compose ps >/dev/null 2>&1; then
    compose start nginx >/dev/null
    return 0
  fi
  if docker ps -a --format '{{.Names}}' | grep -qx 'crm_nginx'; then
    docker start crm_nginx >/dev/null
    return 0
  fi
  return 0
}

nginx_reload() {
  if [ -f "$COMPOSE_FILE" ] && compose ps >/dev/null 2>&1; then
    compose exec -T nginx nginx -t >/dev/null
    compose exec -T nginx nginx -s reload >/dev/null
    return 0
  fi
  if docker ps --format '{{.Names}}' | grep -qx 'crm_nginx'; then
    docker exec crm_nginx nginx -t >/dev/null
    docker exec crm_nginx nginx -s reload >/dev/null
    return 0
  fi
  return 0
}

find_cert_dir() {
  if [ -z "${DOMAIN:-}" ]; then
    return 1
  fi

  local dir="/etc/letsencrypt/live/${DOMAIN}"
  if [ -f "${dir}/fullchain.pem" ] && [ -f "${dir}/privkey.pem" ]; then
    printf '%s\n' "$dir"
    return 0
  fi

  local alt
  alt="$(ls -d "/etc/letsencrypt/live/${DOMAIN}-"* 2>/dev/null | sort -V | tail -n 1 || true)"
  if [ -n "$alt" ] && [ -f "${alt}/fullchain.pem" ] && [ -f "${alt}/privkey.pem" ]; then
    printf '%s\n' "$alt"
    return 0
  fi

  return 1
}

detect_authenticator() {
  if [ -z "${DOMAIN:-}" ]; then
    return 1
  fi

  local conf="/etc/letsencrypt/renewal/${DOMAIN}.conf"
  if [ ! -f "$conf" ]; then
    conf="$(ls -1 "/etc/letsencrypt/renewal/${DOMAIN}-"*.conf 2>/dev/null | sort -V | tail -n 1 || true)"
  fi
  if [ -z "$conf" ] || [ ! -f "$conf" ]; then
    return 1
  fi

  awk -F' *= *' '$1=="authenticator"{print $2; exit}' "$conf"
}

link_certs_into_project() {
  local cert_dir="$1"
  mkdir -p "$SSL_DIR"

  ln -sf "${cert_dir}/fullchain.pem" "${SSL_DIR}/fullchain.pem"
  ln -sf "${cert_dir}/privkey.pem" "${SSL_DIR}/privkey.pem"
  if [ -f "${cert_dir}/chain.pem" ]; then
    ln -sf "${cert_dir}/chain.pem" "${SSL_DIR}/chain.pem"
  else
    ln -sf "${cert_dir}/fullchain.pem" "${SSL_DIR}/chain.pem"
  fi
}

AUTHENTICATOR="$(detect_authenticator || true)"
STOP_NGINX="0"
if [ "$STOP_MODE" = "stop" ]; then
  STOP_NGINX="1"
elif [ "$STOP_MODE" = "no-stop" ]; then
  STOP_NGINX="0"
else
  if [ "$AUTHENTICATOR" = "standalone" ]; then
    STOP_NGINX="1"
  fi
fi

STOPPED="0"
cleanup() {
  if [ "$STOPPED" = "1" ]; then
    nginx_start || true
  fi
}
trap cleanup EXIT

if [ "$STOP_NGINX" = "1" ]; then
  nginx_stop || true
  STOPPED="1"
fi

RENEW_ARGS=(renew)
if [ "$DRY_RUN" = "1" ]; then
  RENEW_ARGS+=(--dry-run)
fi

"${CERTBOT[@]}" "${RENEW_ARGS[@]}"

if CERT_DIR="$(find_cert_dir 2>/dev/null)"; then
  link_certs_into_project "$CERT_DIR"
fi

if [ "$STOPPED" = "1" ]; then
  nginx_start || true
  STOPPED="0"
fi

nginx_reload || true

echo "OK"
