from flask import Flask
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base


class DbConf:
    app = Flask(__name__)
    app.config.from_pyfile('../../../conf/config.py')

    DATABASE = 'sqlite:///sqlite/pychain_db_%s.sqlite3' % (
        app.config['NODE_NUMBER']
    )

    ENGINE = create_engine(
        DATABASE,
        encoding = "utf-8",
        echo = True
    )

    session = scoped_session(
        sessionmaker(
            autocommit = False,
            autoflush = False,
            bind = ENGINE
        )
    )

    Base = declarative_base()
    Base.query = session.query_property()


def main():
    DbConf.Base.metadata.create_all(bind = DbConf.ENGINE)


if __name__ == "__main__":
    main()
