from flask import Flask

app = Flask(__name__)

# Test if the flask connection is running
@app.route('/')
def welcome_test():
    # Test that route is working
    return 'Running on PORT: 5000'