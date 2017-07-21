from sanic import Sanic
from sanic.views import HTTPMethodView
import jinja2_sanic
import jinja2
import asyncio


async def test_render_func(test_client):
    app = Sanic("test_jinja2_render")

    # setup
    template = "foo: {{ foo }}, bar: {{ bar }}, path: {{ request.path }}"
    context_processors = (
        jinja2_sanic.request_processor,
        asyncio.coroutine(
            lambda request: {'foo': 1, 'bar': 3}),
    )
    jinja2_sanic.setup(
        app,
        loader=jinja2.DictLoader(
            {
                "templates.jinja2": template
            }
        ),
        context_processors=context_processors
    )

    @app.route("/")
    @jinja2_sanic.template("templates.jinja2")
    async def func(request):
        return { 'bar': 7 }

    cli = await test_client(app)
    resp = await cli.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert text == "foo: 1, bar: 7, path: /"
