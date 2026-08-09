from .dashboard import dashboard_bp

def register_blueprints(app):
    app.register_blueprint(dashboard_bp)