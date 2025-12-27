from extensions import db
from datetime import date

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(200))
    expense_date = db.Column(db.Date, default=date.today)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
