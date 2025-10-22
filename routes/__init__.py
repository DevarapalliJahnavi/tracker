from .dashboard import dashboard_bp
from .expense import expense_bp
from .api import api_bp


def register_blueprints(app):
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(api_bp)
    print('Registered blueprints: dashboard, expense, api')
