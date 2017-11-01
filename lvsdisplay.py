# -*- coding: utf-8 -*-
from flask import Flask, render_template
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class SmartValue(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    date = Column(String(20), nullable=False)
    device = Column(String(10), nullable=False)
    smartid = Column(Integer)
    smartvalue = Column(Integer)

if __name__ == '__main__':
    app = Flask(__name__)

    @app.route('/')
    @app.route('/index')

    def hello_world():
        engine = create_engine('sqlite:///./smartdb.sqlite')
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        data = session.query(SmartValue).all()

        return render_template('index.html', title='LVS Config', data=data)

    app.run(host='0.0.0.0', debug=True)





@app.route('/index/<string:do_refresh>', methods=['GET','POST'])
def index(do_refresh=False):
	check_init_kvs()
	form = MessageForm()