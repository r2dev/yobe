from app import create, db
from app.models import User
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

yoke = create()


if __name__ == "__main__":
	yoke.run()