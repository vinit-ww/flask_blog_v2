import os
basedir = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:default@127.0.0.1:3306/flywithvip'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
#upload folder link
UPLOAD_FOLDER = os.path.join(basedir,'upload')

