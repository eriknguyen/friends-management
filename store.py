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

    def get_users(self, email_list=None, serialize=False):
        """
        :return: The list of users
        """
        if email_list:
            all_users = self.session.query(User).filter(User.email.in_(email_list)).all()
        else:
            all_users = self.session.query(User).all()
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

    def delete_user(self, id):
        try:
            self.session.query(User).filter_by(id=id).delete()
            return True
        except:
            return None

    def connect_users(self, user1_email, user2_email):
        user1 = self.get_user_by_email(user1_email)
        user2 = self.get_user_by_email(user2_email)
        user1.friends.append(user2)
        user2.friends.append(user1)
        self.session.add(user1)
        self.session.add(user2)
        self.session.commit()
        return True

    def get_user_friends(self, email, serialize=False):
        user = self.session.query(User).filter_by(email=email).first()
        if serialize:
            return [u.serialize() for u in user.friends]
        else:
            return user.friends

    def get_user_common_friends(self, user1_email, user2_email):
        user1_friends = self.get_user_friends(user1_email)
        user2_friends = self.get_user_friends(user2_email)
        common_friends = []
        # temporarily using a quadraric-time function to find common friends
        for friend in user1_friends:
            if friend in user2_friends:
                common_friends.append(friend)

        return common_friends


    def subscribe_user(self, requestor_email, target_email):
        requestor = self.get_user_by_email(requestor_email)
        target = self.get_user_by_email(target_email)
        requestor.subscribings.append(target)
        self.session.add(requestor)
        self.session.commit()
        return True


    def block_user(self, requestor_email, target_email):
        requestor = self.get_user_by_email(requestor_email)
        target = self.get_user_by_email(target_email)
        requestor.blockings.append(target)
        self.session.add(requestor)
        self.session.commit()
        return True

    def get_user_subscribers(self, email, serialize=False):
        user = self.session.query(User).filter_by(email=email).first()
        if serialize:
            return [u.serialize() for u in user.subscribers]
        else:
            return user.subscribers

    def get_user_blocked_list(self, email, serialize=False):
        user = self.session.query(User).filter_by(email=email).first()
        if serialize:
            return [u.serialize() for u in user.blockeds]
        else:
            return user.blockeds