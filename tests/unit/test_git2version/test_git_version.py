import os
import unittest

from git2version import git_version

__author__ = 'christof.pieloth'


class GitVersionTestCase(unittest.TestCase):

    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), '..', 'fixtures')
    TEST_REPO_DIR = os.path.join(FIXTURES_DIR, 'test_repo')

    def test_version(self):
        test_repo_info = git_version.Version(sha1='acc33eb', branch='test')
        info = git_version.from_repository(self.TEST_REPO_DIR)
        self.assertEqual(info, test_repo_info)
