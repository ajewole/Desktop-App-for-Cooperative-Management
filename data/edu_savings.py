import sqlite3
import datetime

class Edu_DB():
    def __init__(self, *args, **kwargs):
        self.connection = sqlite3.connect('fopaj.db')
        self.cursor = self.connection.cursor()
        command = '''CREATE TABLE IF NOT EXISTS edu_savings(edu_id INTEGER PRIMARY KEY AUTOINCREMENT, eduID TEXT NOT NULL, type TEXT NOT NULL, 
                month TEXT NOT NULL, year TEXT NOT NULL, details TEXT NOT NULL, amount FLOAT NOT NULL, interest FLOAT NOT NULL, 
                total_edu FLOAT NOT NULL, date_created DATE NOT NULL, date_last_modified DATE NOT NULL, member_id INTEGER, FOREIGN KEY (member_id) 
                REFERENCES members (member_id) ON UPDATE CASCADE ON DELETE CASCADE)'''
        self.cursor.execute(command)     

    def add_edu_saving(self, edu_saving):
        self.cursor.execute('INSERT INTO edu_savings VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', edu_saving)
        self.connection.commit()
        # self.connection.close()
        # print(edu_saving)
    
    def get_edu_saving(self, id):
        command = "SELECT * FROM edu_savings WHERE edu_id=?"
        self.cursor.execute(command, id)
        result = self.cursor.fetchall()
        if len(result) <=0:
            return []
        else:
            edu = result[0]
            edu_saving = {'edu_id': edu[0], 'eduID': edu[1], 'type': edu[2], 'month': edu[3], 'year': edu[4], \
                    'details': edu[5], 'amount': edu[6], 'interest': edu[7], 'total_edu': edu[8], \
                    'date_created': edu[9], 'date_last_modified': edu[10], 'member_id': edu[11]}
            return edu_saving

    def get_member_edu_savings(self, id):
        command = "SELECT * FROM edu_savings WHERE member_id=? ORDER BY edu_id DESC"
        self.cursor.execute(command, id)
        results = self.cursor.fetchall()
        if len(results) <= 0:
            return []
        else: 
            edu_savings = []
            for edu in results:
                edu_saving = {'edu_id': edu[0], 'eduID': edu[1], 'type': edu[2], 'month': edu[3], 'year': edu[4], \
                    'details': edu[5], 'amount': edu[6], 'interest': edu[7], 'total_edu': edu[8],  \
                    'date_created': edu[9], 'date_last_modified': edu[10], 'member_id': edu[11]}
                edu_savings.append(edu_saving)
            return edu_savings

    def get_all_edu_savings(self):
        command = "SELECT * FROM edu_savings ORDER BY edu_id DESC"
        # command = "SELECT * FROM edu_savings ORDER BY id DESC"
        self.cursor.execute(command)
        results = self.cursor.fetchall()
        if len(results) <= 0:
            return []
        else: 
            edu_savings = []
            for edu in results:
                edu_saving = {'edu_id': edu[0], 'eduID': edu[1], 'type': edu[2], 'month': edu[3], 'year': edu[4], \
                    'details': edu[5], 'amount': edu[6], 'interest': edu[7], 'total_edu': edu[8], \
                    'date_created': edu[9], 'date_last_modified': edu[10], 'member_id': edu[11]}
                edu_savings.append(edu_saving)
            return edu_savings

    
    def update_edu_saving(self, edu_saving):
        command = '''UPDATE edu_savings SET eduID=?, type=?, month=?, year=?, details=?, amount=?, interest=?, 
        total_edu=?, date_created=?, date_last_modified=?, member_id=? WHERE edu_id=?'''
        self.cursor.execute(command, edu_saving)
        self.connection.commit()
        # self.connection.close()  
    
    def remove_edu_saving(self, id):
        command = "DELETE FROM edu_savings WHERE edu_id=?"
        self.cursor.execute(command, id)
        self.connection.commit()
        # self.connection.close()
    
    def get_editable_edus(self, params):
        # command = "SELECT * FROM edu_savings WHERE edu_id > ? AND member_id = ? ORDER BY edu_id DESC"
        command = "SELECT * FROM edu_savings WHERE edu_id > ? AND member_id = ?"
        self.cursor.execute(command, params)
        results = self.cursor.fetchall()
        if len(results) <= 0:
            return []
        else: 
            edu_savings = []
            for edu in results:
                edu_saving = {'edu_id': edu[0], 'eduID': edu[1], 'type': edu[2], 'month': edu[3], 'year': edu[4], \
                    'details': edu[5], 'amount': edu[6], 'interest': edu[7], 'total_edu': edu[8], \
                    'date_created': edu[9], 'date_last_modified': edu[10], 'member_id': edu[11]}
                edu_savings.append(edu_saving)
            return edu_savings