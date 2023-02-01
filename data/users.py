import sqlite3, datetime


class User_DB():
    def __init__(self, *args, **kwargs):
        self.connection = sqlite3.connect('fopaj.db')
        c = self.connection.cursor()
        command = '''CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, userID TEXT NOT NULL, 
        surname TEXT NOT NULL, firstname TEXT NOT NULL, othername TEXT NOT NULL, fullname TEXT NOT NULL, 
        username TEXT NOT NULL, password TEXT NOT NULL, designation TEXT, role TEXT NOT NULL, 
        date_enrolled DATE NOT NULL, date_last_modified DATE NOT NULL)'''
        c.execute(command)   
        self.connection.commit()      

    def add_user(self, user):
        c = self.connection.cursor()
        c.execute('INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', user)
        self.connection.commit()
        c.close()
    
    def get_user(self, id):
        c = self.connection.cursor()
        command = "SELECT * FROM users WHERE user_id=?"
        c.execute(command, id)
        result = c.fetchall()
        user = result[0]
        format = '%Y-%m-%d %H:%M:%S.%f'
        date_enrolled = datetime.datetime.strptime((user[10]), format).strftime("%d/%m/%Y")
        date_last_modified = datetime.datetime.strptime((user[11]), format).strftime("%d/%m/%Y")
        user_fetched = {'user_id': user[0], 'userID': user[1], 'surname': user[2], 'firstname': user[3], \
                'othername': user[4], 'fullname': user[5], 'username': user[6], 'password': user[7], \
                'designation': user[8], 'role': user[9], 'date_enrolled': date_enrolled, 'date_last_modified': date_last_modified}
        c.close()
        return user_fetched
        
    
    def get_users(self):
        c = self.connection.cursor()
        command = "SELECT * FROM users ORDER BY user_id DESC"
        c.execute(command)
        results = c.fetchall()
        users = []
        for user in results:
            user = {'user_id': user[0], 'userID': user[1], 'surname': user[2], 'firstname': user[3], \
                'othername': user[4], 'fullname': user[5], 'username': user[6], 'password': user[7], \
                'designation': user[8], 'role': user[9], 'date_enrolled': user[10], 'date_last_modified': user[11]}               
            users.append(user)
        c.close()
        return users

    def update_user(self, user):
        c = self.connection.cursor()
        command = '''UPDATE users SET surname=?, firstname=?, othername=?, fullname=?, username=?, password=?,
        designation=?, role=?, date_last_modified=? WHERE user_id = ?'''
        c.execute(command, user)
        self.connection.commit()
        c.close()
        
    def remove_user(self, id):
        c = self.connection.cursor()
        command = "DELETE FROM users WHERE user_id=?"
        c.execute(command, id)
        self.connection.commit()
        c.close()
    
    def get_login_user(self, params):
        c = self.connection.cursor()
        command = "SELECT * FROM users WHERE username=? AND password=?"
        c.execute(command, params)
        user = c.fetchone()
        if user == None:
            user_fetched = {}
        else:
            format = '%Y-%m-%d %H:%M:%S.%f'
            date_enrolled = datetime.datetime.strptime((user[10]), format).strftime("%d/%m/%Y")
            date_last_modified = datetime.datetime.strptime((user[11]), format).strftime("%d/%m/%Y")
            user_fetched = {'user_id': user[0], 'userID': user[1], 'surname': user[2], 'firstname': user[3], \
                    'othername': user[4], 'fullname': user[5], 'username': user[6], 'password': user[7], \
                    'designation': user[8], 'role': user[9], 'date_enrolled': date_enrolled, 'date_last_modified': date_last_modified}
        c.close()
        return user_fetched