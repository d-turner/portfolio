'''home routes '''
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

# Define the blueprint: 'index', set its url prefix: app.url/
index_mod = Blueprint('index', __name__,
                      template_folder='templates/index')

@index_mod.route('/')
def index():
    '''Index route'''
    return 'Index page'


@index_mod.route('/home/')
def home():
    '''Home route'''
    try:
        return render_template('home.html')
    except TemplateNotFound:
        abort(404)