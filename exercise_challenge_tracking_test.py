import unittest
from exercise_challenge_tracking import ExerciseTracker


class TestTracking(unittest.TestCase):
    def testProgress(self):
        tracker = ExerciseTracker("walking", 60)
        tracker.progress(5)
        self.assertEqual(tracker.currProgress, 5)
        self.assertNotEqual(tracker.currProgress, tracker.goal)
        self.assertRaises(ValueError, tracker.progress(-1))


if __name__ == "__main__":
    unittest.main()
