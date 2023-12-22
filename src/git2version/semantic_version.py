import logging
import os.path

import semver

from git2version import git_version


logger = logging.getLogger(__name__)


PRE_RELEASE_BRANCHES = ['main', 'master']
PREFIX_RELEASE_BRANCH = 'release'


def from_git(repo: os.path):
    return from_git_info(git_version.from_repository(repo))


def from_git_info(gversion: git_version.Version) -> semver.Version:
    if gversion.tags:
        if len(gversion.tags) > 1:
            logger.warning('More than one tag available, using first of: %s', gversion.tags)
        return semver.Version.parse(gversion.tags[0])

    prerelease = f'pre.{gversion.additional_commits}' \
        if gversion.branch in PRE_RELEASE_BRANCHES or gversion.branch.startswith(PREFIX_RELEASE_BRANCH)\
        else f'dev.{gversion.additional_commits}'
    build = f'g{gversion.sha1}'

    if gversion.recent_tags:
        if len(gversion.recent_tags) > 1:
            logger.warning('More than one recent_tags available, using first of: %s', gversion.recent_tags)

        sversion = semver.Version.parse(gversion.recent_tags[0]).bump_patch()
        sversion = semver.Version(sversion.major, sversion.minor, sversion.patch, prerelease, build)

        return sversion

    return semver.Version(0, 0, 0, prerelease, build)
