.. jinja2-sanic documentation master file, created by
   sphinx-quickstart on Thu Jul 20 17:19:48 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

jinja2-sanic
============

.. image:: https://travis-ci.org/yunstanford/jinja2-sanic.svg?branch=master
    :alt: build status
    :target: https://travis-ci.org/yunstanford/jinja2-sanic

.. image:: https://coveralls.io/repos/github/yunstanford/jinja2-sanic/badge.svg?branch=master
    :alt: coverage status
    :target: https://coveralls.io/github/yunstanford/jinja2-sanic?branch=master


a jinja2 template renderer for Sanic. It supports:

* function based web handlers
* class-based views
* decoractors for convenient useage


-----------
Quick start
-----------

Let's get started.

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


Contents:

.. toctree::
   :maxdepth: 2

   installation
   examples
   globals
   references


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

