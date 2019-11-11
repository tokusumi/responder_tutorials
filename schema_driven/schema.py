from marshmallow import Schema, fields
import datetime


# @api.schema("IdReqSchema")
class IdReqSchema(Schema):
    # def of request schema
    # if required=True, the field must exist
    id = fields.Int(required=True)


# @api.schema("ErrorRespSchema")
class ErrorRespSchema(Schema):
    # you can define response schema, as well
    error = fields.Str()
    errorDate = fields.Date()


class ErrorModel():
    """error response class"""

    def __init__(self, error):
        self.error = str(error)
        self.errorDate = datetime.datetime.now()


# @api.schema("IsExistRespSchema")
class IsExistRespSchema(Schema):
    is_exist = fields.Bool()


class IsExistIDModel():
    def __init__(self, data):
        id = data.get('id')
        self.is_exist = id in [1, 2, 3, 4, 5]


# @api.schema("AllIdRespSchema")
class AllIdRespSchema(Schema):
    exist_ids = fields.List(fields.Int())


class AllExistIDModel():
    def __init__(self):
        self.exist_ids = [1, 2, 3, 4, 5]
