"""
Конфигурация логирования для Finance Backend.
Поддерживает JSON-формат для продакшена и текстовый формат для разработки.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json

# Импортируем настройки из config
from app.core.config import settings


class RequestIDFilter(logging.Filter):
    """Фильтр для добавления request ID к каждому лог-сообщению."""
    
    def __init__(self, request_id: str = None):
        super().__init__()
        self.request_id = request_id or generate_request_id()
    
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = self.request_id
        return True


def generate_request_id() -> str:
    """Генерирует уникальный ID для запроса."""
    import uuid
    return str(uuid.uuid4())[:8]


class RequestContextFilter(logging.Filter):
    """Фильтр для добавления контекста запроса к логам."""
    
    def __init__(self, context: Dict[str, Any] = None):
        super().__init__()
        self.context = context or {}
    
    def filter(self, record: logging.LogRecord) -> bool:
        for key, value in self.context.items():
            setattr(record, key, value)
        return True


class JSONFormatter(logging.Formatter):
    """Форматирование логов в JSON для продакшена."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Добавляем контекст запроса
        if hasattr(record, 'request_id'):
            log_record["request_id"] = record.request_id
        
        # Добавляем путь и метод запроса (если есть)
        if hasattr(record, 'path'):
            log_record["http_path"] = record.path
        
        if hasattr(record, 'method'):
            log_record["http_method"] = record.method
        
        # Добавляем дополнительные поля из extra
        for key in ['user_id', 'account_id', 'transaction_id', 'category_id']:
            if hasattr(record, key):
                log_record[key] = getattr(record, key)
        
        # Добавляем stack trace для ошибок
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_record, ensure_ascii=False)


class ColoredFormatter(logging.Formatter):
    """Цветное форматирование для консоли в разработке."""
    
    # Цвета для уровней логирования
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        level_color = self.COLORS.get(record.levelname, self.RESET)
        
        log_line = f"{level_color}[{record.levelname}]{self.RESET} "
        log_line += f"[{datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')}] "
        
        # Добавляем request_id если есть
        if hasattr(record, 'request_id'):
            log_line += f"[{record.request_id}] "
        
        log_line += f"{record.name} - {record.getMessage()}"
        
        if record.exc_info:
            log_line += f"\n{self.formatException(record.exc_info)}"
        
        return log_line


class StructuredLogger(logging.Logger):
    """Расширенный логгер с контекстом запроса."""
    
    def __init__(self, name: str = "finance"):
        super().__init__(name)
        self.context_stack: list[Dict[str, Any]] = []
    
    def bind(self, **kwargs) -> 'StructuredLogger':
        """Создает копию логгера с дополнительным контекстом."""
        new_logger = StructuredLogger(self.name)
        new_logger.setLevel(self.level)
        for handler in self.handlers:
            new_logger.addHandler(handler)
        
        # Сохраняем контекст в новом логгере
        if not hasattr(new_logger, 'context_stack'):
            new_logger.context_stack = []
        new_logger.context_stack.append(kwargs)
        
        return new_logger
    
    def unbind(self):
        """Убирает последний уровень контекста."""
        if self.context_stack:
            self.context_stack.pop()
    
    def _get_context(self) -> Dict[str, Any]:
        """Собирает весь текущий контекст."""
        context = {}
        for ctx in self.context_stack:
            context.update(ctx)
        return context
    
    def debug(self, msg: str, **kwargs):
        extra = self._get_context()
        extra.update(kwargs)
        super().debug(msg, extra=extra)
    
    def info(self, msg: str, **kwargs):
        extra = self._get_context()
        extra.update(kwargs)
        super().info(msg, extra=extra)
    
    def warning(self, msg: str, **kwargs):
        extra = self._get_context()
        extra.update(kwargs)
        super().warning(msg, extra=extra)
    
    def error(self, msg: str, **kwargs):
        extra = self._get_context()
        extra.update(kwargs)
        super().error(msg, extra=extra)
    
    def critical(self, msg: str, **kwargs):
        extra = self._get_context()
        extra.update(kwargs)
        super().critical(msg, extra=extra)


