from flask import Flask, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

from .extensions import db, ma, limiter, cache
from config import Config

from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.inventory import inventory_bp


def create_app(config_name="Config"):
    app = Flask(__name__)

    if config_name == "TestingConfig":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testing.db"
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    else:
        app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(
        app,
        config={
            "CACHE_TYPE": "SimpleCache",
            "CACHE_DEFAULT_TIMEOUT": 60
        }
    )

    app.register_blueprint(customers_bp)
    app.register_blueprint(mechanics_bp)
    app.register_blueprint(service_tickets_bp)
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    @app.route("/swagger")
    def spec():
        swag = swagger(app)
        swag["info"] = {
            "title": "My Mechanic Shop API",
            "version": "1.0",
            "description": "API documentation for My Mechanic Shop"
        }
        return jsonify(swag)

    SWAGGER_URL = "/api/docs"
    API_URL = "/swagger"

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "My Mechanic Shop API"}
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    with app.app_context():
        db.create_all()

    return app