from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from sqlalchemy import select
from app import db, limiter
from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('auth.login'))
    # HTML şablonları şu an için var olmadığı için hata verebilir, kısıt gereği sadece yönlendirmeyi yapıyoruz
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            select(User).where(
                (User.username == form.username.data) | (User.email == form.username.data)
            )
        )
        if user is None or not user.check_password(form.password.data):
            flash('Geçersiz kullanıcı adı veya şifre', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        flash('Başarıyla giriş yaptınız!', 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
