import responder
import time

api = responder.API(
    allowed_hosts=["*"],  # set allowed hosts
    secret_key='test',  # set secret_key
    # enable_hsts=True, # redirect http to https
)

# define pre-response process
@api.route(before_request=True)
def prepare_response(req, resp):
    resp.headers["X-Pizza"] = "42"


# standard api
@api.route("/")
def hello_world(req, resp):
    resp.text = "hello world!"


# get key parameter
@api.route("/route/{who}")
def hello_world_key(req, resp, *args, who):
    resp.text = f"hello world, {who}!"


# get query parameter
@api.route("/query/")
def hello_world_query(req, resp, *args, **kwargs):
    re = req.params.get("id")
    resp.text = f"hello world, {re}!"


# returning json
@api.route("/{who}/json")
def hello_world_json(req, resp, *args, who):
    resp.media = {"text": who}
    resp.status_code = api.status_codes.HTTP_200


# returning html template
@api.route("/temp/{who}/html")
def hello_world_temp(req, resp, *args, who):
    """
    template: /templates/
    """
    resp.content = api.template("hello.html", who=who)


# process depending on method type
# get request post data
@api.route("/post")
async def get_data(req, resp):
    if req.method == "get":
        resp.text = 'GET method is required.'
        return
    elif req.method == "post":
        data = await req.media()
        resp.media = dict(**data)
        return


# get form data
@api.route("/form")
async def get_form(req, resp):
    if req.method == "post":
        # media method is async function
        # must use await to get post data.
        data = await req.media()

        items = {
            "req": data.get("name"),
            "name": data.get("name"),
        }
        resp.content = api.template("form.html", items=items)


# background task
@api.route("/background")
async def backgroundtask(req, resp):
    """
    implement of background task by @api.background.task decorator.
    return response before finishing process function in this view
    """

    @api.background.task
    def process(data):
        time.sleep(3)
        print(f"saved! {data}")

    data = await req.media()

    process(data)

    resp.media = {"success": True}


if __name__ == "__main__":
    api.run()
