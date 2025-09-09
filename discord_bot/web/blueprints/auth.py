from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.auth import authenticate_user, register_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if authenticate_user(username, password):
            session['user'] = username
            flash('ログイン成功', 'success')
            return redirect(url_for('dashboard.index'))
        flash('ログイン失敗: ユーザー名またはパスワードが間違っています', 'danger')
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if register_user(username, password):
            flash('登録成功', 'success')
            return redirect(url_for('auth.login'))
        flash('登録失敗: ユーザー名が既に使用されています', 'danger')
    return render_template('auth/register.html')

@auth.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))