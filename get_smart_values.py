import re,sys,subprocess
import sqlite3

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

    def store_values(self):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()
        table_name = 'smart_values'
id_column = 'my_1st_column'
column_name = 'my_2nd_column'


# A) Inserts an ID with a specific value in a second column
        try:
             c.execute("INSERT INTO {tn} (id, date, device, smartid, smartvalue) VALUES ({id}, {date}, {dev}, {sid}, {sval})". format(tn=table_name, idf=id_column, cn=column_name))
        except sqlite3.IntegrityError:
             print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))

        # B) Tries to insert an ID (if it does not exist yets
        # with a specific value in a second column
        c.execute("INSERT OR IGNORE INTO {tn} ({idf}, {cn}) VALUES (123456, 'test')".\
                        format(tn=table_name, idf=id_column, cn=column_name))

        # C) Updates the newly inserted or pre-existing entry            
        c.execute("UPDATE {tn} SET {cn}=('Hi World') WHERE {idf}=(123456)".\
                        format(tn=table_name, cn=column_name, idf=id_column))

        conn.commit()
        conn.close()
        conn.close()

    def create_db(self):
        table_name = 'smart_values'  # name of the table to be created
        id_field = 'id'
        id_field_type = 'INTEGER'
        date_field = 'date' # name of the column
        date_field_type = 'STRING'
        device_field = 'device'
        device_field_type = 'STRING'
        smart_id_field = 'smartid'
        smart_id_field_type = 'INTEGER'
        smart_value_field = 'smartvalue'
        smart_value_field_type = 'INTEGER'
        
        # Connecting to the database file
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()

        # Creating a new SQLite table and adding columns
        c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)' .format(tn=table_name, nf=id_field, ft=id_field_type))
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}" .format(tn=table_name, cn=date_field, ct=date_field_type))
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}" .format(tn=table_name, cn=device_field, ct=device_field_type))
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}" .format(tn=table_name, cn=smart_id_field, ct=smart_id_field_type))
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}" .format(tn=table_name, cn=smart_value_field, ct=smart_value_field_type))

        # Committing changes and closing the connection to the database file
        conn.commit()
        conn.close()

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
             print svf.get_values()

