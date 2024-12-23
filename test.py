import pytest
from flask import json
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_list_items_empty(client):
    response = client.get('/items')
    assert response.status_code == 200
    assert response.json == []

def test_add_item(client):
    new_item = {
        'name': 'Laptop',
        'value': 1200.99,
        'is_electronic': True
    }
    response = client.post('/items', json=new_item)
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['name'] == 'Laptop'
    assert response.json['value'] == 1200.99
    assert response.json['is_electronic'] == True
    
def test_list_items_with_data(client):
    response = client.get('/items')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_update_item(client):
    update_data = {
        'id': 1,
        'name': 'Updated Laptop',
        'value': 999.99
    }
    response = client.put('/items', json=update_data)
    assert response.status_code == 200
    assert response.json['name'] == 'Updated Laptop'
    assert response.json['value'] == 999.99

def test_update_item_not_found(client):
    update_data = {
        'id': 999,
        'name': 'Non-existent item'
    }
    response = client.put('/items', json=update_data)
    assert response.status_code == 404
    assert response.json['error'] == 'Item not found'

def test_delete_item(client):
    delete_data = {'id': 1}
    response = client.delete('/items', json=delete_data)
    assert response.status_code == 200
    assert response.json['message'] == 'Item deleted successfully'

def test_delete_item_not_found(client):
    delete_data = {'id': 999}
    response = client.delete('/items', json=delete_data)
    assert response.status_code == 200
    response_list = client.get('/items')
    assert len(response_list.json) == 0
