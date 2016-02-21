from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/home.pt')
def my_view(request):
    return {}


@view_config(route_name='search', renderer='templates/search.pt')
def search(request):
    return {'query': request.params.get('q', '')}
    # http://localhost:6543/search?q=%3Cscript%3Ealert(123)%3C/script%3E
    # chromium-browser --temp-profile --disable-xss-auditor
