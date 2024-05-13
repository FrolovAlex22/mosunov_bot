import logging

format = '[{asctime}] #{levelname:8} {filename}:'\
           '{lineno} - {name} - {message}'

formatter = logging.Formatter(
    fmt=format,
    style='{'
)

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler(filename='logs.log', encoding='utf-8')

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

print(logger.handlers)

logger.warning('Это лог с предупреждением!')
