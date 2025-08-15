import { logger } from './logger';

export interface ApiError {
  message: string;
  code?: string;
  status?: number;
  details?: Record<string, unknown>;
}

export class ErrorHandler {
  /**
   * Extract error message from various error types
   */
  static getErrorMessage(error: unknown): string {
    if (typeof error === 'string') {
      return error;
    }

    if (error && typeof error === 'object') {
      // Axios error
      const axiosError = error as {
        response?: {
          data?: {
            detail?: string | Array<{ msg: string }>;
            message?: string;
          };
          status?: number;
        };
        message?: string;
      };

      if (axiosError.response?.data?.detail) {
        const detail = axiosError.response.data.detail;
        if (typeof detail === 'string') {
          return detail;
        }
        if (Array.isArray(detail)) {
          return detail.map((err) => err.msg).join(', ');
        }
      }

      if (axiosError.response?.data?.message) {
        return axiosError.response.data.message;
      }

      if (axiosError.message) {
        return axiosError.message;
      }

      // Generic error with message property
      const genericError = error as { message?: string };
      if (genericError.message) {
        return genericError.message;
      }
    }

    return 'Ocorreu um erro inesperado';
  }

  /**
   * Log error and return user-friendly message
   */
  static handle(error: unknown, context?: string): string {
    const message = this.getErrorMessage(error);
    
    if (context) {
      logger.error(`[${context}] ${message}`, error);
    } else {
      logger.error(message, error);
    }

    return message;
  }

  /**
   * Check if error is network related
   */
  static isNetworkError(error: unknown): boolean {
    if (error && typeof error === 'object') {
      const axiosError = error as {
        code?: string;
        response?: { status?: number };
      };
      
      return (
        axiosError.code === 'NETWORK_ERROR' ||
        axiosError.code === 'ECONNREFUSED' ||
        !axiosError.response
      );
    }
    return false;
  }

  /**
   * Check if error is authentication related
   */
  static isAuthError(error: unknown): boolean {
    if (error && typeof error === 'object') {
      const axiosError = error as { response?: { status?: number } };
      return axiosError.response?.status === 401 || axiosError.response?.status === 403;
    }
    return false;
  }
}

export default ErrorHandler;
