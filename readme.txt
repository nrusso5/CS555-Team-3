Current Slot Types:
  AMAZON.TIME
		Use Case:
		-	BUILT IN
		Slots Using:
		-	returnInfoandDeleteHabit
		- returnInfoandAddHabit
		- returnInfoandDeleteMedicine
		- returnInfoandAddMedicine
  exercise
		Use Case:
		-	walking
		- running
		- yoga
		- etc.
		Slots Using:
		- returnInfoAndAddExerciseChallenge
  goal
		Use Case:
		- 40 minutes
		- 10 minutes
		- 60 minutes
		- etc.
		Slots Using:
  habit
		Use Case:
		-	go to the gym
		- do breathing exercise
		- drink water
		- stand
		- run
		- walk
		Slots Using:
  medicine
  	Use Case:
		- pain killers
		- iron supplements
		- aspirin
		- tylenol
		- liquids
		- injections
		- topical
		- tablets
		- pills
		Slots Using:
		- returnInfoandDeleteMedicine
		- returnInfoandAddMedicine
  progress
    Use Case:
		- 30 minutes
		Slots Using:
		- returnInfoAndProgressExerciseChallenge

To add more intents (using python), you need to:
	(Optional) Create Slot Types
	1. Create the intent for the class you plan to make (usually the same name as the actual class)
	2. Assign usable slot types to the intent
			- While in the intent screen, add the slot types to the intent slots
			- You also have to change the sample utterance(s) to the format of the user input, so in the example of the intent returnInfoandAddMedicine
				=> add medicine reminder {medicine} at {time}
				=> add medicine {medicine} at {time}
	3. Create the class type in the lambda_function.py file
	4. Request the handler
			Ex. sb.add_request_handler({name of class}())
	
      
