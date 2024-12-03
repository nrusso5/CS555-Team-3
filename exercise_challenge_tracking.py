class ExerciseTracker:
    def __init__(self, exercise: str, goal: int) -> None:
        # initialize the tracker
        if goal <= 0:
            raise ValueError("goal has to be > 0")
        if exercise == "":
            raise ValueError("exercise is empty")
        self.exercise = exercise
        self.goal = goal
        self.currProgress = 0

    def progress(self, progression: int) -> None:
        # update the user's progress
        if progression <= 0:
            raise ValueError("goal has to be > 0")
        self.currProgress += progression

    def goalReached(self) -> None:
        # inform the user that they have reached their goal and
        if self.currProgress == self.goal:
            self.resetProgress()
            return True
        else:
            return False

    def setNewGoal(self, goal: int) -> None:
        # set a new goal
        if goal <= 0:
            raise ValueError("goal has to be > 0")
        self.goal = goal

    def resetProgress(self) -> None:
        # reset progress(helper for goal reached)
        self.currProgress = 0
