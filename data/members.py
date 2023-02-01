import sqlite3
from collections import OrderedDict

class Member_DB():
    def __init__(self, *args, **kwargs):
        self.connection = sqlite3.connect('fopaj.db')
        self.cursor = self.connection.cursor()
        command = "CREATE TABLE IF NOT EXISTS members(member_id INTEGER PRIMARY KEY AUTOINCREMENT, memberID TEXT NOT NULL, staff_no TEXT, ledger_no TEXT, title TEXT, surname TEXT NOT NULL, firstname TEXT NOT NULL, othername TEXT, fullname TEXT NOT NULL, gender TEXT NOT NULL, dob TEXT, phone_no TEXT NOT NULL, email TEXT, contact TEXT, \
                dept TEXT NOT NULL, designation TEXT, salary TEXT, bank_name TEXT, account_no TEXT, account_type TEXT, doa TEXT NOT NULL, date_enrolled DATE NOT NULL, date_last_modified DATE NOT NULL, nok_title TEXT, nok_surname TEXT NOT NULL, nok_firstname TEXT NOT NULL, nok_othername TEXT, \
                nok_fullname TEXT NOT NULL, nok_gender TEXT, nok_phone_no TEXT NOT NULL, nok_email TEXT, nok_job_status TEXT, \
                nok_contact TEXT, nok_work_place TEXT, g1_surname TEXT NOT NULL, g1_firstname TEXT NOT NULL, g1_othername TEXT, g1_phone_no TEXT NOT NULL, g1_email TEXT, g1_contact TEXT, g2_surname TEXT NOT NULL, g2_firstname TEXT NOT NULL, g2_othername TEXT, g2_phone_no TEXT NOT NULL, g2_email TEXT, g2_contact TEXT, \
                monthly_savings FLOAT DEFAULT 0.00, share_capital FLOAT DEFAULT 0.00, xmas_savings FLOAT DEFAULT 0.00, edu_savings FLOAT DEFAULT 0.00, exit_savings FLOAT DEFAULT 0.00, total_savings FLOAT DEFAULT 0.00, total_assets FLOAT DEFAULT 0.00, total_edu FLOAT DEFAULT 0.00, total_exit FLOAT DEFAULT 0.00, \
                total_xmas FLOAT DEFAULT 0.00, loan_balance FLOAT DEFAULT 0.00, commodity_payment FLOAT DEFAULT 0.00, commodity_balance FLOAT DEFAULT 0.00, entrance_fee FLOAT DEFAULT 0.00)"
        self.cursor.execute(command)         

    def add_member(self, member):
        self.cursor.execute('INSERT INTO members VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', member)
        self.connection.commit()
        # self.connection.close()
    
    def get_member(self, id):
        command = "SELECT * FROM members WHERE member_id=?"
        self.cursor.execute(command, id)
        result = self.cursor.fetchall()
        mem = result[0]
        member = {'member_id': mem[0], 'memberID': mem[1], 'staff_no': mem[2], 'ledger_no': mem[3], 'title': mem[4], \
                'surname': mem[5], 'firstname': mem[6], 'othername': mem[7], 'fullname': mem[8], \
                'gender': mem[9], 'dob': mem[10], 'phone_no': mem[11], 'email': mem[12], 'contact': mem[13], \
                'dept': mem[14], 'designation': mem[15], 'salary': mem[16], 'bank_name': mem[17], \
                'account_no': mem[18], 'account_type': mem[19], 'doa': mem[20], 'date_enrolled': mem[21], \
                'date_last_modified': mem[22], 'nok_title': mem[23], 'nok_surname': mem[24], 'nok_firstname': mem[25], \
                'nok_othername': mem[26], 'nok_fullname': mem[27], 'nok_gender': mem[28], 'nok_phone_no': mem[29], \
                'nok_email': mem[30], 'nok_job_status': mem[31], 'nok_contact': mem[32], 'nok_work_place': mem[33], \
                'g1_surname': mem[34], 'g1_firstname': mem[35], 'g1_othername': mem[36], 'g1_phone_no': mem[37], \
                'g1_email': mem[38], 'g1_contact': mem[39], 'g2_surname': mem[40], 'g2_firstname': mem[41], \
                'g2_othername': mem[42], 'g2_phone_no': mem[43], 'g2_email': mem[44], 'g2_contact': mem[45], \
                'monthly_savings': mem[46], 'share_capital': mem[47], 'xmas_savings': mem[48], 'edu_savings': mem[49], \
                'exit_savings': mem[50], 'total_savings': mem[51], 'total_assets': mem[52], 'total_edu': mem[53], \
                'total_exit': mem[54], 'total_xmas': mem[55], 'loan_balance': mem[56], 'commodity_payment': mem[57], \
                'commodity_balance': mem[58], 'entrance_fee': mem[59]}
        return member
    
    def get_members(self):
        command = "SELECT * FROM members ORDER BY member_id DESC"
        # command = "SELECT * FROM members ORDER BY id DESC"
        self.cursor.execute(command)
        results = self.cursor.fetchall()
        members = []
        for mem in results:
            member = {'member_id': mem[0], 'memberID': mem[1], 'staff_no': mem[2], 'ledger_no': mem[3], 'title': mem[4], \
                'surname': mem[5], 'firstname': mem[6], 'othername': mem[7], 'fullname': mem[8], \
                'gender': mem[9], 'dob': mem[10], 'phone_no': mem[11], 'email': mem[12], 'contact': mem[13], \
                'dept': mem[14], 'designation': mem[15], 'salary': mem[16], 'bank_name': mem[17], \
                'account_no': mem[18], 'account_type': mem[19], 'doa': mem[20], 'date_enrolled': mem[21], \
                'date_last_modified': mem[22], 'nok_title': mem[23], 'nok_surname': mem[24], 'nok_firstname': mem[25], \
                'nok_othername': mem[26], 'nok_fullname': mem[27], 'nok_gender': mem[28], 'nok_phone_no': mem[29], \
                'nok_email': mem[30], 'nok_job_status': mem[31], 'nok_contact': mem[32], 'nok_work_place': mem[33], \
                'g1_surname': mem[34], 'g1_firstname': mem[35], 'g1_othername': mem[36], 'g1_phone_no': mem[37], \
                'g1_email': mem[38], 'g1_contact': mem[39], 'g2_surname': mem[40], 'g2_firstname': mem[41], \
                'g2_othername': mem[42], 'g2_phone_no': mem[43], 'g2_email': mem[44], 'g2_contact': mem[45], \
                'monthly_savings': mem[46], 'share_capital': mem[47], 'xmas_savings': mem[48], 'edu_savings': mem[49], \
                'exit_savings': mem[50], 'total_savings': mem[51], 'total_assets': mem[52], 'total_edu': mem[53], \
                'total_exit': mem[54], 'total_xmas': mem[55], 'loan_balance': mem[56], 'commodity_payment': mem[57], \
                'commodity_balance': mem[58], 'entrance_fee': mem[59]}                
            members.append(member)
        return members

    def get_searched_members(self):
        command = "SELECT member_id, memberID, ledger_no, fullname, dept, phone_no FROM members"
        self.cursor.execute(command)
        results = self.cursor.fetchall()
        members = []
        for mem in results:
            member = {'member_id': mem[0], 'memberID': mem[1], 'ledger_no': mem[2], 'fullname': mem[3],\
                'dept': mem[4], 'phone_no': mem[5] }                
            members.append(member)
        return members

    def update_member(self, member):
        command = '''UPDATE members SET staff_no=?, ledger_no=?, title=?, surname=?, firstname=?, othername=?, 
        fullname=?, gender=?, dob=?, phone_no=?, email=?, contact=?, dept=?, designation=?, salary=?, 
        bank_name=?, account_no=?, account_type=?, doa=?, date_last_modified=?, nok_title=?, nok_surname=?,
        nok_firstname=?, nok_othername=?, nok_fullname=?, nok_gender=?, nok_phone_no=?, nok_email=?, 
        nok_job_status=?, nok_contact=?, nok_work_place=?, g1_surname=?, g1_firstname=?, g1_othername=?, 
        g1_phone_no=?, g1_email=?, g1_contact=?, g2_surname=?, g2_firstname=?, g2_othername=?, g2_phone_no=?, 
        g2_email=?, g2_contact=?, monthly_savings=?, xmas_savings=?, edu_savings=?, exit_savings=?, total_savings=?,
        total_assets=?, total_edu=?, total_exit=?, total_xmas=?, loan_balance=?, commodity_payment=?,
        commodity_balance=? WHERE member_id=?'''
        self.cursor.execute(command, member)
        self.connection.commit()
        # self.connection.close()
        #   
    def update_member_trans(self, member):
        command = '''UPDATE members SET total_savings=?, total_assets=?, loan_balance=? WHERE member_id=?'''
        self.cursor.execute(command, member)
        self.connection.commit()
        # self.connection.close()  

    def update_member_com(self, member):
        command = '''UPDATE members SET commodity_balance=? WHERE member_id=?'''
        self.cursor.execute(command, member)
        self.connection.commit()
        # self.connection.close()  

    def update_member_edu(self, member):
        command = '''UPDATE members SET total_edu=? WHERE member_id=?'''
        self.cursor.execute(command, member)
        self.connection.commit()

    def update_member_exit(self, member):
        command = '''UPDATE members SET total_exit=? WHERE member_id=?'''
        self.cursor.execute(command, member)
        self.connection.commit()

    def update_member_xmas(self, member):
        command = '''UPDATE members SET total_xmas=? WHERE member_id=?'''
        self.cursor.execute(command, member)
        self.connection.commit()
        # self.connection.close()  
    
    def remove_member(self, id):
        command = "DELETE FROM members WHERE member_id=?"
        self.cursor.execute(command, id)
        self.connection.commit()
        # self.connection.close()
    
    def get_members_count(self):
        command = "SELECT COUNT(*) FROM members"
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        if len(result) <=0:
            return 0
        else:
            return result[0]

    def get_total_share_capital(self):
        command = "SELECT SUM(share_capital) FROM members"
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        if len(result) <=0:
            return 0
        else:
            return result[0]

    def get_total_assets(self):
        command = "SELECT SUM(total_assets) FROM members"
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        if len(result) <=0:
            return 0
        else:
            return result[0]

    def get_total_savings(self):
        command = "SELECT SUM(total_savings) FROM members"
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        if len(result) <=0:
            return 0
        else:
            return result[0]

    def get_total_loan_balance(self):
        command = "SELECT SUM(loan_balance) FROM members"
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        if len(result) <=0:
            return 0
        else:
            return result[0]

    def get_total_xmas(self):
        command = "SELECT SUM(total_xmas) FROM members"
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        if len(result) <=0:
            return 0
        else:
            return result[0]

    def get_total_edu(self):
        command = "SELECT SUM(total_edu) FROM members"
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        if len(result) <=0:
            return 0
        else:
            return result[0]

    def get_total_exit(self):
        command = "SELECT SUM(total_exit) FROM members"
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        if len(result) <=0:
            return 0
        else:
            return result[0]
    
# db = Member_DB()
# results = db.get_member(('FOPAJ1907',))
# results = db.get_members_count()

# print(results)
# print(len(results))