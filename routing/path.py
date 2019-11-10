from .views import routing_view
import responder


api = responder.API()

# path check
@api.route("/check/{path}")
def checking(req, resp, path):
    url = api.path_matches_route('/' + path)
    resp.text = f'{url}'

# convert function name to url
@api.route('/check_func/{name}')
def check_func(req, resp, name):
    try:
        url = api.url_for(name)
    except (KeyError, ValueError):
        # KeyError when endpoint includes path parameter
        # ValueError when name includes slash
        url = None
    resp.text = f'{url}'


# define default view
# call the following funciton if any url patterns are not matched
@api.route('/', default=True)
def default_view(req, resp):
    resp.text = "this endpoint does not exist"


# add route by the other way than decorator
# routing_view is defined in routing/views.py
api.add_route('/add/post', routing_view)


# redirect
@api.route('/redirect')
def redirect(req, resp):
    # both is available
    # api.redirect(resp, '/')
    resp.redirect('/')


# static
# default = True
# endpointを指定しないとstatic modeになる
# default = Trueなので
# view(endpoint)をpathをいれなければstatic / index.htmlを返す
# fileが存在しなければnot foundと表示

if __name__ == "__main__":
    api.run()
