import main
import pytest


@pytest.fixture
def api():
    return main.api


def test_login(api):
    @api.route("/main")
    def main_view(req, resp):
        assert req.session.get('User') == 'test'
        resp.session['User'] = ''

    @api.route("/some_url/{user}")
    def some_view(req, resp, user):
        resp.session['User'] = user
        api.redirect(resp, '/main')

    api.requests.get(url='some_url/test')


def test_login_with_slash(api):

    @api.route("/main2")
    def main_view2(req, resp):
        assert req.session.get('User') == 'test'
        resp.session['User'] = ''

    @api.route("/slash_url/{user}/")
    def slash_view(req, resp, user):
        resp.session['User'] = user
        api.redirect(resp, '/main2')

    api.requests.get(url='slash_url/test/')
