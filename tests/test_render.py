from sanic import Sanic
from sanic.views import HTTPMethodView
import jinja2_sanic
import jinja2


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
