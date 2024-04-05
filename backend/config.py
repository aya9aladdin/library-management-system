class Config:
    DEBUG = False
    TESTING = False
    MONGO_URI = "mongodb://localhost:27017/books_db"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    MONGO_URI = "mongodb://localhost:27017/test_books_db"
