from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db, jwt
from routes.auth import auth_bp
from routes.expenses import expense_bp
from routes.analytics import analytics_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ CORS — APPLY ONCE, CORRECTLY
    CORS(
        app,
        resources={r"/api/*": {"origins": "https://expensetrackertomanageexpenses.netlify.app"}},
        supports_credentials=True
    )

    # Init extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(expense_bp, url_prefix="/api/expenses")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")

    # Create DB tables
    with app.app_context():
        from models import User, Expense
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
