import responder
import time
from logging import config, getLogger
from settings import LOGGER_CONF

api = responder.API()
# api = responder.API(enable_hsts=True)
config.dictConfig(LOGGER_CONF)
logger = getLogger("logger")

# define pre-response proccess
@api.route(before_request=True)
def prepare_response(req, resp):
    resp.headers["X-Pizza"] = "42"


# logging to file(it depends on LOGGER_CONF in settings.py)
@api.route("/logger/")
def logger_view(req, resp):
    logger.info("logger success")
    resp.text = "check logger file!"


@api.route("/")
def hello_world(req, resp):
    resp.text = "hello world!"


@api.route("/{who}")
def hello_world_key(req, resp, *args, who):
    resp.text = "hello world, {}!".format(who)


# get query parameter
@api.route("/query/")
def hello_world_query(req, resp, *args, **kwargs):
    re = req.params.get("id")
    # resp.text = "hello world, {}!".format(re)
    resp.text = re


# returning json
@api.route("/{who}/json")
def hello_world_json(req, resp, *args, who):
    resp.media = {"text": who}
    resp.status_code = api.status_codes.HTTP_200


# returning template
@api.route("/temp/{who}/html")
def hello_world_temp(req, resp, *args, who):
    """
    template: /templates/
    """
    resp.content = api.template("hello.html", who=who)


# get request data
@api.route("/post")
async def get_data(req, resp):

    @api.background.task
    def proccess(data):
        time.sleep(3)
        print("saved!", data)

    data = await req.media()

    proccess(data)
    resp.media = {"success": True}


# get form data
@api.route("/form")
async def get_form(req, resp):
    if req.method == "post":
        data = await req.media()
    else:
        data = {}
    items = {
        "req": data.get("name"),
        "name": data.get("name"),
    }
    resp.content = api.template("form.html", items=items)


if __name__ == "__main__":
    api.run()
