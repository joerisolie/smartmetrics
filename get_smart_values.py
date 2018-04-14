import os,re,sys,subprocess,datetime

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class DBManager():
    sqlite_file = None
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


class SmartValueCrucial(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    date = Column(String(20), nullable=False)
    device = Column(String(10), nullable=False)
    rsc = Column(Integer)
    pfc = Column(Integer)
    efc = Column(Integer)
    abec = Column(Integer)
    urnb = Column(Integer)
    et = Column(Integer)
    rec = Column(Integer)
    plr = Column(Integer)
    hpnpc = Column(Integer)
    fpnpc = Column(Integer)


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


class SmartValueManagerCrucial(object):
    device = None
    parameters = None

    def get_values(self):
        process = subprocess.Popen('/usr/sbin/smartctl -a %s' % self.device, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()
        if proc_stdout[1].strip(): print proc_stdout[1].strip()
        if process.returncode != 0:
            raise OSError('Error %s' % process.returncode)
  
        out = SmartValueCrucial()
        out.date = datetime.datetime.now()
        out.device = self.device
        for p in self.parameters:
            for l in proc_stdout[0].strip().split('\n'):
                if p[0] in l:
                    line = [s for s in l.split(" ") if s is not ""]
                    if p[1] == 5: out.rsc = int(line[9])
                    elif p[1] == 171: out.pfc = int(line[9])
                    elif p[1] == 172: out.efc = int(line[9])
                    elif p[1] == 173: out.abec = int(line[9])
                    elif p[1] == 180: out.urnb = int(line[9])
                    elif p[1] == 194: out.et = int(line[9])
                    elif p[1] == 196: out.rec = int(line[9])
                    elif p[1] == 202: out.plr = int(line[9])
                    elif p[1] == 247: out.hpnpc = int(line[9])
                    elif p[1] == 248: out.fpnpc = int(line[9])
        return out


class SmartValueManagerSamsung(object):
    device = None
    parameters = None

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


if __name__ == '__main__':
    if sys.argv[1]:
        dbm = DBManager()
        dbm.sqlite_file = './smartdb.sqlite'
        if sys.argv[1] == 'createdb':
            dbm.create_db()
        else:
            svf = None
            val = None
            if sys.argv[2] == 'samsung':
                svf = SmartValueManagerSamsung()
                svf.device = sys.argv[1]
                svf.parameters = [('5 Reallocated_Sector_Ct', 5, 'Reallocated Sector Count', 'rsc'),
                                  ('181 Program_Fail_Cnt_Total', 181, 'Program Fail Count', 'pfc'),
                                  ('182 Erase_Fail_Count_Total', 182, 'Erase Fail Count', 'efc'),
                                  ('179 Used_Rsvd_Blk_Cnt_Tot', 179, 'Used Reserved Blocks Total', 'urbct'),
                                  ('194 Temperature_Celsius', 194, 'Enclosure Temperature', 'et'),
                                  ('183 Runtime_Bad_Block', 183, 'Runtime Bad Block Count', 'rbb'),
                                  ('177 Wear_Leveling_Count', 177, 'Percent Wear Level', 'wlc'),
                                  ('241 Total_LBAs_Written', 241, 'Total LBAs Written', 'tlw')
                                  ]
            else:
                svf = SmartValueManagerCrucial()
                svf.device = sys.argv[1]
                svf.parameters = [('5 Reallocated_Sector_Ct', 5, 'Reallocated Sector Count', 'rsc'),
                                  ('171 Unknown_Attribute', 171, 'Program Fail Count', 'pfc'),
                                  ('172 Unknown_Attribute', 172, 'Erase Fail Count', 'efc'),
                                  ('173 Unknown_Attribute', 173, 'Average Block-Erase Count', 'abec'),
                                  ('180 Unused_Rsvd_Blk_Cnt_Tot', 180, 'Unused Reserved NAND Blocks', 'urnb'),
                                  ('194 Temperature_Celsius', 194, 'Enclosure Temperature', 'et'),
                                  ('196 Reallocated_Event_Count', 196, 'Reallocation Event Count', 'rec'),
                                  ('202 Unknown_SSD_Attribute', 202, 'Percent Lifetime Remaining', 'plr'),
                                  ('247 Unknown_Attribute', 247, 'Host Program NAND Pages Count', 'hpnpc'),
                                  ('248 Unknown_Attribute', 248, 'FTL Program NAND Pages Count', 'fpnpc')
                                  ]
            val = svf.get_values()
            print val
            dbm.store_values(val)