from datetime import datetime

# Primary class for the habit reminder, corresponding to Alexa intent and behavior
class HabitReminder:
    def __init__(self):
        # Stores habit names and time
        self.habit_schedule = {}  
        
        # No reminder occurred yet
        self.last_reminded_time = None

    # Configures schedule for habits
    def configure_schedule(self, time, habit_name):
        self.habit_schedule[time] = habit_name

    # Core check and remind function
    def check_and_remind(self, current_time):
        # Check if the current time matches scheduled time for any habit
        if current_time in self.habit_schedule:
            # Update the last reminded time to right now
            self.last_reminded_time = current_time

            # Define reminder result string
            reminder_result = ""

            # Assign its value
            reminder_result = f"Reminder: It's time to {self.habit_schedule[current_time]}."

            # Return it
            return reminder_result
        
        else:   # Not time to remind
            return "No reminders at this time."
