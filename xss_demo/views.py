from pyramid.view import view_config
from pyramid.request import Response
import html


@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {}


@view_config(route_name='post', renderer='templates/post.pt')
def post(request):
    return {}


@view_config(route_name='search', renderer='templates/search.pt')
def search(request):
    return {'query': request.params.get('q', '')}
    # http://localhost:6543/search?q=%3Cscript%3Ealert(123)%3C/script%3E
    # chromium-browser --temp-profile --disable-xss-auditor


@view_config(route_name='search_raw')
def search_raw(request):
    """
    Search results without template (raw Response() object).
    Templates help escaping characters.
    """
    query = request.params.get('q', '')
    #query = html.escape(query)
    content = """
<html>
    <body>
        <p>Your query is: {0}</p>
    </body>
</html>""".format(query)
    return Response(content)
