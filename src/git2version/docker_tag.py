import logging
import os
import re

import semver
from dataclasses import dataclass
from typing import Optional

from git2version import semantic_version


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Tag:
    major: int
    minor: int
    patch: int
    additional: Optional[str] = None

    def __post_init__(self):
        # check for special character
        #
        # The tag must be valid ASCII and can contain lowercase and uppercase letters, digits, underscores, periods, and hyphens.
        # https://docs.docker.com/engine/reference/commandline/tag/
        if not self.additional:
            return

        if not self.additional.isascii():
            raise ValueError(f'Invalid additional, contains non-ASCII character: {self.additional}')

        for c in self.additional:
            if not c.isalpha() and not c.isdigit() and c not in ['_', '-', '.']:
                raise ValueError(f'Invalid additional, allowed [a-z, A-Z, 0-9, -, _, .]: {self.additional}')

    def __str__(self) -> str:
        additional = f'-{self.additional}' if self.additional else ''
        return f'{self.major}.{self.minor}.{self.patch}{additional}'

    @classmethod
    def is_valid(cls, tag: str) -> bool:
        try:
            pattern = re.compile(r'(\d+.\d+.\d+)(.*)')
            match = pattern.match(tag)
            if not match:
                return False

            major, minor, patch = match.group(1).split('.')
            additional = match.group(2) if match.lastindex == 2 else None

            cls(major, minor, patch, additional)
            return True
        except Exception as ex:
            logger.debug(str(ex))
            return False


def from_git(repo: os.path):
    version = semantic_version.from_git(repo)
    return from_semver(version)


def from_semver(version: semver.Version) -> Tag:
    prerelease = version.prerelease.replace('+', '-') if version.prerelease else ''
    build = version.build.replace('+', '-') if version.build else ''

    additional = f'{prerelease}-{build}'.strip('-')
    additional = additional if additional else None

    return Tag(major=version.major, minor=version.minor, patch=version.patch, additional=additional)
