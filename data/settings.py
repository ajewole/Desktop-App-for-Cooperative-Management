import sqlite3, datetime


class Settings_DB():
    def __init__(self, *args, **kwargs):
        self.connection = sqlite3.connect('fopaj.db')
        c = self.connection.cursor()
        command = '''CREATE TABLE IF NOT EXISTS settings(settings_id INTEGER PRIMARY KEY AUTOINCREMENT,  
        app_name TEXT NOT NULL DEFAULT 'FOPAJ FARMERS COOPERATIVE MULTIPURPOSE SOCIETY LIMITED', 
        app_logo TEXT, interest_rate FLOAT DEFAULT 0.01, entrance_fee FLOAT DEFAULT 5000.00,
        share_capital FLOAT DEFAULT 10000.00, monthly_savings FLOAT DEFAULT 20000.00, 
        xmas_savings FLOAT DEFAULT 1000.00, edu_savings FLOAT DEFAULT 1000.00, exit_savings FLOAT DEFAULT 1000.00,
        date_last_modified DATE)'''
        c.execute(command)   
        self.connection.commit()      

    def get_settings(self):
        c = self.connection.cursor()
        command = "SELECT * FROM settings ORDER BY settings_id DESC LIMIT 1"
        c.execute(command)
        settings = c.fetchone()
        settings_fetched = {'settings_id': settings[0], 'app_name': settings[1], 'app_logo': settings[2], \
            'interest_rate': settings[3], 'entrance_fee': settings[4], 'share_capital': settings[5], \
            'monthly_savings': settings[6], 'xmas_savings': settings[7], 'edu_savings': settings[8], 
            'exit_savings': settings[9], 'date_last_modified': settings[10]}               
        c.close()
        return settings_fetched

    def update_setting(self, settings):
        c = self.connection.cursor()
        command = '''UPDATE settings SET app_name=?, app_logo=?, interest_rate=?, entrance_fee=?, share_capital=?,
        monthly_savings=?, xmas_savings=?, edu_savings=?, exit_savings=?, date_last_modified=? '''
        c.execute(command, settings)
        self.connection.commit()
        c.close()
    