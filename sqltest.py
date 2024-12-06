import unittest
import mysql.connector
from sql import mySQLdb

class testMySQLDatabase(unittest.TestCase):
    @classmethod 
    def setUpClass(cls):
        host = input("Enter MySQL host (e.g., localhost): ")
        user = input("Enter MySQL username: ")
        password = input("Enter MySQL password: ")
        database_name = input("Enter the name of the database to connect to: ")
        
        # Establish a connection to the database
        cls.database = mySQLdb(host, user, password, database_name)

    def testInsertAndFetchContact(self):
        self.database.insert_contact_info("John Doe", "9009009999")
        test11 = self.database.fetch_contact_by_id(1)
        self.assertEqual(test11, ("John Doe", "9009009999"))

        self.database.insert_contact_info("Jane Doe", "900900900")
        test11 = self.database.fetch_contact_by_id(2)
        self.assertEqual(test11, ("Jane Doe", "900900900"))

    def testInsertAndFetchHealth(self):
        self.database.create_user("999")
        test11 = self.database.fetch_health_information_by_id(999)
        self.assertEqual(test11, (999, ","))

        self.database.edit_health_information("999", "comments for patient with this ID", 0)
        test21 = self.database.fetch_health_information_by_id(999)
        self.assertEqual(test21, (999, "comments for patient with this ID,"))

        self.database.edit_health_information("999", "different comments for patient with this ID", 0)
        test21 = self.database.fetch_health_information_by_id(999)
        self.assertEqual(test21, (999, "different comments for patient with this ID,"))
        
        self.database.create_user("998")
        test11 = self.database.fetch_health_information_by_id(998)
        self.assertEqual(test11, (998, ","))

        self.database.edit_health_information("998", "comments for patient with this ID", 1)
        test11 = self.database.fetch_health_information_by_id("998")
        self.assertEqual(test11, (998, ",comments for patient with this ID"))

        self.database.edit_health_information("999", "Comments in index 1", 1)
        test11 = self.database.fetch_health_information_by_id("999")
        self.assertEqual(test11, (999, "different comments for patient with this ID,Comments in index 1"))

    def testEncryptionAndDecryption(self):
        encrypted_name = self.database.encrypt_data("John Doe")
        self.assertNotEqual(encrypted_name, "John Doe")
        decrypted_name = self.database.decrypt_data(encrypted_name)
        self.assertEqual(decrypted_name, "John Doe")

    # def testEditHealthInformation(self):
    #     #self.database.insert_health_information("999", "Comments for patient with this ID.")
    #     self.database.edit_health_information("999", "different comments for patient with this ID")
    #     test21 = self.database.fetch_health_information_by_id(999)
    #     self.assertEqual(test21, (999, "different comments for patient with this ID"))

if __name__ == '__main__':
    unittest.main()