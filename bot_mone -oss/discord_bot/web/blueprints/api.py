from flask import Blueprint, jsonify, request

from database.db_manager import get_session
from database.models import Guild, User, MessageLog, Setting

api_bp = Blueprint('api', __name__)

@api_bp.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"}), 200

@api_bp.route('/data', methods=['GET'])
def get_data():
    # Placeholder for data retrieval logic
    data = {"message": "This is sample data"}
    return jsonify(data), 200

@api_bp.route('/data/<int:item_id>', methods=['GET'])
def get_data_item(item_id):
    # Placeholder for retrieving a specific data item
    data_item = {"id": item_id, "message": f"This is data item {item_id}"}
    return jsonify(data_item), 200

@api_bp.route('/data', methods=['POST'])
def create_data():
    # Placeholder for data creation logic
    return jsonify({"message": "Data created"}), 201

@api_bp.route('/data/<int:item_id>', methods=['DELETE'])
def delete_data_item(item_id):
    # Placeholder for data deletion logic
    return jsonify({"message": f"Data item {item_id} deleted"}), 204

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@api_bp.route('/guilds', methods=['GET', 'POST'])
def guilds():
    session = get_session()
    if request.method == 'GET':
        guilds = session.query(Guild).all()
        result = [{'id': g.id, 'name': g.name, 'owner_id': g.owner_id} for g in guilds]
        session.close()
        return jsonify(result)
    else:
        data = request.json
        g = Guild(id=data['id'], name=data['name'], owner_id=data['owner_id'])
        session.add(g)
        session.commit()
        session.close()
        return jsonify({'result': 'created'})

@api_bp.route('/users', methods=['GET'])
def users():
    session = get_session()
    users = session.query(User).all()
    result = [{'id': u.id, 'name': u.name, 'discriminator': u.discriminator} for u in users]
    session.close()
    return jsonify(result)

@api_bp.route('/messages', methods=['GET'])
def messages():
    session = get_session()
    logs = session.query(MessageLog).order_by(MessageLog.created_at.desc()).limit(100).all()
    result = [{'id': m.id, 'guild_id': m.guild_id, 'user_id': m.user_id, 'content': m.content, 'created_at': m.created_at.isoformat()} for m in logs]
    session.close()
    return jsonify(result)

@api_bp.route('/settings/<int:guild_id>', methods=['GET', 'POST'])
def settings(guild_id):
    session = get_session()
    if request.method == 'GET':
        settings = session.query(Setting).filter_by(guild_id=guild_id).all()
        result = {s.key: s.value for s in settings}
        session.close()
        return jsonify(result)
    else:
        data = request.json
        for k, v in data.items():
            s = session.query(Setting).filter_by(guild_id=guild_id, key=k).first()
            if s:
                s.value = v
            else:
                s = Setting(guild_id=guild_id, key=k, value=v)
                session.add(s)
        session.commit()
        session.close()
        return jsonify({'result': 'updated'})

api = Blueprint('api', __name__)

# 必要ならルートを追加
@api.route('/ping')
def ping():
    return 'pong'