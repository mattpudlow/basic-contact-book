from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


class Main:
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)


if __name__ == '__main__':
    main = Main()
    main.app.run(debug=True)