class RequestLoggingMiddleware:
    """Middleware для логирования HTTP запросов и ответов."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)
        
        from starlette.requests import Request
        request = Request(scope)
        
        # Генерируем ID запроса
        request_id = generate_request_id()
        
        start_time = datetime.utcnow()
        
        logger = logging.getLogger("finance.http")
        
        # Логирование входящего запроса
        logger.info(
            f"Request: {request.method} {request.url.path}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "query_params": str(request.query_params),
                "client_host": scope.get('client', [None])[0] if scope.get('client') else None,
                "user_agent": request.headers.get("user-agent", ""),
            },
        )
        
        # Создаем custom response
        async def send_wrapper(response):
            # Логирование ответа
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000
            response_status = None
            if response["type"] == "http.response.start":
                response_status = response["status"]
            logger.info(
                f"Response: {request.method} {request.url.path}",
                extra={
                    "path": request.url.path,
                    "method": request.method,
                    "status_code": response_status,
                    "duration_ms": duration,
                    "request_id": request_id,
                }
            )
            
            await send(response)
        
        # Добавляем request ID к запросу
        request.state.request_id = request_id
        
        await self.app(scope, receive, send_wrapper)


def setup_logging(
    log_level: str = "INFO",
    log_format: str = "text",  # "text" или "json"
    log_file: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
) -> StructuredLogger:
    """
    Настройка логирования приложения.
    
    Args:
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Формат логов ("text" или "json")
        log_file: Путь к файлу логов (если None - только в консоль)
        max_bytes: Максимальный размер файла перед ротацией
        backup_count: Количество файлов для хранения
    
    Returns:
        StructuredLogger: Настроенный логгер
    """
    
    # Создаем root logger
    root_logger = logging.getLogger("finance")
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Очищаем существующие handlers
    root_logger.handlers.clear()
    
    # Форматирование
    if log_format == "json":
        formatter = JSONFormatter()
    else:
        formatter = ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler с ротацией (если указан файл)
    if log_file:
        from logging.handlers import RotatingFileHandler
        
        file_path = Path(log_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            str(file_path),
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(logging.INFO)
        
        # Для файла используем обычный формат с timestamp
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        
        root_logger.addHandler(file_handler)
    
    # Настройка логгеров для конкретных модулей
    loggers = {
        "finance.app": logging.getLogger("finance.app"),
        "finance.api": logging.getLogger("finance.api"),
        "finance.crud": logging.getLogger("finance.crud"),
        "finance.service": logging.getLogger("finance.service"),
        "finance.err": logging.getLogger("finance.err"),
        "finance.http": logging.getLogger("finance.http"),
    }
    
    for name, logger_instance in loggers.items():
        logger_instance.setLevel(getattr(logging, log_level.upper()))
        logger_instance.propagate = False
    
    # Создаем и возвращаем структурированный логгер
    structured_logger = StructuredLogger("finance")
    return structured_logger


def get_logger(name: str = None) -> StructuredLogger:
    """
    Получение логгера с именем модуля.
    
    Args:
        name: Имя логгера (если None - используется имя вызывающего модуля)
    
    Returns:
        StructuredLogger: Логгер для использования в коде
    """
    import inspect
    
    if not name:
        # Автоматически определяем имя модуля
        frame = inspect.currentframe().f_back
        name = frame.f_globals["__name__"]
    
    return logging.getLogger(name)


def log_request_context(
    logger: StructuredLogger,
    user_id: str = None,
    account_id: str = None,
    transaction_id: str = None,
    category_id: str = None,
    request_path: str = None,
):
    """
    Запись контекста запроса в лог.
    
    Args:
        logger: Логгер для записи
        user_id: ID пользователя
        account_id: ID учетной записи
        transaction_id: ID транзакции
        category_id: ID категории
        request_path: Путь API endpoint
    """
    extra = {}
    
    if user_id:
        extra["user_id"] = user_id
    if account_id:
        extra["account_id"] = account_id
    if transaction_id:
        extra["transaction_id"] = transaction_id
    if category_id:
        extra["category_id"] = category_id
    if request_path:
        extra["path"] = request_path
    
    logger.info("Request context", extra=extra)


# Инициализация логгера при импорте модуля
def initialize_logging():
    """Инициализация логирования с настройками из config."""
    
    log_level = "DEBUG" if settings.DEBUG else "INFO"
    log_format = "json" if not settings.DEBUG else "text"
    
    # Для продакшена можно включить файл логов
    log_file = None  # "/var/log/finance-api/app.log" if not settings.DEBUG else None
    
    logger = setup_logging(
        log_level=log_level,
        log_format=log_format,
        log_file=log_file
    )
    
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    return logger


# Создаем логгер при импорте
logger = initialize_logging()
