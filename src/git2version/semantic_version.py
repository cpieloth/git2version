import logging
import os.path
import semver

from git2version import git_version


logger = logging.getLogger(__name__)


PRE_RELEASE_BRANCHES = ['main', 'master']
PREFIX_RELEASE_BRANCH = 'release'


def from_git(repo: os.path):
    return from_git_info(git_version.from_repository(repo))


def from_git_info(git_version: git_version.Version) -> semver.Version:
    if git_version.tags:
        if len(git_version.tags) > 1:
            logger.warning('More than one tag available, using first of: %s', git_version.tags)
        return semver.Version.parse(git_version.tags[0])

    prerelease = f'pre.{git_version.additional_commits}' if git_version.branch in PRE_RELEASE_BRANCHES or git_version.branch.startswith(PREFIX_RELEASE_BRANCH) else f'dev.{git_version.additional_commits}'
    build = f'g{git_version.sha1}'

    if git_version.recent_tags:
        if len(git_version.recent_tags) > 1:
            logger.warning('More than one recent_tags available, using first of: %s', git_version.recent_tags)

        version = semver.Version.parse(git_version.recent_tags[0]).bump_patch()
        version = semver.Version(version.major, version.minor, version.patch, prerelease, build)

        return version

    return semver.Version(0, 0, 0, prerelease, build)
