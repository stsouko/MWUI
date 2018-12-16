# -*- coding: utf-8 -*-
#
#  Copyright 2018 Ramil Nugmanov <stsouko@live.ru>
#  This file is part of CIPress.
#
#  CIPress is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
from flask import Blueprint, redirect, url_for, request, current_app, flash, render_template
from flask_login import login_user, logout_user, login_required, current_user
from pony.orm import db_session
from .database import User
from .forms import (RegistrationForm, LoginForm, LogoutForm, CheckPasswordForm, ChangePasswordForm, NewPasswordForm,
                    EmailForm)
from ...utils import is_safe_url, send_mail


bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


@bp.route('/login', methods=('GET', 'POST'))
@db_session
def login():
    target = request.args.get('next')
    if not target or not is_safe_url(target):
        target = url_for('main.index')
    if current_user.is_authenticated:
        return redirect(target)

    form = LoginForm()
    if form.validate_on_submit():
        u = User[current_app.config['schema']].get(email=form.email.data.lower())
        login_user(u, remember=form.remember.data)
        return redirect(target)
    return render_template('auth/form.html', form=form, title='Authorization')


@bp.route('/register', methods=('GET', 'POST'))
@db_session
def register():
    target = request.args.get('next')
    if not target or not is_safe_url(target):
        target = url_for('main.index')
    if current_user.is_authenticated:
        return redirect(target)

    form = RegistrationForm()
    if form.validate_on_submit():
        u = User[current_app.config['schema']](email=form.email.data.lower(), password=form.password.data)
        flash('Check email box for message with instructions')
        message = current_app.config['registration_mail'].copy()
        message['message'] = message['message'] % url_for('auth.confirm', token=u.restore, next=target)
        send_mail(mail_to=u.email, **message)
        return redirect(url_for('auth.login', next=target))
    return render_template('auth/form.html', form=form, title='Registration')


@bp.route('/confirm/<string:token>', methods=('GET',))
@db_session
def confirm(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    u = User[current_app.config['schema']].get(restore=token)
    if u:
        u.is_active = True
        u.restore = None
        target = request.args.get('next') or url_for('main.index')
        flash('Email confirmed. Please login')
        return redirect(url_for('auth.login', next=target))
    flash('Invalid confirm token')
    return redirect(url_for('auth.login'))


@bp.route('/logout', methods=('GET', 'POST'))
@login_required
def logout():
    form = LogoutForm()
    if form.validate_on_submit():
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template('auth/form.html', form=form, title='Log out')


@bp.route('/droptail', methods=('GET', 'POST'))
@db_session
@login_required
def logout_all():
    form = CheckPasswordForm()
    if form.validate_on_submit():
        current_user.change_token()
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template('auth/form.html', form=form, title='Log out from all devices')


@bp.route('/password', methods=('GET', 'POST'))
@db_session
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.change_password(form.password.data)
        logout_user()
        flash('Password changed. Please login with new password')
        return redirect(url_for('auth.login'))
    return render_template('auth/form.html', form=form, title='Change password')


@bp.route('/restore/', methods=('GET', 'POST'))
@db_session
def forgot():
    target = request.args.get('next')
    if not target or not is_safe_url(target):
        target = url_for('main.index')
    if current_user.is_authenticated:
        return redirect(target)

    form = EmailForm()
    if form.validate_on_submit():
        u = User[current_app.config['schema']].get(email=form.email.data.lower())
        if u:
            token = u.get_restore_token()
            message = current_app.config['restore_mail'].copy()
            message['message'] = message['message'] % url_for('auth.restore', token=token, next=target)
            send_mail(mail_to=u.email, **message)
        flash('Check email box for message with instructions')
        return redirect(url_for('auth.login'))
    return render_template('auth/form.html', form=form, title='Restore access')


@bp.route('/restore/<string:token>', methods=('GET', 'POST'))
@db_session
def restore(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = NewPasswordForm()
    if form.validate_on_submit():
        u = User[current_app.config['schema']].get(restore=token)
        if u:
            u.change_password(form.password.data)
            u.restore = None
            target = request.args.get('next') or url_for('main.index')
            flash('Password changed. Please login with new password')
            return redirect(url_for('auth.login', next=target))
        flash('Invalid restore token')
        return redirect(url_for('auth.login'))
    return render_template('auth/form.html', form=form, title='Restore access')
