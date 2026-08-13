from .dashboard import dashboard_bp
from .departments import departments_bp
from .employees import employees_bp


def register_blueprints(app):
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(departments_bp)
    app.register_blueprint(employees_bp)
