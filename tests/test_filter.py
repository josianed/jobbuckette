import os
import unittest
import datetime

# Configure your app to use the testing configuration
if not "CONFIG_PATH" in os.environ:
    os.environ["CONFIG_PATH"] = "jobbuckette.config.TestingConfig"

import jobbuckette
from jobbuckette.filters import *

class FilterTests(unittest.TestCase):
    def test_date_format(self):
        date = datetime.date(1999, 12, 31)
        formatted = dateformat(date, "%d/%m/%Y")
        self.assertEqual(formatted, "31/12/1999")

    def test_date_format_none(self):
        formatted = dateformat(None, "%d/%m/%Y")
        self.assertEqual(formatted, None)

if __name__ == "__main__":
    unittest.main()
