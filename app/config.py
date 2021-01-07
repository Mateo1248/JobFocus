import os

MODEL_URL = "http://127.0.0.1:8003/model/predict"
SEARCH_LIMIT = 10000

class Config:
    SECRET_KEY = ".ňƗŲ\x18Ǯô\x82ĂƆŎ\x96ƃƦ\x928¿ƌƁa"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgres://{}:{}@{}/{}".format(
        "postgres",
        "postgres",
        "localhost:5433",
        "jobfocus_test"
    )
    ENV = "development"


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgres://{}:{}@{}/{}".format(
        "postgres",
        "postgres",
        "localhost:5433",
        "jobfocus"
    )
    ENV = "production"


get_config = dict(
    development=DevelopmentConfig,
    production=ProductionConfig
)