import unittest
from exercise_challenge_tracking import ExerciseTracker


class TestTracking(unittest.TestCase):
    def testProgress(self):
        tracker = ExerciseTracker("walking", 60)
        tracker.progress(5)
        self.assertEqual(tracker.currProgress, 5)
        self.assertNotEqual(tracker.currProgress, tracker.goal)
        with self.assertRaises(ValueError):
            tracker.progress(-1)
        tracker.progress(55)
        self.assertTrue(tracker.goalReached())

    def testGoalReached(self):
        tracker = ExerciseTracker("walking", 60)
        tracker.progress(4)
        self.assertFalse(tracker.goalReached())
        tracker.progress(56)
        self.assertTrue(tracker.goalReached())

    def testResetProgress(self):
        tracker = ExerciseTracker("walking", 60)
        tracker.progress(5)
        tracker.resetProgress()
        self.assertEqual(tracker.currProgress, 0)

    def testNewGoal(self):
        tracker = ExerciseTracker("walking", 60)
        tracker.setNewGoal(50)
        self.assertEqual(tracker.goal, 50)
        with self.assertRaises(ValueError):
            tracker.setNewGoal(0)

    def testInit(self):
        with self.assertRaises(ValueError):
            ExerciseTracker("walking", -1)
        tracker = ExerciseTracker("walking", 60)
        self.assertIsNotNone(tracker)


if __name__ == "__main__":
    unittest.main()
