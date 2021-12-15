from sqlalchemy import Column, Integer, String
from Instaloader.database import BASE, SESSION


class Users(BASE):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    user_id = Column(Integer, primary_key=True)
    insta_username = Column(String)
    insta_password = Column(String)

    def __init__(self, user_id, insta_username=None, insta_password=None):
        self.user_id = user_id
        self.insta_username = insta_username
        self.insta_password = insta_password


Users.__table__.create(checkfirst=True)


async def num_users():
    try:
        return SESSION.query(Users).count()
    finally:
        SESSION.close()


async def set_info(user_id, username, password):
    q = SESSION.query(Users).get(user_id)
    if q:
        q.insta_username = username
        q.insta_password = password
    else:
        SESSION.add(Users(user_id, username, password))
    SESSION.commit()


async def get_info(user_id):
    q: Users = SESSION.query(Users).get(user_id)
    if q and q.insta_password:
        info = q.insta_username, q.insta_password
        SESSION.close()
        return info
    else:
        SESSION.add(Users(user_id))
        SESSION.commit()
        return None, None
