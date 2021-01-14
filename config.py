import os
if os.path.exists("env.py"):
    import env


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")

    MONGO_URI = os.environ.get("MONGO_URI")

    MONGODB_SETTINGS = {
        'db': os.environ.get("MONGO_DBNAME"),
        'host': os.environ.get("MONGO_URI")
        }
