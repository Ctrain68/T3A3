from flask import Flask, jsonify
from marshmallow.exceptions import ValidationError
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy, func
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

func = func()
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("default_settings.app_config")

    # if app.config["ENV"] == "production":
    #     from log_handlers import file_handler
    #     app.logger.addHandler(file_handler)

    # from database import init_db
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    func.init(app)


   

    from commands import db_commands
    app.register_blueprint(db_commands)

    from controllers import registerable_controllers

    for controller in registerable_controllers:
        app.register_blueprint(controller)

    @app.errorhandler(ValidationError)
    def handle_bad_request(error):
        return (jsonify(error.messages), 400)

    return app
# if __name__ == '__main__':
#     app.run(debug=True)
