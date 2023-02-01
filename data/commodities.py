import sqlite3
from collections import OrderedDict
import datetime

class Comm_DB():
    def __init__(self, *args, **kwargs):
        self.connection = sqlite3.connect('fopaj.db')
        self.cursor = self.connection.cursor()
        command = '''CREATE TABLE IF NOT EXISTS commodities(com_id INTEGER PRIMARY KEY AUTOINCREMENT, comID TEXT NOT NULL, type TEXT NOT NULL, 
                month TEXT NOT NULL, year TEXT NOT NULL, details TEXT NOT NULL, amount FLOAT NOT NULL, interest FLOAT NOT NULL, 
                commodity_balance FLOAT NOT NULL, date_created DATE NOT NULL, date_last_modified DATE NOT NULL, member_id INTEGER, FOREIGN KEY (member_id) 
                REFERENCES members (member_id) ON UPDATE CASCADE ON DELETE CASCADE)'''
        self.cursor.execute(command)     

    def add_commodity(self, commodity):
        self.cursor.execute('INSERT INTO commodities VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', commodity)
        self.connection.commit()
        # self.connection.close()
        # print(commodity)
    
    def get_commodity(self, id):
        command = "SELECT * FROM commodities WHERE com_id=?"
        self.cursor.execute(command, id)
        result = self.cursor.fetchall()
        if len(result) <=0:
            return []
        else:
            com = result[0]
            commodity = {'com_id': com[0], 'comID': com[1], 'type': com[2], 'month': com[3], 'year': com[4], \
                    'details': com[5], 'amount': com[6], 'interest': com[7], 'commodity_balance': com[8], \
                    'date_created': com[9], 'date_last_modified': com[10], 'member_id': com[11]}
            return commodity

    def get_member_commodities(self, id):
        command = "SELECT * FROM commodities WHERE member_id=? ORDER BY com_id DESC"
        self.cursor.execute(command, id)
        results = self.cursor.fetchall()
        if len(results) <= 0:
            return []
        else: 
            commodities = []
            for com in results:
                commodity = {'com_id': com[0], 'comID': com[1], 'type': com[2], 'month': com[3], 'year': com[4], \
                    'details': com[5], 'amount': com[6], 'interest': com[7], 'commodity_balance': com[8],  \
                    'date_created': com[9], 'date_last_modified': com[10], 'member_id': com[11]}
                commodities.append(commodity)
            return commodities

    def get_all_commodities(self):
        command = "SELECT * FROM commodities ORDER BY com_id DESC"
        # command = "SELECT * FROM commodities ORDER BY id DESC"
        self.cursor.execute(command)
        results = self.cursor.fetchall()
        if len(results) <= 0:
            return []
        else: 
            commodities = []
            for com in results:
                commodity = {'com_id': com[0], 'comID': com[1], 'type': com[2], 'month': com[3], 'year': com[4], \
                    'details': com[5], 'amount': com[6], 'interest': com[7], 'commodity_balance': com[8], \
                    'date_created': com[9], 'date_last_modified': com[10], 'member_id': com[11]}
                commodities.append(commodity)
            return commodities

    
    def update_commodity(self, commodity):
        command = '''UPDATE commodities SET comID=?, type=?, month=?, year=?, details=?, amount=?, interest=?, 
        commodity_balance=?, date_created=?, date_last_modified=?, member_id=? WHERE com_id=?'''
        self.cursor.execute(command, commodity)
        self.connection.commit()
        # self.connection.close()  
    
    def remove_commodity(self, id):
        command = "DELETE FROM commodities WHERE com_id=?"
        self.cursor.execute(command, id)
        self.connection.commit()
        # self.connection.close()
    
    def get_editable_coms(self, params):
        # command = "SELECT * FROM commodities WHERE com_id > ? AND member_id = ? ORDER BY com_id DESC"
        command = "SELECT * FROM commodities WHERE com_id > ? AND member_id = ?"
        self.cursor.execute(command, params)
        results = self.cursor.fetchall()
        if len(results) <= 0:
            return []
        else: 
            commodities = []
            for com in results:
                commodity = {'com_id': com[0], 'comID': com[1], 'type': com[2], 'month': com[3], 'year': com[4], \
                    'details': com[5], 'amount': com[6], 'interest': com[7], 'commodity_balance': com[8], \
                    'date_created': com[9], 'date_last_modified': com[10], 'member_id': com[11]}
                commodities.append(commodity)
            return commodities
    
# db = Monthly_DB()
# today = datetime.date.today()
# date_created = today.strftime("%d/%m/%Y")
# date_last_modified = date_created
# com = ('TRANS234', 'Monthly Savings', 'July', '2022', 'Monthly Savings for the month of July, 2022', '30000.00', \
#             '200.00', '300000.00', '12000.00', date_created, date_last_modified, 'FOPAJ1473')

# results = db.add_commodity(com)
# results = db.get_commodity(('FOPAJ1473',))
# results = db.get_commodities()

# print(results)