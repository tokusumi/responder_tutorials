import main
import pytest


@pytest.fixture
def api():
    return main.api


def test_response(api):
    hello = "hello world"

    @api.route("/some_url")
    def some_view(req, resp):
        resp.text = hello

    r = api.requests.get(url=api.url_for(some_view))
    assert r.text == hello


def test_hello_world(api):
    hello = "hello world!"
    r = api.requests.get(url="/")
    assert r.text == hello


def test_hello_world_key(api):
    who = "Sam"
    r = api.requests.get(url="/{}".format(who))
    assert r.text == "hello world, {}!".format(who)


def test_query_parameter(api):
    ids = "10"
    r = api.requests.get(url="/query/?id={}".format(ids))
    assert r.text == ids


def test_hello_world_json(api):
    who = "Sam"
    r = api.requests.get(url="/{}/json".format(who))
    assert r.json().get('text') == who
