from flask import Blueprint, render_template

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    # DBから統計情報取得（仮）
    stats = {
        'guild_count': 0,
        'user_count': 0,
        'message_count': 0,
    }
    return render_template('dashboard/index.html', stats=stats)

@dashboard.route('/logs')
def logs():
    # DBからログ取得（仮）
    logs = []
    return render_template('logs/guild.html', logs=logs)