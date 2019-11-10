import responder


api = responder.API(allowed_hosts=["*"], secret_key='test')


@api.route(before_request=True)
def pre_authentication(req, resp):
    """
    authentication: 
    the followings requests is valid,
    - static file
    - login view
    - correct session is equiped

    Others is redirected to login view 
    """
    # pass static file
    if req.url.path.startswith('/static/'):
        return

    # pass login
    elif req.url.path == '/login':
        return

    # pass having valid userid in session
    elif req.session.get('UserId', False) == 'user':
        return

    # login is necessary
    api.redirect(resp, f"/login?next='{req.url.path}'")


@api.route("/login")
async def login_views(req, resp):
    """
    login
    note: error occurs if slash exists at the end of path.
    """
    next_url = req.params.get('next', MAIN_PAGE)
    resp.session['UserId'] = ''

    if req.method == 'get':
        resp.content = api.template('login.html', url='/login')

    elif req.method == 'post':
        data = await req.media()

        user_id = data.get("user_id", "")
        password = data.get("password", "")

        if user_id == USER_ID and password == PASSWORD:
            resp.session['UserId'] = user_id
            api.redirect(resp, next_url)

        resp.content = api.template("login.html", message="IDもしくはPASSWORDを正しく入力してください", url='/login')


@api.route('/main')
async def main_view(req, resp):
    user = req.session.get('UserId', 'Anonymous')
    resp.text = f'hello, {user}'
    resp.session['UserId'] = ''


if __name__ == "__main__":
    USER_ID = 'user'
    PASSWORD = 'pass'
    MAIN_PAGE = '/main'
    api.run(address='0.0.0.0', debug=True)
