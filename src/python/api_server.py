from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from database.operations import (
    init_db, add_chat_message, get_chat_history, get_recent_chat_history,
    add_memory, get_all_memories, delete_memory_by_key, get_database_stats,
    clear_chat_history, delete_chat_msg_by_id
)
from kairos_ai import KairosAI

# Set up paths
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_PATH))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "kairos.db")
SCHEMA_PATH = os.path.join(BASE_PATH, "database", "schema.sql")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize database and Kairos AI
init_db(DB_PATH, SCHEMA_PATH)
kairos = KairosAI()

@app.route('/api/chat', methods=['POST'])
def chat():
  data = request.json
  message = data.get('message')
  include_memories = data.get('include_memories', False)

  if not message:
    return jsonify({'error': 'Message is required'}), 400

  try:
    # Add user message to history
    add_chat_message('user', message, db_path=DB_PATH)
    
    # Generate Kairos response
    response = kairos.generate_response(message)
    
    # Add Kairos response to history
    add_chat_message('assistant', response, db_path=DB_PATH)
    
    return jsonify({'response': response})
  except Exception as e:
    return jsonify({'error': f'Failed to generate response: {str(e)}'}), 500

@app.route('/api/memories', methods=['GET', 'POST'])
def memories():
  if request.method == 'GET':
    memories = get_all_memories(db_path=DB_PATH)
    return jsonify({'memories': memories})
  elif request.method == 'POST':
    data = request.json
    memory_key = data.get('memory_key')
    memory_value = data.get('memory_value')
    priority = data.get('priority', 5)
    
    if not memory_key or not memory_value:
      return jsonify({'error': 'Memory key and value are required'}), 400
    
    try:
      add_memory(memory_key, memory_value, priority, db_path=DB_PATH)
      return jsonify({'message': 'Memory added successfully'})
    except Exception as e:
      return jsonify({'error': f'Failed to add memory: {str(e)}'}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
  try:
    stats = get_database_stats(db_path=DB_PATH)
    return jsonify({'stats': stats})
  except Exception as e:
    return jsonify({'error': f'Failed to get database stats: {str(e)}'}), 500

@app.route('/api/chat-history', methods=['GET', 'DELETE'])
def chat_history():
  if request.method == 'GET':
    try:
      limit = request.args.get('limit', type=int)
      history = get_chat_history(limit=limit, db_path=DB_PATH)
      return jsonify({'history': history})
    except Exception as e:
      return jsonify({'error': f'Failed to get chat history: {str(e)}'}), 500
  elif request.method == 'DELETE':
    try:
      clear_chat_history(db_path=DB_PATH)
      return jsonify({'message': 'Chat history cleared successfully'})
    except Exception as e:
      return jsonify({'error': f'Failed to clear chat history: {str(e)}'}), 500

@app.route('/api/chat-history/<int:msg_id>', methods=['DELETE'])
def delete_chat_message(msg_id):
  try: 
    success = delete_chat_msg_by_id(msg_id, db_path=DB_PATH)
    if success:
      return jsonify({'message': f'Chat message {msg_id} deleted successfully'})
    else:
      return jsonify({'error': f'Chat message {msg_id} not found'}), 404
  except Exception as e:
    return jsonify({'error': f'Failed to delete chat message: {str(e)}'}), 500
  
@app.route('/api/memories/<memory_key>', methods=['DELETE'])
def delete_memory(memory_key):
  try:
    success = delete_memory_by_key(memory_key, db_path=DB_PATH)
    if success:
      return jsonify({'message': f'Memory "{memory_key}" deleted successfully'})
    else:
      return jsonify({'error': f'Memory "{memory_key}" not found'}), 404
  except Exception as e:
    return jsonify({'error': f'Failed to delete memory: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)