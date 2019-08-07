import responder


api = responder.API()

@api.route("/")
async def hello(req, resp):
    resp.media = {"text": "Hello python!"}


if __name__ == "__main__":
    api.run(debug=False)
