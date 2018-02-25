import sqlalchemy as db
from sqlalchemy.orm import relationship, backref
from . import Model

friend_map = db.Table(
    'friend_map',
    Model.metadata,
    db.Column('user1_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('user2_id', db.Integer, db.ForeignKey('user.id'))
)

follow_map = db.Table(
    'subscribe_map',
    Model.metadata,
    db.Column('subscriber_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('target_id', db.Integer, db.ForeignKey('user.id'))
)

block_map = db.Table(
    'block_map',
    Model.metadata,
    db.Column('blocker_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('target_id', db.Integer, db.ForeignKey('user.id'))
)


class User(Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    email = db.Column(db.String(200), nullable=False)

    # friends = relationship('User', secondary=friend_map, backref=backref('friends', lazy='joined'), lazy='dynamic')
    # followings = relationship('User', secondary=follow_map, backref=backref('followers', lazy='joined'), lazy='dynamic')
    # block_list = relationship('User', secondary=block_map, backref=backref('block_by_list', lazy='joined'),
    #                           lazy='dynamic')

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email
        }
