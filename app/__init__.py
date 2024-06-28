import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask_admin.menu import MenuLink
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import MetaData
from config import Config

# Instantiate Flask extensions
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
csrf_protect = CSRFProtect()
mail = Mail()
migrate = Migrate()
bootstrap = Bootstrap()
moment = Moment()
login = LoginManager()
login.login_view = 'admin_bp.admin_login'
login.login_message = 'Пожалуйста, авторизируйтесь на сайте'


def create_app(config_class=Config):
    # Create a Flask applicaction.
    # Instantiate Flask
    app = Flask(__name__)
    # Load App Config settings
    app.config.from_object(config_class)
    # Setup Flask-SQLAlchemy
    db.init_app(app)
    # Setup Flask-Migrate
    migrate.init_app(app, db)
    # Setup Flask-Mail
    mail.init_app(app)
    # Setup Flask-Login
    login.init_app(app)
    # Setup WTForms CSRFProtect
    csrf_protect.init_app(app)
    # Setup Bootstrap
    bootstrap.init_app(app)
    # Setup Moment
    moment.init_app(app)

    # Register blueprints
    # Admin
    from app.admin import admin_bp
    app.register_blueprint(admin_bp)


    # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    from wtforms.fields import HiddenField

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    class AdminUserView(ModelView):
        can_edit = True
        can_create = True
        can_delete = True
        can_view_details = True
        column_exclude_list = ['password_hash']
        form_excluded_columns = ['password_hash']

        form_columns = ['username', 'email', 'password_hash', 'registry', 'admin']


    # # Admin model views
    admin = Admin(app, name='Админка', template_mode='bootstrap3')
    #
    # # Main model views
    from app.models.models import User
    admin.add_view(AdminUserView(User, db.session, name='Пользователь'))

    admin.add_link(MenuLink(name='Выход', endpoint='admin_bp.admin_login'))


    return app
