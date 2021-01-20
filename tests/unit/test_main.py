"""
Tests functions in main
"""
import os
import unittest

from dotenv import load_dotenv
from main import Yasna, Status

class TestMain(unittest.TestCase):
    """
    Suit cases to test main.py
    """

    def setUp(self):
        """
        Setup variables for unit testing
        """
        self.yasna = Yasna()

    def test_status_enum(self):
        """
        Test success Enum
        """
        success = "#36B37E"
        fail = "#FF5630"

        self.assertEqual(Status["success"].value, success)
        self.assertEqual(Status["fail"].value, fail)
