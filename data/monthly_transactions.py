import sqlite3
from collections import OrderedDict
import datetime

class Monthly_DB():
    def __init__(self, *args, **kwargs):
        self.connection = sqlite3.connect('fopaj.db')
        self.cursor = self.connection.cursor()
        command = '''CREATE TABLE IF NOT EXISTS monthly_transactions(trans_id INTEGER PRIMARY KEY AUTOINCREMENT, transID TEXT NOT NULL, type TEXT NOT NULL, 
                month TEXT NOT NULL, year TEXT NOT NULL, details TEXT NOT NULL, amount FLOAT NOT NULL, interest FLOAT NOT NULL, 
                total_savings FLOAT NOT NULL, loan_balance FLOAT NOT NULL, date_created DATE NOT NULL, 
                date_last_modified DATE NOT NULL, member_id INTEGER, FOREIGN KEY (member_id) 
                REFERENCES members (member_id) ON UPDATE CASCADE ON DELETE CASCADE)'''
        self.cursor.execute(command)     

    def add_transaction(self, transaction):
        self.cursor.execute('INSERT INTO monthly_transactions VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', transaction)
        self.connection.commit()
        # self.connection.close()
        # print(transaction)
    
    def get_transaction(self, id):
        command = "SELECT * FROM monthly_transactions WHERE trans_id=?"
        self.cursor.execute(command, id)
        result = self.cursor.fetchall()
        if len(result) <=0:
            return []
        else:
            trans = result[0]
            transaction = {'trans_id': trans[0], 'transID': trans[1], 'type': trans[2], 'month': trans[3], 'year': trans[4], \
                    'details': trans[5], 'amount': trans[6], 'interest': trans[7], 'total_savings': trans[8], \
                    'loan_balance': trans[9], 'date_created': trans[10], 'date_last_modified': trans[11], 'member_id': trans[12]}
            return transaction

    def get_member_transactions(self, id):
        command = "SELECT * FROM monthly_transactions WHERE member_id=? ORDER BY trans_id DESC"
        self.cursor.execute(command, id)
        results = self.cursor.fetchall()
        if len(results) <= 0:
            return []
        else: 
            transactions = []
            for trans in results:
                format = '%Y-%m-%d %H:%M:%S.%f'
                date_created = datetime.datetime.strptime((trans[10]), format).strftime("%d/%m/%Y")
                date_last_modified = datetime.datetime.strptime((trans[11]), format).strftime("%d/%m/%Y")
                transaction = {'trans_id': trans[0], 'transID': trans[1], 'type': trans[2], 'month': trans[3], 'year': trans[4], \
                    'details': trans[5], 'amount': trans[6], 'interest': trans[7], 'total_savings': trans[8], \
                    'loan_balance': trans[9], 'date_created': date_created, 'date_last_modified': date_last_modified, 'member_id': trans[12]}
                transactions.append(transaction)
            return transactions

    def get_all_transactions(self):
        command = '''SELECT trans_id, transID, type, month, year, details, amount, 
        monthly_transactions.date_last_modified as date_last_modified, monthly_transactions.member_id as member_id, 
        members.fullname as fullname FROM monthly_transactions INNER JOIN members ON members.member_id = monthly_transactions.member_id
        ORDER BY monthly_transactions.date_last_modified DESC'''
        command2 = '''SELECT com_id, comID, type, month, year, details, amount, 
        commodities.date_last_modified as date_last_modified, commodities.member_id as member_id, 
        members.fullname as fullname FROM commodities INNER JOIN members ON members.member_id = commodities.member_id
        ORDER BY commodities.date_last_modified DESC'''
        command3 = '''SELECT xmas_id, xmasID, type, month, year, details, amount, 
        xmas_savings.date_last_modified as date_last_modified, xmas_savings.member_id as member_id, 
        members.fullname as fullname FROM xmas_savings INNER JOIN members ON members.member_id = xmas_savings.member_id
        ORDER BY xmas_savings.date_last_modified DESC'''
        command4 = '''SELECT edu_id, eduID, type, month, year, details, amount, 
        edu_savings.date_last_modified as date_last_modified, edu_savings.member_id as member_id, 
        members.fullname as fullname FROM edu_savings INNER JOIN members ON members.member_id = edu_savings.member_id
        ORDER BY edu_savings.date_last_modified DESC'''
        command5 = '''SELECT exit_id, exitID, type, month, year, details, amount, 
        exit_savings.date_last_modified as date_last_modified, exit_savings.member_id as member_id, 
        members.fullname as fullname FROM exit_savings INNER JOIN members ON members.member_id = exit_savings.member_id
        ORDER BY exit_savings.date_last_modified DESC'''
        self.cursor.execute(command)
        results = self.cursor.fetchall()
        if len(results) <= 0:
            monthly_transactions = []
        else: 
            monthly_transactions = results

        self.cursor.execute(command2)
        results2 = self.cursor.fetchall()
        if len(results2) <= 0:
            commodities = []
        else: 
            commodities = results2

        self.cursor.execute(command3)
        results3 = self.cursor.fetchall()
        if len(results3) <= 0:
            xmas_savings = []
        else: 
            xmas_savings = results3

        self.cursor.execute(command4)
        results4 = self.cursor.fetchall()
        if len(results4) <= 0:
            edu_savings = []
        else: 
            edu_savings = results4

        self.cursor.execute(command5)
        results5 = self.cursor.fetchall()
        if len(results5) <= 0:
            exit_savings = []
        else: 
            exit_savings = results
        
        transactions = monthly_transactions + commodities + xmas_savings + edu_savings + exit_savings
        all_transactions = []
        for trans in transactions:
            transaction = {'trans_id': trans[0], 'transID': trans[1], 'type': trans[2], 'month': trans[3], 'year': trans[4], \
                'details': trans[5], 'amount': trans[6], 'date_last_modified': trans[7], 'member_id': trans[8], \
                'fullname': trans[9]}
            all_transactions.append(transaction)
        sorted_transactions = sorted(all_transactions, key=lambda x: x['date_last_modified'], reverse=True)
        return sorted_transactions[:10]
        # return transactions

    
    def update_transaction(self, transaction):
        command = '''UPDATE monthly_transactions SET transID=?, type=?, month=?, year=?, details=?, amount=?, interest=?, 
        total_savings=?, loan_balance=?, date_created=?, date_last_modified=?, member_id=? WHERE trans_id=?'''
        self.cursor.execute(command, transaction)
        self.connection.commit()
        # self.connection.close()  
    
    def remove_transaction(self, id):
        command = "DELETE FROM monthly_transactions WHERE trans_id=?"
        self.cursor.execute(command, id)
        self.connection.commit()
        # self.connection.close()
    
    def get_editable_trans(self, params):
        # command = "SELECT * FROM monthly_transactions WHERE trans_id > ? AND member_id = ? ORDER BY trans_id DESC"
        command = "SELECT * FROM monthly_transactions WHERE trans_id > ? AND member_id = ?"
        self.cursor.execute(command, params)
        results = self.cursor.fetchall()
        if len(results) <= 0:
            return []
        else: 
            transactions = []
            for trans in results:
                transaction = {'trans_id': trans[0], 'transID': trans[1], 'type': trans[2], 'month': trans[3], 'year': trans[4], \
                    'details': trans[5], 'amount': trans[6], 'interest': trans[7], 'total_savings': trans[8], \
                    'loan_balance': trans[9], 'date_created': trans[10], 'date_last_modified': trans[11], 'member_id': trans[12]}
                transactions.append(transaction)
            return transactions
    
# db = Monthly_DB()
# today = datetime.date.today()
# date_created = today.strftime("%d/%m/%Y")
# date_last_modified = date_created
# trans = ('TRANS234', 'Monthly Savings', 'July', '2022', 'Monthly Savings for the month of July, 2022', '30000.00', \
#             '200.00', '300000.00', '12000.00', date_created, date_last_modified, 'FOPAJ1473')

# results = db.add_transaction(trans)
# results = db.get_transaction(('FOPAJ1473',))
# results = db.get_all_transactions()

# print(results)