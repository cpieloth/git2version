from dataclasses import dataclass, field
import logging
import os
import re
import subprocess
from typing import List


__author__ = 'Christof Pieloth'


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Version:
    sha1: str
    branch: str
    tags: List[str] = field(default_factory=list)
    recent_tags: List[str] = field(default_factory=list)
    additional_commits: int = 0


def from_repository(repo: os.path) -> Version:
    git_cmd = 'git'

    if subprocess.call([git_cmd, '--version'], stdout=subprocess.PIPE) != 0:
        raise OSError(f'Command not available: {git_cmd}')

    if not os.access(repo, os.R_OK):
        raise PermissionError(f'No read access to: {repo}')

    recent_tags = []
    additional_commits = 0

    sha1 = subprocess.check_output([git_cmd, 'rev-parse', '--short', 'HEAD'], cwd=repo).decode('utf-8').strip()
    branch = subprocess.check_output([git_cmd, 'branch', '--show-current'], cwd=repo).decode('utf-8').strip()
    tags = subprocess.check_output([git_cmd, 'tag', '--list', '--points-at', sha1], cwd=repo).decode('utf-8')
    tag_list = list(filter(bool, tags.split('\n')))

    if tag_list:
        return Version(sha1=sha1, branch=branch, tags=tag_list, recent_tags=recent_tags, additional_commits=additional_commits)

    try:
        describe = subprocess.check_output([git_cmd, 'describe', '--tags'], cwd=repo).decode('utf-8')
        pattern = re.compile(r'(.+)-(\d+)-(.+)')
        match = pattern.match(describe)
        if match:
            recent_tags = [match.group(1)]
            additional_commits = int(match.group(2))
        else:
            logger.debug('Could not parse git-describe output: %s', describe)
    except Exception as ex:  # pylint: disable=broad-exception-caught
        logger.debug('Error calling git-describe: %s', ex)

    return Version(sha1=sha1, branch=branch, tags=tag_list, recent_tags=recent_tags, additional_commits=additional_commits)
