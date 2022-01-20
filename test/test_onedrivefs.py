import os
import unittest
from uuid import uuid4

try:
    from fs.onedrivefs.onedrivefs import SubOneDriveFS
    from fs.test import FSTestCases
    from msgraphy.fs.onedrivefs import MSGraphyOneDriveFS
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass

TEST_URL = os.getenv('MSGRAPHYFS_TEST_URL')


@unittest.skipIf(TEST_URL is None, 'MSGRAPHYFS_TEST_URL not set')
class TestMSGraphyFS(FSTestCases, unittest.TestCase):

    def make_fs(self):
        drive, path = TEST_URL.split(":", 1)
        self.root_fs = MSGraphyOneDriveFS(f"{drive}:/", writeable=True)

        self.filename = f"{path}/unittest-{uuid4().hex}"

        print("Creating test directory", self.filename)
        self.root_fs.makedir(self.filename)

        return SubOneDriveFS(self.root_fs, self.filename)

    def destroy_fs(self, fs):
        print("Removing test directory", self.filename)
        self.root_fs.removetree(self.filename)
