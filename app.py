import os

from app.models.database import Database
from app import create_app

app = create_app("development")
db = Database(app.config['DATABASE_URI'])
if __name__ == '__main__':
    app.run()
