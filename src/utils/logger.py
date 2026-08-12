import logging
from src.config.settings import BASE_DIR

LOG_DIRECTORY = BASE_DIR / "logs"
LOG_DIRECTORY.mkdir(exist_ok=True)

logger = logging.getLogger("EnterpriseRAG")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(
    LOG_DIRECTORY / "application.log"
)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)