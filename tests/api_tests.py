import unittest
import os
import shutil
import json
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility
from io import StringIO

import sys; print(list(sys.modules.keys()))
# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "mainapp.config.TestingConfig"

from mainapp.main import app
from mainapp import models
from mainapp.utils import upload_path



class TestAPI(unittest.TestCase):
    """ Tests for the API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()


        # Create folder for test uploads
        os.mkdir(upload_path())

    def tearDown(self):
        """ Test teardown """

        # Delete test upload folder
        shutil.rmtree(upload_path())


