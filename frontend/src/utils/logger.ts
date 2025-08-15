/**
 * Centralized logging utility
 * Only logs in development mode to avoid cluttering production logs
 */

interface LogLevel {
  ERROR: 'error';
  WARN: 'warn';
  INFO: 'info';
  DEBUG: 'debug';
}

const LOG_LEVELS: LogLevel = {
  ERROR: 'error',
  WARN: 'warn',
  INFO: 'info',
  DEBUG: 'debug'
};

class Logger {
  private isDev = import.meta.env.DEV;

  private log(level: keyof LogLevel, message: string, ...args: unknown[]) {
    if (this.isDev) {
      console[LOG_LEVELS[level]](message, ...args);
    }
  }

  error(message: string, ...args: unknown[]) {
    this.log('ERROR', message, ...args);
  }

  warn(message: string, ...args: unknown[]) {
    this.log('WARN', message, ...args);
  }

  info(message: string, ...args: unknown[]) {
    this.log('INFO', message, ...args);
  }

  debug(message: string, ...args: unknown[]) {
    this.log('DEBUG', message, ...args);
  }
}

export const logger = new Logger();
export default logger;
