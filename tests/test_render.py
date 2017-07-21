from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.exceptions import ServerError
from sanic import response
import jinja2_sanic
import jinja2
import pytest
from unittest import mock


async def test_render_func(test_client):
    app = Sanic("test_jinja2_render")

    # setup
    template = "<html><body><h1>{{Player}}</h1>{{Category}}</body></html>"
    jinja2_sanic.setup(
        app,
        loader=jinja2.DictLoader(
            {
                "templates.jinja2": template
            }
        )
    )

    @app.route("/")
    @jinja2_sanic.template("templates.jinja2")
    async def func(request):
        return {
            "Player": "CR7",
            "Category": "Soccer",
        }

    cli = await test_client(app)
    resp = await cli.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert text == "<html><body><h1>CR7</h1>Soccer</body></html>"
    

async def test_render_class_view_based(test_client):
    app = Sanic("test_jinja2_render")

    # setup
    template = "<html><body><h1>{{Player}}</h1>{{Category}}</body></html>"
    jinja2_sanic.setup(
        app,
        loader=jinja2.DictLoader(
            {
                "templates.jinja2": template
            }
        )
    )

    class SimpleView(HTTPMethodView):

        @jinja2_sanic.template("templates.jinja2")
        async def get(self, request):
            return {
                "Player": "CR7",
                "Category": "Soccer",
            }

    # register routes
    app.add_route(SimpleView.as_view(), "/")

    cli = await test_client(app)
    resp = await cli.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert text == "<html><body><h1>CR7</h1>Soccer</body></html>"


async def test_render_func_convert_to_coroutine(test_client):
    app = Sanic("test_jinja2_render")

    # setup
    template = "<html><body><h1>{{Player}}</h1>{{Category}}</body></html>"
    jinja2_sanic.setup(
        app,
        loader=jinja2.DictLoader(
            {
                "templates.jinja2": template
            }
        )
    )

    @app.route("/")
    @jinja2_sanic.template("templates.jinja2")
    def func(request):
        return {
            "Player": "CR7",
            "Category": "Soccer",
        }

    cli = await test_client(app)
    resp = await cli.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert text == "<html><body><h1>CR7</h1>Soccer</body></html>"


async def test_render_not_initialize_jinja_env():
    app = Sanic("test_jinja2_render")

    @app.route("/")
    @jinja2_sanic.template("templates.jinja2")
    def func(request):
        return {
            "Player": "CR7",
            "Category": "Soccer",
        }

    request = mock.Mock()
    request.app = app

    with pytest.raises(ServerError) as ctx:
        await func(request)

    assert str(ctx.value) == "Template engine has not been initialized yet."


async def test_render_template_missing():
    app = Sanic("test_jinja2_render")

    # setup
    template = "<html><body><h1>{{Player}}</h1>{{Category}}</body></html>"
    jinja2_sanic.setup(
        app,
        loader=jinja2.DictLoader(
            {
                "templates.jinja2": template
            }
        )
    )

    @app.route("/")
    @jinja2_sanic.template("templates.jinja3")
    def func(request):
        return {
            "Player": "CR7",
            "Category": "Soccer",
        }

    request = mock.Mock()
    request.app = app

    with pytest.raises(ServerError) as ctx:
        await func(request)

    assert str(ctx.value) == "Template 'templates.jinja3' not found"


async def test_render_func(test_client):
    app = Sanic("test_jinja2_render")

    # setup
    template = "<html><body><h1>{{Player}}</h1>{{Category}}</body></html>"
    jinja2_sanic.setup(
        app,
        loader=jinja2.DictLoader(
            {
                "templates.jinja2": template
            }
        )
    )

    @app.route("/")
    @jinja2_sanic.template("templates.jinja2")
    async def func(request):
        return "CR7"

    request = mock.Mock()
    request.app = app

    with pytest.raises(ServerError) as ctx:
        await func(request)

    assert str(ctx.value) == "context should be mapping, not <class 'str'>"


async def test_render_context_is_None(test_client):
    app = Sanic("test_jinja2_render")

    # setup
    template = "<html><body><h1>{{Player}}</h1>{{Category}}</body></html>"
    jinja2_sanic.setup(
        app,
        loader=jinja2.DictLoader(
            {
                "templates.jinja2": template
            }
        )
    )

    @app.route("/")
    @jinja2_sanic.template("templates.jinja2")
    async def func(request):
        return None

    cli = await test_client(app)
    resp = await cli.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert text == "<html><body><h1></h1></body></html>"


async def test_render_context_is_httpresponse(test_client):
    app = Sanic("test_jinja2_render")

    # setup
    template = "<html><body><h1>{{Player}}</h1>{{Category}}</body></html>"
    jinja2_sanic.setup(
        app,
        loader=jinja2.DictLoader(
            {
                "templates.jinja2": template
            }
        )
    )

    @app.route("/")
    @jinja2_sanic.template("templates.jinja2")
    async def func(request):
        return response.json({
            "Player": "CR7",
            "Category": "Soccer",
        })

    cli = await test_client(app)
    resp = await cli.get('/')
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json == {"Player": "CR7", "Category": "Soccer"}
