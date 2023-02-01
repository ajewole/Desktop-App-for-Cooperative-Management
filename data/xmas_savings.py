import sqlite3
import datetime

class Xmas_DB():
    def __init__(self, *args, **kwargs):
        self.connection = sqlite3.connect('fopaj.db')
        self.cursor = self.connection.cursor()
        command = '''CREATE TABLE IF NOT EXISTS xmas_savings(xmas_id INTEGER PRIMARY KEY AUTOINCREMENT, xmasID TEXT NOT NULL, type TEXT NOT NULL, 
                month TEXT NOT NULL, year TEXT NOT NULL, details TEXT NOT NULL, amount FLOAT NOT NULL, interest FLOAT NOT NULL, 
                total_xmas FLOAT NOT NULL, date_created DATE NOT NULL, date_last_modified DATE NOT NULL, member_id INTEGER, FOREIGN KEY (member_id) 
                REFERENCES members (member_id) ON UPDATE CASCADE ON DELETE CASCADE)'''
        self.cursor.execute(command)     

    def add_xmas_saving(self, xmas_saving):
        self.cursor.execute('INSERT INTO xmas_savings VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', xmas_saving)
        self.connection.commit()
        # self.connection.close()
        # print(xmas_saving)
    
    def get_xmas_saving(self, id):
        command = "SELECT * FROM xmas_savings WHERE xmas_id=?"
        self.cursor.execute(command, id)
        result = self.cursor.fetchall()
        if len(result) <=0:
            return []
        else:
            xmas = result[0]
            xmas_saving = {'xmas_id': xmas[0], 'xmasID': xmas[1], 'type': xmas[2], 'month': xmas[3], 'year': xmas[4], \
                    'details': xmas[5], 'amount': xmas[6], 'interest': xmas[7], 'total_xmas': xmas[8], \
                    'date_created': xmas[9], 'date_last_modified': xmas[10], 'member_id': xmas[11]}
            return xmas_saving

    def get_member_xmas_savings(self, id):
        command = "SELECT * FROM xmas_savings WHERE member_id=? ORDER BY xmas_id DESC"
        self.cursor.execute(command, id)
        results = self.cursor.fetchall()
        if len(results) <= 0:
            return []
        else: 
            xmas_savings = []
            for xmas in results:
                xmas_saving = {'xmas_id': xmas[0], 'xmasID': xmas[1], 'type': xmas[2], 'month': xmas[3], 'year': xmas[4], \
                    'details': xmas[5], 'amount': xmas[6], 'interest': xmas[7], 'total_xmas': xmas[8],  \
                    'date_created': xmas[9], 'date_last_modified': xmas[10], 'member_id': xmas[11]}
                xmas_savings.append(xmas_saving)
            return xmas_savings

    def get_all_xmas_savings(self):
        command = "SELECT * FROM xmas_savings ORDER BY xmas_id DESC"
        # command = "SELECT * FROM xmas_savings ORDER BY id DESC"
        self.cursor.execute(command)
        results = self.cursor.fetchall()
        if len(results) <= 0:
            return []
        else: 
            xmas_savings = []
            for xmas in results:
                xmas_saving = {'xmas_id': xmas[0], 'xmasID': xmas[1], 'type': xmas[2], 'month': xmas[3], 'year': xmas[4], \
                    'details': xmas[5], 'amount': xmas[6], 'interest': xmas[7], 'total_xmas': xmas[8], \
                    'date_created': xmas[9], 'date_last_modified': xmas[10], 'member_id': xmas[11]}
                xmas_savings.append(xmas_saving)
            return xmas_savings

    
    def update_xmas_saving(self, xmas_saving):
        command = '''UPDATE xmas_savings SET xmasID=?, type=?, month=?, year=?, details=?, amount=?, interest=?, 
        total_xmas=?, date_created=?, date_last_modified=?, member_id=? WHERE xmas_id=?'''
        self.cursor.execute(command, xmas_saving)
        self.connection.commit()
        # self.connection.close()  
    
    def remove_xmas_saving(self, id):
        command = "DELETE FROM xmas_savings WHERE xmas_id=?"
        self.cursor.execute(command, id)
        self.connection.commit()
        # self.connection.close()
    
    def get_editable_xmass(self, params):
        # command = "SELECT * FROM xmas_savings WHERE xmas_id > ? AND member_id = ? ORDER BY xmas_id DESC"
        command = "SELECT * FROM xmas_savings WHERE xmas_id > ? AND member_id = ?"
        self.cursor.execute(command, params)
        results = self.cursor.fetchall()
        if len(results) <= 0:
            return []
        else: 
            xmas_savings = []
            for xmas in results:
                xmas_saving = {'xmas_id': xmas[0], 'xmasID': xmas[1], 'type': xmas[2], 'month': xmas[3], 'year': xmas[4], \
                    'details': xmas[5], 'amount': xmas[6], 'interest': xmas[7], 'total_xmas': xmas[8], \
                    'date_created': xmas[9], 'date_last_modified': xmas[10], 'member_id': xmas[11]}
                xmas_savings.append(xmas_saving)
            return xmas_savings
    
# db = Monthly_DB()
# today = datetime.date.today()
# date_created = today.strftime("%d/%m/%Y")
# date_last_modified = date_created
# xmas = ('TRANS234', 'Monthly Savings', 'July', '2022', 'Monthly Savings for the month of July, 2022', '30000.00', \
#             '200.00', '300000.00', '12000.00', date_created, date_last_modified, 'FOPAJ1473')

# results = db.add_xmas_saving(xmas)
# results = db.get_xmas_saving(('FOPAJ1473',))
# results = db.get_xmas_savings()

# print(results)