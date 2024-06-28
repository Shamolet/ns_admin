from flask import Blueprint

admin_bp = Blueprint('admin_bp', __name__)

# flake8: noqa
from app.admin import routes