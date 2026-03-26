import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    """Base configuration class"""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "TOPSECRET"
    DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

    DB_HOST = os.environ.get("DB_HOST") or "localhost"
    DB_USER = os.environ.get("DB_USER") or "root"
    DB_PASSWORD = os.environ.get("DB_PASSWORD") or ""
    DB_NAME = os.environ.get("DB_NAME") or "greenery"
    DB_PORT = int(os.environ.get("DB_PORT", 3306))

    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "greenery"


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    DB_HOST = os.environ.get("DB_HOST")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_NAME = os.environ.get("DB_NAME")


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    DB_NAME = "greenery"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
