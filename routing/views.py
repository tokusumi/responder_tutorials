def routing_view(api):
    """
    demonstrate routing view like django urls.py
    add this view by api.add_route in main.py
    """
    async def _routing_view(req, resp):
        if req.method == "post":
            data = await req.media()
        else:
            data = {}
        items = {
            "req": data.get("name"),
            "name": data.get("name"),
        }
        resp.content = api.template("form.html", items=items)

    return _routing_view
