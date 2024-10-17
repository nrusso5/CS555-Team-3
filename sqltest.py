import unittest
import mysql.connector
from sql import mySQLdb

class testMySQLDatabase(unittest.TestCase):
    @classmethod 
    def setUpClass(cls):
        cls.database = mySQLdb('--', '--', '--!', '--')


    def testInsertAndFetchContact(self):
        self.database.insert_contact_info("John Doe", "1005556666")
        test1 = self.database.fetch_contact_by_id(1)
        self.assertEqual(test1[0], (1, "John Doe", "1005556666"))

    def testInsertAndFetchHealth(self):
        self.database.insert_health_information("999", "Comments for patient with this ID.")
        test2 = self.database.fetch_health_information_by_id(999)
        self.assertEqual(test2[0], (999, "Comments for patient with this ID."))

if __name__ == '__main__':
    unittest.main()