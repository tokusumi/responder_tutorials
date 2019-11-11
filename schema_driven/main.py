import responder
from marshmallow import ValidationError
from schema import (
    IdReqSchema,
    ErrorRespSchema,
    IsExistRespSchema,
    AllIdRespSchema,
    ErrorModel,
    IsExistIDModel,
    AllExistIDModel
)

api = responder.API(
    openapi='3.0.0',  # OpenAPI version
    docs_route='/docs',  # endpoint for interactive documentation by swagger UI. if None, this is not available.
)

api.schema("IdReqSchema")(IdReqSchema)
api.schema("ErrorRespSchema")(ErrorRespSchema)
api.schema("IsExistRespSchema")(IsExistRespSchema)
api.schema("AllIdRespSchema")(AllIdRespSchema)


@api.route("/schema_driven")
async def schema_driven_view(req, resp):
    """exist id checker endpoint.
    note: tags is not available
    ref:
        https://responder.readthedocs.io/en/latest/tour.html#openapi-schema-support
        https://swagger.io/docs/specification/describing-request-body/
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#requestBodyObject
    ---
    name: is_exest
    get:
        description: Get the all exist id
        responses:
            200:
                description: All exist_id to be returned
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/AllIdRespSchema"
    post:
        description: Check the id exists or not
        requestBody:
            content:
                appliation/json:
                    schema:
                        $ref: "#/components/schemas/IdReqSchema"
        responses:
            200:
                description: true/false whether id exists to be returned
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/IsExistRespSchema"
            400:
                description: validation error
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/ErrorRespSchema"
    """
    if req.method == "get":
        # validate response data
        resp.media = AllIdRespSchema().dump(AllExistIDModel())

    elif req.method == "post":
        request = await req.media()
        try:
            # validate request data using Schema
            # if strict=True, raise ValidationError if exist_id in request data is others type such as int
            data = IdReqSchema().load(request)

        except ValidationError as error:
            # raise ValidationError
            resp.status_code = api.status_codes.HTTP_400
            # use Schema for response
            resp.media = ErrorRespSchema().dump(ErrorModel(error))

            return
        # validate response data
        resp.media = IsExistRespSchema().dump(IsExistIDModel(data))


if __name__ == "__main__":
    """
    access at to get schema.yml
    http:127.0.0.1:5042/schema.yml
    """
    api.run()
