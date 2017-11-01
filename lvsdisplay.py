# -*- coding: utf-8 -*-
from flask import Flask, render_template
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from get_smart_values import SmartValue, Base

if __name__ == '__main__':
    app = Flask(__name__)

    @app.route('/')
    @app.route('/index')
    @app.route('/index/<string:device>')
    def index(device='sda'):
        if device != 'sda':
            device = ('/dev/%s' % device,device)
        else:
            device = ('/dev/sda','sda')
        engine = create_engine('sqlite:///./smartdb.sqlite')
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        data = session.query(SmartValue).filter(SmartValue.device == device[0]).all()

        return render_template('index.html', title='Smart Data of %s' % device[1], device=device, data=data)

    app.run(host='0.0.0.0', debug=True)
