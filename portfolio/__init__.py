''' Flask controller'''
from flask import Flask, render_template
from portfolio.common.mongo import Mongo

# Import a module / component using its Blueprint handler variable (index_mod)
from portfolio.index_mod.controllers import index_mod as index_module
from portfolio.auth_mod.controllers import auth_mod as authentication_module

app = Flask(__name__)

# External configuration file
app.config.from_object('config')

## setup db here
@app.before_first_request
def init_database():
    Mongo.init()

# Register Blueprints
app.register_blueprint(index_module)
app.register_blueprint(authentication_module)


# setup 404 handler
@app.errorhandler(404)
def not_found(error):
    '''Doc String'''
    error_str = str(error.code) + " : Sorry will be up shortly"
    return render_template('404.html', error=error_str), 404


if __name__ == '__main__':
    app.run()
    