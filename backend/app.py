from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ SINGLE, CORRECT CORS CONFIG
    CORS(
        app,
        resources={r"/api/*": {
            "origins": "https://expensetrackertomanageexpenses.netlify.app"
        }},
        supports_credentials=True
    )

    db.init_app(app)
    jwt.init_app(app)

    from routes.auth import auth_bp
    from routes.expenses import expense_bp
    from routes.analytics import analytics_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(expense_bp, url_prefix="/api/expenses")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")

    with app.app_context():
        from models import User, Expense
        db.create_all()

    return app


app = create_app()


# ✅ THIS IS CRITICAL: handle preflight
@app.route("/api/<path:path>", methods=["OPTIONS"])
def options_handler(path):
    return "", 200


if __name__ == "__main__":
    app.run(debug=True)
