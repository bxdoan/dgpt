from wsgiref import simple_server
import falcon

from src.api.chat_resourse import Chat
from src.api.healthcheck import HealthCheckResource, VersionResource
from src.config import APP_PORT


app = falcon.App()
app.add_route('/api/v1/healthcheck', HealthCheckResource())
app.add_route('/api/v1/versions/current', VersionResource())
app.add_route('/api/v1/chat', Chat())

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', APP_PORT, app)
    httpd.serve_forever()
