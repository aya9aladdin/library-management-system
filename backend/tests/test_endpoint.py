import pytest
import sys
import random

sys.path.append('../')  

from main import app
from pymongo import MongoClient
from config import TestingConfig

DATABASE = "test_books_db"
COLLECTION = "books"

@pytest.fixture
def test_client():
    app.config.from_object(TestingConfig)
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


def test_get_books(test_client):
    response = test_client.get('/books/')
    assert response.status_code == 200

def test_post_book(test_client):
    book_data = {
        'title': 'Test Book',
        'ISBN': '123',
        'genre': 'Test Genre',
        'author': 'Test Author',
        'pub_year': 2024
    }

    response = test_client.post('/books/', json=book_data)

    assert response.status_code == 200

    assert response.json['message'] == "Book added successfully"

def test_post_book_with_bad_data(test_client):
    book_data = {
        'ISBN': '12345637890',
        'genre': 'Test Genre',
        'author': 'Test Author',
        'pub_year': 2024
    }

    response = test_client.post('/books/', json=book_data)

    assert response.status_code == 400

    assert response.json['message']["title"] == 'title is required'