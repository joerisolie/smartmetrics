import os,re,sys,subprocess,datetime

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class SmartValueSamsung(Base):
    __tablename__ = 'samsung'
    id = Column(Integer, primary_key=True)
    date = Column(String(20), nullable=False)
    device = Column(String(10), nullable=False)
    rsc = Column(Integer)
    pfc = Column(Integer)
    efc = Column(Integer)
    urbct = Column(Integer)
    et = Column(Integer)
    rbb = Column(Integer)
    wlc = Column(Integer)
    tlw = Column(Integer)


class SmartValueManagerSamsung(object):
    device = None
    parameters = None
    sqlite_file = None

    def get_values(self):
        process = subprocess.Popen('/usr/sbin/smartctl -a %s' % self.device, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()
        if proc_stdout[1].strip(): print proc_stdout[1].strip()
        if process.returncode != 0:
            raise OSError('Error %s' % process.returncode)
  
        out = SmartValueSamsung()
        out.date = datetime.datetime.now()
        out.device = self.device
        for p in self.parameters:
            for l in proc_stdout[0].strip().split('\n'):
                if p[0] in l:
                    line = [s for s in l.split(" ") if s is not ""]
                    if p[1] == 5: out.rsc = int(line[9])
                    elif p[1] == 181: out.pfc = int(line[9])
                    elif p[1] == 182: out.efc = int(line[9])
                    elif p[1] == 179: out.urbct = int(line[9])
                    elif p[1] == 194: out.et = int(line[9])
                    elif p[1] == 183: out.rbb = int(line[9])
                    elif p[1] == 177: out.wlc = int(line[9])
                    elif p[1] == 241: out.tlw = int(line[9])
        return out

    def store_values(self,value):
        engine = create_engine('sqlite:///%s' % (self.sqlite_file))
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.add(value)
        session.commit()

    def create_db(self):
        engine = create_engine('sqlite:///%s' % (self.sqlite_file))
        Base.metadata.create_all(engine)

if __name__ == '__main__':
    if sys.argv[1]:
        svf = SmartValueManagerSamsung()
        svf.sqlite_file = './smartdb.sqlite'
        if sys.argv[1] == 'createdb':
             svf.create_db()
        else:
             svf.device = sys.argv[1]
             svf.parameters = [('5 Reallocated_Sector_Ct',5,'Reallocated Sector Count','rsc'),
                          ('181 Program_Fail_Cnt_Total',181,'Program Fail Count','pfc'),
                          ('182 Erase_Fail_Count_Total',182,'Erase Fail Count','efc'),
                          ('179 Used_Rsvd_Blk_Cnt_Tot',179,'Used Reserved Blocks Total','urbct'),
                          ('194 Temperature_Celsius',194,'Enclosure Temperature','et'),
                          ('183 Runtime_Bad_Block',183,'Runtime Bad Block Count','rbb'),
                          ('177 Wear_Leveling_Count',177,'Percent Wear Level','wlc'),
                          ('241 Total_LBAs_Written',241,'Total LBAs Written','tlw')
                          ]
             val = svf.get_values()
             print val
             svf.store_values(val)




