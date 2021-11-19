
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd


app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        # read our CSV file
        data = pd.read_csv('C:/Users/Dell/OneDrive/Desktop/users.csv')
        data = data.to_dict()
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=int)
        parser.add_argument('name', required=True, type=str)
        parser.add_argument('city', required=True, type=str)

        args = parser.parse_args()

        # read our CSV file
        data = pd.read_csv('C:/Users/Dell/OneDrive/Desktop/users.csv')

        if args['userId'] in list(data['userId']):
            return {
                       'message': f"'{args['userId']}' already exists."
                   }, 404
        else:

            # adding the newly provided values
            data = data.append({
                'userId': args['userId'],
                'name': args['name'],
                'city': args['city']
            }, ignore_index=True)

            # saving back to CSV file
            data.to_csv('C:/Users/Dell/OneDrive/Desktop/users.csv', index=False)
            return {'data': data.to_dict()}, 200

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=int)
        parser.add_argument('name', store_missing=False)
        parser.add_argument('city', store_missing=False)
        args = parser.parse_args()

        # read our CSV file
        data = pd.read_csv('C:/Users/Dell/OneDrive/Desktop/users.csv')

        # check that the location exists
        if args['userId'] in list(data['userId']):

            # if it exists, we can update it
            user_data = data[data['userId'] == args['userId']]

            # if name has been provided, we update name
            if 'name' in args:
                user_data['name'] = args['name']

            # if city has been provided, we update city
            if 'city' in args:
                user_data['city'] = args['city']

            # update data
            data[data['userId'] == args['userId']] = user_data

            # now save updated data
            data.to_csv('C:/Users/Dell/OneDrive/Desktop/users.csv', index=False)

            return {'data': data.to_dict()}, 200

        else:

            return {
                       'message': f"'{args['locationId']}' location does not exist."
                   }, 404

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=int)

        args = parser.parse_args()

        # read our CSV file
        data = pd.read_csv('C:/Users/Dell/OneDrive/Desktop/users.csv')

        if args['userId'] in list(data['userId']):

            # removing the data entry matching given userId
            data = data[data['userId'] != args['userId']]

            # saving back to CSV file
            data.to_csv('C:/Users/Dell/OneDrive/Desktop/users.csv', index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {
                       'message': f"'{args['userId']}' does not exist."
                   }, 404


api.add_resource(Users, "/users")


if __name__ == "__main__":
    app.run(debug=True)

