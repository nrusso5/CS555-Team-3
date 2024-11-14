class ExerciseTracker:
    def __init__(self, exercise: str, goal: int) -> None:
        if goal <= 0:
            raise ValueError("goal has to be > 0")
        self.exercise = exercise
        self.goal = goal
        self.currProgress = 0

    def progress(self, progression: int) -> None:
        if progression <= 0:
            raise ValueError("goal has to be > 0")
        self.currProgress += progression

    def goalReached(self) -> None:
        if self.currProgress == self.goal:
            self.resetProgress()
            return True
        else:
            return False

    def setNewGoal(self, goal: int) -> None:
        if goal <= 0:
            raise ValueError("goal has to be > 0")
        self.goal = goal

    def resetProgress(self) -> None:
        self.currProgress = 0
