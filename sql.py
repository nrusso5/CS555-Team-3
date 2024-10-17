import mysql.connector
class mySQLdb:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host='--',
            user='--',
            password='--',
            database='--'
        )
        self.cursor = self.conn.cursor()

    def insert_contact_info(self, full_name, phone_number):
        sql = "INSERT INTO contactinformation (full_name, phone_number) VALUES (%s, %s)"
        self.cursor.execute(sql, (full_name, phone_number))
        self.conn.commit()
        print(f'User {full_name}, with phone number: {phone_number} added')

    def insert_health_information(self, id, comments):
        sql = "INSERT INTO healthinformation (id, comments) VALUES (%s, %s)"
        self.cursor.execute(sql, (id, comments))
        self.conn.commit()
        print(f'User {id} added')

    def fetch_contact_by_id(self, id):
        sql = "SELECT * FROM contactinformation WHERE ID = %s"
        self.cursor.execute(sql, (id,))
        results = self.cursor.fetchall()
        return results
        # print(f"user with {id}'s information: {results}")
        # print(f'Types: id:{type(id)}, results: {type(results[0][0])} {type(results[0][1])} {type(results[0][2])}')

    def fetch_health_information_by_id(self, id):
        sql = "SELECT * FROM healthinformation WHERE ID = %s"
        self.cursor.execute(sql, (id,))
        results = self.cursor.fetchall()
        return results

    def fetch_table(self, table):
        self.cursor.execute(f'SELECT * FROM {table}')
        results = self.cursor.fetchall()
        for row in results:
            print(row)

    if __name__ == '__main__':
        insert_contact_info("John doe", "9999999999")

        insert_health_information("1", "comments about the health of this person with user id 1")
        fetch_contact_by_id(1)
        fetch_table("contactinformation")
        fetch_table("healthinformation")

        # insert_user('Alice', 'alice@example.com')
        # insert_user('Bob', 'bob@example.com')

        # print("Current users in the database:")
        # fetch_users()

        # Close the cursor and connection
        # self.cursor.close()
        # self.conn.close()