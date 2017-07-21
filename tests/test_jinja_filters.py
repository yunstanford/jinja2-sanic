from sanic import Sanic
from sanic.views import HTTPMethodView
import jinja2_sanic
import jinja2


async def test_jinja2_filter(test_client):
    app = Sanic("test_jinja2_render")

    # setup
    def simple_func(last_name):
        return "Y.{last_name}".format(last_name=last_name)

    jinja2_sanic.setup(
        app,
        loader=jinja2.DictLoader(
            {
                "templates.jinja2": "{{ 2|simple_func }}"
            }
        ),
        filters={'simple_func': simple_func}
    )

    @app.route("/")
    @jinja2_sanic.template("templates.jinja2")
    async def func(request):
        return {}

    cli = await test_client(app)
    resp = await cli.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert text == "Y.2"