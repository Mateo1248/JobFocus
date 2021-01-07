from flask_login import LoginManager, login_required, current_user
from flask_principal  import Principal, identity_loaded, RoleNeed, UserNeed, Permission, RoleNeed
from app.src.services.user import get_user_by_id


def init_auth(app):
    global admin_permission
    global employee_permission
    global employeer_permission

    login_manager = LoginManager()
    login_manager.login_view = 'auth.auth'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)


    Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user

        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        if hasattr(current_user, 'role'):
            identity.provides.add(RoleNeed(current_user.role))

    admin_permission = Permission(RoleNeed('admin'))
    employee_permission = Permission(RoleNeed('employee'))
    employeer_permission = Permission(RoleNeed('employeer'))
