from pyramid.config import Configurator
from .models import (
    DB,
    Post,
    Comment,
    )


def _init_db():
    p = Post('My first blogpost', 'Administrator')
    DB.save(p)
    c1 = Comment('Great post!', 'Paul E.', post_id=p.id)
    c2 = Comment(
        'Well written but I disagree with your conclusion.',
        'Max M.',
        post_id=p.id
        )
    DB.save(c1)
    DB.save(c2)
    p.comment_ids = [c1.id, c2.id]
    DB.save(p)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('post', '/post')
    config.add_route('search', '/search')
    config.add_route('search_raw', '/search_raw')
    config.scan()
    _init_db()
    return config.make_wsgi_app()
