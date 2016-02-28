import pytest


def test_save_post_sets_id():
    from xss_demo.models import (
        DB,
        Post,
        )

    post = Post('Just some text', date=123)
    assert post.id is None
    DB.save_post(post)
    print(post.id)
    assert post.id is not None


def test_get_post_returns_same_data():
    from xss_demo.models import (
        DB,
        Post,
        )

    post = Post('Just some text', date=123)
    DB.save_post(post)
    post2 = DB.get_post(post.id)
    assert post is not post2  # different objects
    assert post.__dict__ == post2.__dict__


def test_get_post_invalid_id():
    from xss_demo.models import DB

    with pytest.raises(ValueError):
        DB.get_post(99)


def test_save_existing_post_writes_data():
    from xss_demo.models import (
        DB,
        Post,
        )

    post = Post('Just some text', date=123)
    DB.save_post(post)
    original_id = post.id
    post.content = 'Modified text'
    DB.save_post(post)
    assert post.id == original_id
    assert DB.get_post(original_id).content == 'Modified text'

def test_save_post_invalid_id():
    from xss_demo.models import (
        DB,
        Post,
        )

    post = Post('Just some text', date=123)
    post.id = 99
    with pytest.raises(ValueError):
        DB.save_post(post)


def test_delete_post():
    from xss_demo.models import (
        DB,
        Post,
        )

    post = Post('Just some text', date=123)
    DB.save_post(post)
    original_id = post.id
    DB.delete(post)
    assert DB._db['posts'][original_id] is None
    assert post.id is None


def test_cant_get_deleted_post():
    from xss_demo.models import (
        DB,
        Post,
        )

    post = Post('Just some text', date=123)
    DB.save_post(post)
    original_id = post.id
    DB.delete(post)

    with pytest.raises(ValueError):
        DB.get_post(original_id)
