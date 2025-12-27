from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, jwt
from routes.analytics import analytics_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ ENABLE CORS FOR ALL ROUTES (IMPORTANT)
    CORS(
        app,
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.expenses import expense_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(expense_bp, url_prefix="/api/expenses")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")

    # Create database tables
    with app.app_context():
        from models import User, Expense
        db.create_all()

    return app


app = create_app()


# ✅ GLOBAL OPTIONS HANDLER (FIXES PREFLIGHT CORS ERROR)
@app.route("/api/<path:path>", methods=["OPTIONS"])
def options_handler(path):
    return "", 200


# ✅ ENSURE HEADERS ARE ALWAYS PRESENT
@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers",
        "Content-Type,Authorization"
    )
    response.headers.add(
        "Access-Control-Allow-Methods",
        "GET,POST,PUT,DELETE,OPTIONS"
    )
    response.headers.add(
        "Access-Control-Allow-Origin",
        "*"
    )
    return response


if __name__ == "__main__":
    app.run(debug=True)
