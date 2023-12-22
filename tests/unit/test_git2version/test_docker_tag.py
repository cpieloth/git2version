import unittest

import semver

from git2version import docker_tag

__author__ = 'christof.pieloth'


class DockerTagTestCase(unittest.TestCase):

    def test_tag_valid(self):
        tag = docker_tag.Tag(1, 2, 3)
        self.assertEqual('1.2.3', str(tag))

        tag = docker_tag.Tag(1, 2, 3, 'dev.1_build')
        self.assertEqual('1.2.3-dev.1_build', str(tag))

    def test_tag_invalid(self):
        # The tag must be valid ASCII and can contain lowercase and uppercase letters, digits, underscores, periods, and hyphens.
        # https://docs.docker.com/engine/reference/commandline/tag/

        with self.assertRaises(Exception) as _:
            docker_tag.Tag(1, 2, 3, 'ä')

        with self.assertRaises(Exception) as _:
            docker_tag.Tag(1, 2, 3, '+g23213')

        with self.assertRaises(Exception) as _:
            docker_tag.Tag(1, 2, 3, 'g23213+')

        with self.assertRaises(Exception) as _:
            docker_tag.Tag(1, 2, 3, 'g2+3213')

        with self.assertRaises(Exception) as _:
            docker_tag.Tag(1, 2, 3, '1~2')

    def test_from_semver_valid(self):
        version = semver.Version(1, 2, 3, 'dev.1', 'g123')
        tag = docker_tag.from_semver(version)
        self.assertEqual('1.2.3-dev.1-g123', str(tag))

    def test_from_semver_invalid(self):
        version = semver.Version(1, 2, 3, 'dev~2', 'g2')
        with self.assertRaises(Exception) as _:
            docker_tag.from_semver(version)

        version = semver.Version(1, 2, 3, 'dev~3', 'g3')
        with self.assertRaises(Exception) as _:
            docker_tag.from_semver(version)
