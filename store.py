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

    def get_users(self, serialize=False):
        """
        :return: The list of users
        """
        all_users = self.session.query(User).filter(User.id == id).all()
        if serialize:
            return [u.serialize() for u in all_users]
        else:
            return all_users

    def get_user_by_id(self, id, serialize=False):
        user = self.session.query(User).filter_by(id=id).first()
        if not user:
            return None
        if serialize:
            return user.serialize()
        else:
            return user

    def get_user_by_email(self, email, serialize=False):
        user = self.session.query(User).filter_by(email=email).first()
        if not user:
            return None
        if serialize:
            return user.serialize()
        else:
            return user

    def connect_users(self, user1_email, user2_email):
        user1 = self.session.query(User).filter_by(email=user1_email).first()
        user2 = self.session.query(User).filter_by(email=user2_email).first()
        user1.friends.append(user2)
        self.session.add(user1)
        self.session.commit()
        return True

    def delete_user(self, id):
        try:
            self.session.query(User).filter_by(id=id).delete()
            return True
        except:
            return None