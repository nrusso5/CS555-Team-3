import mysql.connector
from cryptography.fernet import Fernet

class mySQLdb:
    def __init__(self, host, user, password, database, key=None):
        host, port = host.split(":")
        self.conn = mysql.connector.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database
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
        if isinstance(data, str):
            data = data.encode()  
        return self.cipher.decrypt(data).decode() 


    def insert_contact_info(self, full_name, phone_number):
        """
        Send contact information into mysql database
        """
        full_name = self.encrypt_data(full_name)
        phone_number = self.encrypt_data(phone_number)

        sql = "INSERT INTO contact_information (full_name, phone_number) VALUES (%s, %s)"
        self.execute_sql(sql, full_name, phone_number)


    def insert_health_information(self, id, comments):
        """
        Send health information into mysql database
        """
        comments = self.encrypt_data(comments)
        sql = "INSERT INTO health_information (id, comments) VALUES (%s, %s)"
        self.execute_sql(sql, id, comments)


    def fetch_contact_by_id(self, id):
        """
        Fetch contact information by userID
        """
        sql = "SELECT * FROM contact_information WHERE ID = %s"
        self.cursor.execute(sql, (id,))
        results = self.cursor.fetchall()
        name = self.decrypt_data(results[0][1])
        phone_number = self.decrypt_data(results[0][2])
        return name, phone_number


    def fetch_health_information_by_id(self, id):
        """
        Fetch health information by userID 
        """
        sql = "SELECT * FROM health_information WHERE ID = %s"
        self.cursor.execute(sql, (id,))
        results = self.cursor.fetchall()
        id = results[0][0]
        comments = self.decrypt_data(results[0][1])
        return id, comments
        

    def execute_sql(self, sql, s1, s2=None):
        self.cursor.execute(sql, (s1, s2))
        self.conn.commit


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
        pass