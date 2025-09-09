from flask import Flask, render_template
from web.blueprints.api import api
from web.blueprints.guild import guild
from web.blueprints.auth import auth
from web.blueprints.dashboard import dashboard
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

app = Flask(__name__, template_folder='web/templates')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

# Blueprint登録
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(guild, url_prefix='/guild')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(dashboard, url_prefix='/dashboard')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.errorhandler(404)
def not_found(e):
    return '404 Not Found', 404

@app.errorhandler(500)
def server_error(e):
    return '500 Internal Server Error', 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000, debug=False)
    except KeyboardInterrupt:
        print('Web server stopped by user (KeyboardInterrupt)')
    finally:
        pass