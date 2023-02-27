from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from ariadne.constants import PLAYGROUND_HTML
from ariadne import graphql_sync, make_executable_schema

from app.models.User import User
from app.models import db
# Make sure to declare Models before instantiating Schemas. Otherwise sqlalchemy.orm.configure_mappers() will run too soon and fail. https://pypi.org/project/marshmallow-sqlalchemy/
from .views import all_views

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
CORS(app)
migrate = Migrate(app, db)

from .graphql import query, type_defs, mutation
from app.serializers import ma

ma.init_app(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

app.register_blueprint(all_views, url_prefix="/api/v1")

schema = make_executable_schema(type_defs, [query, mutation])


@app.route("/api/v1/graphql", methods=["GET"])
def graphql_playground():
    '''
    Create a GraphQL Playground UI for the GraphQL schema
    '''
    # Playground accepts GET requests only.
    # If you wanted to support POST you'd have to
    # change the method to POST and set the content
    # type header to application/graphql
    return PLAYGROUND_HTML


@app.route("/api/v1/graphql", methods=["POST"])
def graphql_server():
    '''
    GraphQL endpoint for executing GraphQL queries
    '''
    data = request.get_json()
    success, result = graphql_sync(
        schema, data, context_value={"request": request})
    status_code = 200 if success else 400
    return jsonify(result), status_code


'''
Comandos flask cli
'''


@app.cli.command("seed")
def seed():
    """Seed the database."""
    user_1 = User(username="medico", password="senha@123".encode('utf-8'))
    db.session.add(user_1)
    db.session.commit()
    print(user_1)
