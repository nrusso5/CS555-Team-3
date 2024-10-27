import mysql.connector
from cryptography.fernet import Fernet

class mySQLdb:
    def __init__(self, host, user, password, database, key=None):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='PAssword21!',
            database='test_db'
        )
        if not key:
            self.key = Fernet.generate_key()
        else:
            self.key = key
        self.cipher = Fernet(self.key)
        self.cursor = self.conn.cursor()

    def encrypt_data(self, data):
        return self.cipher.encrypt(data.encode())

    def decrypt_data(self, data: bytes):
        return self.cipher.decrypt(data).decode()

    def insert_contact_info(self, full_name, phone_number):
        """
        Send contact information into mysql database
        """
        full_name = self.encrypt_data(full_name)
        phone_number = self.encrypt_data(full_name)

        sql = "INSERT INTO contactinformation (full_name, phone_number) VALUES (%s, %s)"
        self.cursor.execute(sql, (full_name, phone_number))
        self.conn.commit()
        print(f'User {full_name}, with phone number: {phone_number} added')

    def insert_health_information(self, id, comments):
        """
        Send health information into mysql database
        """
        comments = self.encrypt_data(comments)
        sql = "INSERT INTO healthinformation (id, comments) VALUES (%s, %s)"
        self.cursor.execute(sql, (id, comments))
        self.conn.commit()
        print(f'User {id} added')

    def fetch_contact_by_id(self, id):
        """
        Fetch contact information by userID
        """
        sql = "SELECT * FROM contactinformation WHERE ID = %s"
        self.cursor.execute(sql, (id,))
        results = self.cursor.fetchall()
        results = self.decrypt_data(results[0][1])
        results2 = self.decrypt_data(results[0][2])
        return results, results2

    def fetch_health_information_by_id(self, id):
        """
        Fetch health information by userID 
        """
        sql = "SELECT * FROM healthinformation WHERE ID = %s"
        self.cursor.execute(sql, (id,))
        results = self.cursor.fetchall()
        results = self.decrypt_data(results[0][0])
        results2 = self.decrypt_data(results[0][1])
        return results

    def log_changes(self, user, database, action, time):
        """
        Log all changes made to databases healthinformation and contactinformation
        """
        user = self.encrypt_data(user)
        database = self.encrypt_data(database)
        action = self.encrypt_data(action)
        time = self.encrypt_data(time)

        sql = "INSERT INTO audit_log (user, database, action, time) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (user, database, action, time))
        self.conn.commit()
        print("Changelog saved")



    if __name__ == '__main__':
        quit()