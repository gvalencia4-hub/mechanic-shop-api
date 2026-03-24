import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    TESTING = False
    DEBUG = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///mechanic_shop.db"
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URI")
        or os.environ.get("SQLALCHEMY_DATABASE_URI")
    )
    SECRET_KEY = os.environ.get("SECRET_KEY", "prod-secret")
    DEBUG = False
    TESTING = False