import sqlite3
import datetime

class Exit_DB():
    def __init__(self, *args, **kwargs):
        self.connection = sqlite3.connect('fopaj.db')
        self.cursor = self.connection.cursor()
        command = '''CREATE TABLE IF NOT EXISTS exit_savings(exit_id INTEGER PRIMARY KEY AUTOINCREMENT, exitID TEXT NOT NULL, type TEXT NOT NULL, 
                month TEXT NOT NULL, year TEXT NOT NULL, details TEXT NOT NULL, amount FLOAT NOT NULL, interest FLOAT NOT NULL, 
                total_exit FLOAT NOT NULL, date_created DATE NOT NULL, date_last_modified DATE NOT NULL, member_id INTEGER, FOREIGN KEY (member_id) 
                REFERENCES members (member_id) ON UPDATE CASCADE ON DELETE CASCADE)'''
        self.cursor.execute(command)     

    def add_exit_saving(self, exit_saving):
        self.cursor.execute('INSERT INTO exit_savings VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', exit_saving)
        self.connection.commit()
        # self.connection.close()
        # print(exit_saving)
    
    def get_exit_saving(self, id):
        command = "SELECT * FROM exit_savings WHERE exit_id=?"
        self.cursor.execute(command, id)
        result = self.cursor.fetchall()
        if len(result) <=0:
            return []
        else:
            exit = result[0]
            exit_saving = {'exit_id': exit[0], 'exitID': exit[1], 'type': exit[2], 'month': exit[3], 'year': exit[4], \
                    'details': exit[5], 'amount': exit[6], 'interest': exit[7], 'total_exit': exit[8], \
                    'date_created': exit[9], 'date_last_modified': exit[10], 'member_id': exit[11]}
            return exit_saving

    def get_member_exit_savings(self, id):
        command = "SELECT * FROM exit_savings WHERE member_id=? ORDER BY exit_id DESC"
        self.cursor.execute(command, id)
        results = self.cursor.fetchall()
        if len(results) <= 0:
            return []
        else: 
            exit_savings = []
            for exit in results:
                exit_saving = {'exit_id': exit[0], 'exitID': exit[1], 'type': exit[2], 'month': exit[3], 'year': exit[4], \
                    'details': exit[5], 'amount': exit[6], 'interest': exit[7], 'total_exit': exit[8],  \
                    'date_created': exit[9], 'date_last_modified': exit[10], 'member_id': exit[11]}
                exit_savings.append(exit_saving)
            return exit_savings

    def get_all_exit_savings(self):
        command = "SELECT * FROM exit_savings ORDER BY exit_id DESC"
        # command = "SELECT * FROM exit_savings ORDER BY id DESC"
        self.cursor.execute(command)
        results = self.cursor.fetchall()
        if len(results) <= 0:
            return []
        else: 
            exit_savings = []
            for exit in results:
                exit_saving = {'exit_id': exit[0], 'exitID': exit[1], 'type': exit[2], 'month': exit[3], 'year': exit[4], \
                    'details': exit[5], 'amount': exit[6], 'interest': exit[7], 'total_exit': exit[8], \
                    'date_created': exit[9], 'date_last_modified': exit[10], 'member_id': exit[11]}
                exit_savings.append(exit_saving)
            return exit_savings

    
    def update_exit_saving(self, exit_saving):
        command = '''UPDATE exit_savings SET exitID=?, type=?, month=?, year=?, details=?, amount=?, interest=?, 
        total_exit=?, date_created=?, date_last_modified=?, member_id=? WHERE exit_id=?'''
        self.cursor.execute(command, exit_saving)
        self.connection.commit()
        # self.connection.close()  
    
    def remove_exit_saving(self, id):
        command = "DELETE FROM exit_savings WHERE exit_id=?"
        self.cursor.execute(command, id)
        self.connection.commit()
        # self.connection.close()
    
    def get_editable_exits(self, params):
        # command = "SELECT * FROM exit_savings WHERE exit_id > ? AND member_id = ? ORDER BY exit_id DESC"
        command = "SELECT * FROM exit_savings WHERE exit_id > ? AND member_id = ?"
        self.cursor.execute(command, params)
        results = self.cursor.fetchall()
        if len(results) <= 0:
            return []
        else: 
            exit_savings = []
            for exit in results:
                exit_saving = {'exit_id': exit[0], 'exitID': exit[1], 'type': exit[2], 'month': exit[3], 'year': exit[4], \
                    'details': exit[5], 'amount': exit[6], 'interest': exit[7], 'total_exit': exit[8], \
                    'date_created': exit[9], 'date_last_modified': exit[10], 'member_id': exit[11]}
                exit_savings.append(exit_saving)
            return exit_savings