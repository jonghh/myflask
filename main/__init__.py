#EC2 flask 관련 사항:
#https://ndb796.tistory.com/244
#https://medium.com/analytics-vidhya/deploy-a-flask-app-on-amazon-aws-ec2-and-keep-it-running-while-you-are-offline-38d22571e2c5
#https://medium.com/analytics-vidhya/deploy-a-flask-app-on-amazon-aws-ec2-and-keep-it-running-while-you-are-offline-38d22571e2c5


from flask import Flask
from .view import hello, policynews

app = Flask(__name__)

app.register_blueprint(hello.bp)
app.register_blueprint(policynews.bp)