import sae
from bulb import wsgi

application = sae.create_wsgi_app(wsgi.application)
