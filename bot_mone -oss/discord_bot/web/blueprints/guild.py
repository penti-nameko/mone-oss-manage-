from flask import Blueprint, render_template, request, redirect, url_for, flash

from database.db_manager import get_guilds, get_guild_details

guild_bp = Blueprint('guild', __name__)

@guild_bp.route('/guilds')
def guild_list():
    guilds = get_guilds()  # DBから取得
    return render_template('guilds/index.html', guilds=guilds)

@guild_bp.route('/guilds/<int:guild_id>')
def guild_detail(guild_id):
    guild = get_guild_details(guild_id)  # DBから取得
    if guild is None:
        flash('Guild not found', 'error')
        return redirect(url_for('guild.guilds'))
    return render_template('guilds/detail.html', guild=guild)

@guild_bp.route('/guilds/<int:guild_id>/settings', methods=['GET', 'POST'])
def guild_settings(guild_id):
    if request.method == 'POST':
        # DBに設定反映
        return redirect(url_for('guild.guild_detail', guild_id=guild_id))
    settings = {}  # DBから取得
    return render_template('moderation/settings.html', settings=settings)

from flask import Blueprint

guild = Blueprint('guild', __name__)

# 必要ならルートを追加
@guild.route('/guilds')
def guilds():
    return 'guilds endpoint'