from flask import Flask, request
import boto3
import os
import json

app = Flask(__name__)

session = boto3.Session(
    aws_access_key_id=os.environ.get('ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('SECRET_KEY'),
    region_name=os.environ.get('REGION_NAME')
)

dynamodb = session.resource('dynamodb', endpoint_url="http://dynamodb.eu-central-1.amazonaws.com")

table = dynamodb.Table('Books')

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/insert/', methods=['POST'])
def insert_book():
    response = table.put_item(
        Item={
            'title': request.json['title'],
            'author': request.json['author'],
            'year': request.json['year']
        }
    )
    return request.data


@app.route('/get/', methods=['GET'])
def get_books():
    response = table.scan()
    data = response['Items']
    return json.dumps(data)


@app.route('/get/<title>', methods=['GET'])
def get_book(title):
    return table.get_item(Key={'title': title})['Item']


@app.route('/delete/<title>', methods=['DELETE'])
def delete_book(title):
    response = table.delete_item(
        Key={
            'title': title
        }
    )
    return response


@app.route('/update/', methods=['PATCH'])
def update_book():
    response = table.update_item(
        Key={
            'title': request.json['title']
        },
        UpdateExpression="set author=:a",
        ExpressionAttributeValues={
            ':a': request.json['author']
        }
    )
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0")
