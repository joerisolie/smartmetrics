import os,re,sys,subprocess,datetime

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

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

class SmartValueManager(object):
    device = None
    parameters = None
    sqlite_file = None

    def get_values(self):
        process = subprocess.Popen('smartctl -a %s' % self.device, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()
        if proc_stdout[1].strip(): print proc_stdout[1].strip()
        if process.returncode != 0:
            raise OSError('Error %s' % process.returncode)
  
        out = []
        for p in self.parameters:
            for l in proc_stdout[0].strip().split('\n'):
                if p[0] in l:
                    line = [s for s in l.split(" ") if s is not ""]
                    out.append((p[1],int(line[9])))
        return out

    def store_values(self,values):
        print values

        engine = create_engine('sqlite:///%s' % (self.sqlite_file))
        Base.metadata.bind = engine

        cur_date = datetime.datetime.now()
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        for v in values:
            sv = SmartValue()
            sv.date = str(cur_date.isoformat())
            sv.device = self.device
            sv.smartid = v[0]
            sv.smartvalue = v[1]
            session.add(sv)

        session.commit()

    def create_db(self):
        engine = create_engine('sqlite:///%s' % (self.sqlite_file))
        Base.metadata.create_all(engine)

if __name__ == '__main__':
    if sys.argv[1]:
        svf = SmartValueManager()
        svf.sqlite_file = './smartdb.sqlite'
        if sys.argv[1] == 'createdb':
             svf.create_db()
        else:
             svf.device = sys.argv[1]
             svf.parameters = [('5 Reallocated_Sector_Ct',5,'Reallocated Sector Count'), 
                          ('171 Unknown_Attribute',171,'Program Fail Count'), 
                          ('172 Unknown_Attribute',172,'Erase Fail Count'), 
                          ('173 Unknown_Attribute',173,'Average Block-Erase Count'), 
                          ('180 Unused_Rsvd_Blk_Cnt_Tot',180,'Unused Reserved NAND Blocks'), 
                          ('194 Temperature_Celsius',194,'Enclosure Temperature'), 
                          ('196 Reallocated_Event_Count',196,'Reallocation Event Count'), 
                          ('202 Unknown_SSD_Attribute',202,'Percent Lifetime Remaining'), 
                          ('247 Unknown_Attribute',247,'Host Program NAND Pages Count'), 
                          ('248 Unknown_Attribute',248,'FTL Program NAND Pages Count')
                          ]
             vals = svf.get_values()
             print vals
             svf.store_values(vals)

