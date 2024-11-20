"""
Test the calc module
"""

from django.test import SimpleTestCase

from app import calc

class TestCalc(SimpleTestCase):
    """Test the calc module"""

    def test_add_numbers(self):
        """Test that two numbers are added together"""
        res=calc.add(3, 6)
        self.assertEqual(res,9)

    def test_subtract_numbers(self):
        """Test that two numbers are subtracted"""
        res=calc.subtract(10, 15)
        self.assertEqual(res,5)

