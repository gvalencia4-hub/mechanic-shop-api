import os
from application import create_app

config_name = os.environ.get("FLASK_CONFIG") or "DevelopmentConfig"
app = create_app(config_name)