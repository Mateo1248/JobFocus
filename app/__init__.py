from flask import Flask
from flask_login import LoginManager

from app.src.models import init_db
from app.src.utils.auth import init_auth
from app.src.utils.ml_utils import init_cache
from app.config import get_config


def create_app(config_name):

    # init app
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='src/templates'
    )
    app.config.from_object(get_config[config_name])
    app.app_context().push()

    init_db(app)
    init_auth(app)

    # init cache for recommendation
    init_cache()

    # register blueprints
    from app.src.controllers.auth import auth_bp
    from app.src.controllers.index import index_page
    from app.src.controllers.recommendation import recommendation_ep
    from app.src.controllers.user import user_ep
    from app.src.controllers.stats import stats_ep
    app.register_blueprint(stats_ep)
    app.register_blueprint(auth_bp)
    app.register_blueprint(index_page)
    app.register_blueprint(user_ep)
    app.register_blueprint(recommendation_ep)

    return app