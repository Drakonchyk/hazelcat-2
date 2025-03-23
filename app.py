from flask import Flask
from routes.fill_map_route import fill_map_blueprint
from routes.get_value_route import get_value_blueprint
from routes.increment_no_locks_route import increment_no_locks_blueprint
from routes.increment_pessimistic_route import increment_pessimistic_blueprint
from routes.increment_optimistic_route import increment_optimistic_blueprint

def create_app():
    app = Flask(__name__)

    app.register_blueprint(fill_map_blueprint, url_prefix="/")
    app.register_blueprint(get_value_blueprint, url_prefix="/")
    app.register_blueprint(increment_no_locks_blueprint, url_prefix="/")
    app.register_blueprint(increment_pessimistic_blueprint, url_prefix="/")
    app.register_blueprint(increment_optimistic_blueprint, url_prefix="/")

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(port=5100, debug=True)
