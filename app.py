from src import config, app, session
from src.routes.routes import api

# Routes
app.register_blueprint(api, url_prefix = "/api")

# App Start
if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

session.close()