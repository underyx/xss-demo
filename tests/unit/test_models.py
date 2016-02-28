import pytest


def test_save_post_sets_id():
    from xss_demo.models import (
        DB,
        Post,
        )

    post = Post('Just some text')
    assert post.id is None
    DB.save(post)
    assert post.id is not None


def test_get_post_returns_same_data():
    from xss_demo.models import (
        DB,
        Post,
        )

    post = Post('Just some text')
    DB.save(post)
    post2 = DB.get(Post, post.id)
    assert post is not post2  # different objects
    assert post.__dict__ == post2.__dict__


def test_get_post_invalid_id():
    from xss_demo.models import (
        DB,
        Post,
        )

    with pytest.raises(ValueError):
        DB.get(Post, 99)


def test_save_existing_post_writes_data():
    from xss_demo.models import (
        DB,
        Post,
        )

    post = Post('Just some text')
    DB.save(post)
    original_id = post.id
    post.content = 'Modified text'
    DB.save(post)
    assert post.id == original_id
    assert DB.get(Post, original_id).content == 'Modified text'


def test_save_post_invalid_id():
    from xss_demo.models import (
        DB,
        Post,
        )

    post = Post('Just some text')
    post.id = 99
    with pytest.raises(ValueError):
        DB.save(post)


def test_delete_post():
    from xss_demo.models import (
        DB,
        Post,
        )

    post = Post('Just some text')
    DB.save(post)
    original_id = post.id
    DB.delete(post)
    assert DB._db['posts'][original_id] is None
    assert post.id is None


def test_cant_get_deleted_post():
    from xss_demo.models import (
        DB,
        Post,
        )

    post = Post('Just some text')
    DB.save(post)
    original_id = post.id
    DB.delete(post)

    with pytest.raises(ValueError):
        DB.get(Post, original_id)
