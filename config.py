class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    JWT_SECRET_KEY = "bigsecret"
    DATABASE_URI = 'postgres://vhgxtqnhjxsisd:224afcd6908b388a13a86418e71a7f5f66f0e33d406e8b46d82d25f088ef00c2@ec2-54-225-110-156.compute-1.amazonaws.com:5432/d2qnpu0duojjn'


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True
    DATABASE_URI = 'postgresql://postgres:maka1997@localhost/testdb'


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
   


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

