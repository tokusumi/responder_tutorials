import responder
from logging import config, getLogger
from .settings import LOGGER_CONF

api = responder.API()

config.dictConfig(LOGGER_CONF)
logger = getLogger("logger")


# logging to file(it depends on LOGGER_CONF in settings.py)
@api.route("/logger/")
def logger_view(req, resp):
    logger.info("logger success")
    resp.text = "check logger file!"


if __name__ == "__main__":
    api.run()
