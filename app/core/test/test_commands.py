from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db(self):
        """Test waiting for db"""

        class Getitem:
            def __init__(self):
                self.attempt = 0

            def __call__(self, item):
                if self.attempt < 5:
                    self.attempt += 1
                    raise OperationalError()
                else:
                    return True

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            getitem = Getitem()
            gi.side_effect = getitem
            call_command('wait_for_db')
            self.assertGreaterEqual(getitem.attempt, 5)
