from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import init_database
from models.user import User


class Store:
    def __init__(self, engine):
        """
        :param engine: The engine route and login details
        :return: a new instance of Data Store class
        :type engine: string
        """
        if not engine:
            raise ValueError('The values specified in engine parameter has to be supported by SQLAlchemy')
        self.engine = engine
        db_engine = create_engine(engine)
        db_session = sessionmaker(bind=db_engine)
        self.session = db_session()

    def init_database(self):
        """
        Initializes the database tables and relationships
        :return: None
        """
        init_database(self.engine)

    def add_user(self, email):
        """
        Creates and saves a new user to the database.

        :param email: Email address of the user
        :return: The id of the new user
        """
        new_user = User(email=email)

        self.session.add(new_user)
        self.session.commit()

        return new_user.id

    def get_users(self, id=None, email=None, serialize=False):
        """
        If the id parameter is  defined then it looks up the user with the given id,
        otherwise it loads all the users

        :param id: The id of the user which needs to be loaded (default value is None)
        :return: The list of users
        """
        if id is None:
            if email is None:
                all_users = self.session.query(User).order_by(User.email).all()
            else:
                all_users = self.session.query(User).filter(User.email == email).all()
        else:
            all_users = self.session.query(User).filter(User.id == id).all()

        if serialize:
            return [u.serialize() for u in all_users]
        else:
            return all_users


    def delete_user(self, id):
        try:
            self.session.query(User).filter_by(id=id).delete()
            return True
        except:
            return None