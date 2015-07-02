from flask import Flask
app = Flask(__name__)


@app.route('/')
def main():
    return "Python Instagram Analyzer"

if __name__ == '__main__':
    app.run()