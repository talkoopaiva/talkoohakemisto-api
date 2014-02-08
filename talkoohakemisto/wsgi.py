import newrelic.agent

from . import Application

app = Application()
app = newrelic.agent.wsgi_application()(app.wsgi_app)
