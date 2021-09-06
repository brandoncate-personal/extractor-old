from flask import Flask, request, abort
from flask_restful import Resource, Api
from marshmallow import Schema, fields

from handlers.extractor import extract


class ExtractorQuerySchema(Schema):
    repo = fields.Str(required=True)


app = Flask(__name__)
api = Api(app)
schema = ExtractorQuerySchema()


class ExtractorHandler(Resource):
    def get(self):
        errors = schema.validate(request.args)
        if errors:
            abort(400, str(errors))

        results = schema.load(request.args)

        return extract(results['repo'])


api.add_resource(ExtractorHandler, '/extract')

# omit of you intend to use `flask run` command
if __name__ == '__main__':
    app.run(debug=False)
