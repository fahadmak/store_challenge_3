class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    JWT_SECRET_KEY = "bigsecret"
    DATABASE_URI = 'postgres://tquvntrciomlye:0e9dfeca2f405e0f2193a3b7fbc6f316dd4f63caad0fdf9b5a4406bcb2fbc585@ec2-23-21-171-249.compute-1.amazonaws.com:5432/d1akcs0pg5u19u'
    JWT_ACCESS_TOKEN_EXPIRES = False


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

