import unittest
import os
from stegno import hide_message_in_image, reveal_message_from_image  # Make sure these functions are correctly defined in stegno.py

class TestSteganography(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Assuming your test image is in the 'tests' directory under your project
        cls.test_image_path = os.path.join(os.path.dirname(__file__), 'tests', 'test_image.png')
        cls.test_message = "Secret Message"

    def test_hide_and_reveal_message(self):
        # Use the class variable for the image path
        output_path = hide_message_in_image(TestSteganography.test_image_path, self.test_message)
        self.assertIsNotNone(output_path, "Hiding the message failed.")

        revealed_message = reveal_message_from_image(output_path)
        self.assertEqual(self.test_message, revealed_message, "The revealed message does not match the original.")

if __name__ == "__main__":
    unittest.main()
