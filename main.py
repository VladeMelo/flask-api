from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import datetime
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

items = []

@app.route('/items', methods=['GET'])
def list_items():
    return jsonify(items), 200

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = {
        'id': len(items) + 1,
        'name': data['name'],
        'value': data['value'],
        'creation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'is_electronic': data['is_electronic']
    }

    items.append(new_item)

    return jsonify(new_item), 201

@app.route('/items', methods=['PUT'])
def update_item():
    data = request.get_json()
    for item in items:
        if item['id'] == data['id']:
            item.update({
                'name': data.get('name', item['name']),
                'value': data.get('value', item['value']),
                'is_electronic': data.get('is_electronic', item['is_electronic'])
            })
            
            return jsonify(item), 200
        
    return jsonify({'error': 'Item not found'}), 404

@app.route('/items', methods=['DELETE'])
def delete_item():
    data = request.get_json()

    global items
    items = [item for item in items if item['id'] != data['id']]

    return jsonify({'message': 'Item deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
