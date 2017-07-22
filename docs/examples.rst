=======
Example
=======

A simple example.

.. code-block:: python

    from sanic import Sanic
    from sanic.views import HTTPMethodView
    from sanic.exceptions import ServerError

    app = Sanic("sanic_jinja2_render")

    # Setup jinja2 environment
    template = "<html><body><h1>{{Player}}</h1>{{Category}}</body></html>"
    jinja2_sanic.setup(
        app,
        loader=jinja2.DictLoader(
            {
                "templates.jinja2": template
            }
        )
    )

    # Usage in function based web handlers
    @app.route("/")
    @jinja2_sanic.template("templates.jinja2")
    async def func(request):
        return {
            "Player": "CR7",
            "Category": "Soccer",
        }

    # Usage in class-based views
    class SimpleView(HTTPMethodView):

        @jinja2_sanic.template("templates.jinja2")
        async def get(self, request):
            return {
                "Player": "CR7",
                "Category": "Soccer",
            }

    # register class based view routes
    app.add_route(SimpleView.as_view(), "/")

    # Start Server
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=8000)


If you have more complicated processing, you may wanna use `render_template()` function.

.. code-block:: python

    from sanic import Sanic
    from sanic.views import HTTPMethodView
    from sanic.exceptions import ServerError

    app = Sanic("sanic_jinja2_render")

    # Setup jinja2 environment
    template = "<html><body><h1>{{Player}}</h1>{{Category}}</body></html>"
    jinja2_sanic.setup(
        app,
        loader=jinja2.DictLoader(
            {
                "templates.jinja2": template
            }
        )
    )

    # Usage in function based web handlers
    @app.route("/")
    async def func(request):
        context = {
            "Player": "CR7",
            "Category": "Soccer",
        }
        resp = jinja2_sanic.render_template("templates.jinja2", request, context)

        # Custom Processing
        resp.headers['Access-Control-Allow-Origin'] = '*'

        return resp

    # Usage in class-based views
    class SimpleView(HTTPMethodView):

        async def get(self, request):
            context = {
                "Player": "CR7",
                "Category": "Soccer",
            }
            resp = jinja2_sanic.render_template("templates.jinja2", request, context)

            # Custom Processing
            resp.headers['Access-Control-Allow-Origin'] = '*'

            return resp

    # register class based view routes
    app.add_route(SimpleView.as_view(), "/")

    # Start Server
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=8000)
