from flask import Flask, request, jsonify
from bot.bot import bot_generate
import requests
from pathlib import Path
import requests
import os

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def communicate():
    data = request.json
    msgType = data.get('msgType', '')
    user_id = data.get('userId', '')
    user_nickname = data.get('userNickname', '')
    if msgType == 'file':
        filePath = data.get('filePath', '')
        fileName = data.get('fileName', '')
        response = add_doc_to_my_memory(user_id=user_id, user_nickname=user_nickname, file_path=filePath, file_name=fileName)
    else:
        message = data.get('message', '')
        response = bot_chat(message, user_id, user_nickname)
    response = {
        'message': response,
        'user_id': user_id,
        'user_nickname': user_nickname
    }
    return jsonify(response)

def bot_chat(message: str, user_id='MASTER_USER', user_nickname='MASTER_USER'):
    # parse command and execute
    AI_message = execute_command_from_query(message, user_id, user_nickname)
    return AI_message

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
