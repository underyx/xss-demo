from threading import RLock
from copy import deepcopy


class _DB():
    _db = {
        'posts': [],
        'comments': [],
        }
    _db_lock = RLock()

    def save_post(self, post):
        lock = _DB._db_lock
        db = _DB._db
        with lock:
            if post.id:
                # Make sure entry exists
                self.get_post(post.id)
                db['posts'][post.id] = deepcopy(post.serialize())
            else:
                db['posts'].append(post.serialize())
                post.id = len(db['posts']) - 1 
        return post

    def get_post(self, post_id):
        lock = _DB._db_lock
        db = _DB._db
        with lock:
            try:
                data = db['posts'][post_id]
            except IndexError:
                data = None
            if not data:
                raise ValueError('Invalid ID')
            post = Post.deserialize(deepcopy(data))
            post.id = post_id
            return post

    def delete(self, obj):
        lock = _DB._db_lock
        db = _DB._db
        with lock:
            # Make sure entry exists
            self.get_post(obj.id)
            db['posts'][obj.id] = None
            obj.id = None


DB = _DB()


def now():
    return 123


class Post():
    def __init__(self, content, date=None):
        self.id = None
        self.content = content
        self.date = date if date else now()

    def serialize(self):
        return {
            'content': self.content,
            'date': self.date,
            }

    @staticmethod
    def deserialize(data):
        content = data['content']
        date = data['date']
        return Post(content, date=date)

