from flask import render_template, redirect, url_for, request, flash
from flask_admin import expose
from flask_login import current_user, logout_user, login_user
from werkzeug.urls import url_parse
from app.admin import admin_bp
from app.forms.auth_forms import AdminLoginForm
from app.models.models import User


@expose('/')
def index(self):
    if not current_user.is_authenticated:
        return redirect(url_for('admin_bp.admin_login'))
    return self.render('admin_panel.html')


@admin_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_bp.index'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Неверная пара логин/пароль", "error")
            return redirect(url_for('admin_bp.admin_login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin_bp.index')
        return redirect(next_page)
    return render_template('admin_login.html', form=form)


@admin_bp.route('/admin_logout')
def admin_logout():
    logout_user()
    return redirect(url_for('admin_bp.admin_login'))