from .dashboard import dashboard_bp
from .departments import departments_bp


def register_blueprints(app):
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(departments_bp)
