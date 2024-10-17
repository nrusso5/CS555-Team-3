import unittest

#Import main medicine reminder functionality
from Nicholas_Russo_User_Story_Medicine_Reminders import *
from datetime import datetime


#Unit tests for the MedicineReminder class, as per Quiz 03
class TestMedicineReminder(unittest.TestCase):
    
    #Setting up the unit test environment
    def setUp(self):
        #Creating an instance of MedicineReminder for each test. MedicineReminder class defined in other file.
        self.reminder = MedicineReminder()

    #TEST 1: Testing a scheduled reminder
    def test_reminder_at_scheduled_time(self):
        #Avoiding timedelta here due to bugs. datetime.now works
        time_to_remind = datetime.now().replace(second=0, microsecond=0)

        #Testing with an arbitrary medicine
        self.reminder.configure_schedule(time_to_remind, "blood pressure medicine")
        
        #---Affirm that the reminder is given at the scheduled time
        result = self.reminder.check_and_remind(time_to_remind)

        #Make sure the reminder is good
        self.assertEqual(result, "Reminder: It's time to take your blood pressure medicine.")

        #And make sure the time matches what it should be
        self.assertEqual(self.reminder.last_reminded_time, time_to_remind)

    
    #TEST 2: Testing a reminder time disparity
    def test_no_reminder_at_different_time(self):

        #Using a different test medicine from before
        time_to_remind = datetime.now().replace(second=0, microsecond=0)
        self.reminder.configure_schedule(time_to_remind, "cholesterol medicine")

        #Test that no reminder is given at a different time
        #Manually adjusting the minutes without timedelta (caused bugs in test file, not original code)
        new_minute = (time_to_remind.minute + 5) % 60 #Incrementing
        different_time = time_to_remind.replace(minute=new_minute)

        #Update the current hour if needed due to the minute increment
        if new_minute < time_to_remind.minute:
            different_time = different_time.replace(hour=(time_to_remind.hour + 1) % 24)

        #------Core of the test
        result = self.reminder.check_and_remind(different_time)
        #Check that the absence of reminders (intended behavior) is present
        self.assertEqual(result, "No reminders at this time.")

        #Check that reminder hasn't reminded
        self.assertIsNone(self.reminder.last_reminded_time)


#---------Run the tests---------

#Run the unit tests
if __name__ == "__main__":
    unittest.main()


