# -*- coding: utf-8 -*-
from flask import Flask, render_template
from sqlalchemy.ext.declarative import Base, SmartValue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':
    app = Flask(__name__)

    @app.route('/')
    @app.route('/index')
    def hello_world():
        engine = create_engine('sqlite:///./smartdb.sqlite')
        Base.metadata.bind = engine
        DBSession = sessionmaker()
        DBSession.bind = engine
        session = DBSession()
        data = session.query(SmartValue).all()

        return render_template('index.html', title='LVS Config', data=data)

    app.run(host='0.0.0.0', debug=True)

