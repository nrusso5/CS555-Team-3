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

    def create_user(self, id):
        sql = "INSERT INTO health_information (id, comments) VALUES (%s, %s)"
        self.execute_sql(sql, id, self.encrypt_data(","))
    
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
    

    #Adding edit contact info doesn't seem necessary as its not being used.
    #Changed to assume userid is created by default. this will be the default write function. 
    #structure: time-medicine,time-habit
    def edit_health_information(self, id, comments, reminderType: bool, removing: bool):
        """
        Update health information with userID
        reminderType: 0->medicine reminder. 1-> healthy habit
        """
        prior = self.fetch_health_information_by_id(id)

        if comments not in prior:
            raise ValueError("Value not in table")
                

        prior = prior[1]
        prior = prior.split(',')
        if (not reminderType and not removing):
            if (prior[0] == ""):
                comments += "," + prior[1]
            else:
                comments = prior[0] + ";" + comments + "," + prior[1]
        elif(reminderType and not removing):
            if (prior[1] == ""):
                comments = prior[0] + "," + comments
            else:
                comments = prior[0] + "," + prior[1] + ";" + comments
        elif (not reminderType and removing):
            objects = prior[0].split(";")
            filter = [obj for obj in objects if obj != comments]#here comments is the item to remove. 
            comments = ";".join(filter) + "," + prior[1]
        elif(reminderType and removing):
            objects = prior[1].split(";")
            filter = [obj for obj in objects if obj != comments]
            comments = prior[0] + "," + ";".join(filter)
        comments = self.encrypt_data(comments)
        sql = "UPDATE health_information SET comments = %s WHERE ID = %s"
        self.execute_sql(sql, comments, id)
    

    def execute_sql(self, sql, s1, s2=None):
        self.cursor.execute(sql, (s1, s2))
        self.conn.commit()


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