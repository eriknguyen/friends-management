import sqlalchemy as db
from sqlalchemy.orm import relationship, backref
from . import Model

friend_map = db.Table(
    'friend_map',
    Model.metadata,
    db.Column('user1_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('user2_id', db.Integer, db.ForeignKey('user.id'))
)

subscribe_map = db.Table(
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
    email = db.Column(db.String(200), nullable=False, unique=True)

    friends = relationship(
        'User', secondary=friend_map,
        primaryjoin=(friend_map.c.user1_id == id),
        secondaryjoin=(friend_map.c.user2_id == id),
        lazy='dynamic')

    subscribings = relationship(
        'User', secondary=subscribe_map,
        primaryjoin=(subscribe_map.c.subscriber_id == id),
        secondaryjoin=(subscribe_map.c.target_id == id),
        backref=backref('subscribers', lazy='dynamic'), lazy='dynamic')

    blockings = relationship(
        'User', secondary=block_map,
        primaryjoin=(block_map.c.blocker_id == id),
        secondaryjoin=(block_map.c.target_id == id),
        backref=backref('blockeds', lazy='dynamic'),
        lazy='dynamic'
    )

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email
        }
