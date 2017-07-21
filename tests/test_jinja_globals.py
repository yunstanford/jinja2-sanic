from sanic import Sanic
from sanic.views import HTTPMethodView
import jinja2_sanic
import jinja2


async def test_get_env(test_client):
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
    env = jinja2_sanic.get_env(app)
    assert isinstance(env, jinja2.Environment)
    # consistent
    assert env is jinja2_sanic.get_env(app)
