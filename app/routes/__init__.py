from .dashboard import dashboard_bp
from .departments import departments_bp
from .employees import employees_bp
from .users import users_bp
from .reports import reports_bp
from .settings import settings_bp


def register_blueprints(app):
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(departments_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(settings_bp)
