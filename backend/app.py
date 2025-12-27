from flask import Flask
from config import Config
from extensions import db, jwt, cors
from routes.analytics import analytics_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # Import and register blueprints
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

if __name__ == "__main__":
    app.run(debug=True)
