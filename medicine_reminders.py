from datetime import datetime
import unittest

#Primary class for the medicine reminder, corresponding to Alexa intent and behavior
class MedicineReminder:
    def __init__(self):
        #Stores medication names and time
        self.medicine_schedule = {}  
        
        #No remind occured yet
        self.last_reminded_time = None

    #Config schedule, as needed
    def configure_schedule(self, time, medication_name):
        self.medicine_schedule[time] = medication_name


    #Core check and remind function
    def check_and_remind(self, current_time):
        #Check if the current time matches scheduled time for any medication
        if current_time in self.medicine_schedule:
            #Update the last reminded time to right now
            self.last_reminded_time = current_time

            #Define reminder result string
            reminder_result = ""

            #Assign its value
            reminder_result = f"Reminder: It's time to take your {self.medicine_schedule[current_time]}."

            #Return it
            return reminder_result
        
        else:   #Not time to remind
            #May make null
            return "No reminders at this time."
