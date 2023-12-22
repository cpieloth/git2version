"""Module for command line interface implementation."""

import abc
import argparse
import logging
import os
import semver
import sys

from git2version import git_version, docker_tag
from git2version import semantic_version


class SubCommand(abc.ABC):
    """
    Abstract base class for sub commands.

    A new sub command can be added by calling the init_subparser().
    """

    @classmethod
    @abc.abstractmethod
    def _name(cls):
        """
        Return name of the command.

        :return: Command name
        :rtype: str
        """
        raise NotImplementedError()

    @classmethod
    def _help(cls):
        """
        Return help description.

        :return: Help description
        :rtype: str
        """
        return cls.__doc__

    @classmethod
    @abc.abstractmethod
    def _add_arguments(cls, parser):
        """
        Initialize the argument parser and help for the specific sub-command.

        Must be implemented by a sub-command.

        :param parser: A parser.
        :type parser: argparse.ArgumentParser
        :return: void
        """
        raise NotImplementedError()

    @classmethod
    def init_subparser(cls, subparsers):
        """
        Initialize the argument parser and help for the specific sub-command.

        :param subparsers: A subparser.
        :type subparsers: argparse.ArgumentParser
        :return: void
        """
        parser = subparsers.add_parser(cls._name(), help=cls._help())
        cls._add_arguments(parser)
        parser.set_defaults(func=cls.execute)

    @classmethod
    @abc.abstractmethod
    def execute(cls, args):
        """
        Execute the command.

        Must be implemented by a sub-command.

        :param args: argparse arguments.
        :return: 0 on success.
        """
        raise NotImplementedError()


class GitVersionCmd(SubCommand):
    """Prints version information from git."""

    @classmethod
    def _name(cls):
        return 'git-version'

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument('-d', '--directory', help='Directory inside a git repository.', default=os.getcwd())
        return parser

    @classmethod
    def execute(cls, args):
        """Execute the command."""
        try:
            info = git_version.from_repository(args.directory)
            print(info)
            return 0
        except Exception as ex:  # pylint: disable=broad-exception-caught
            print(ex, file=sys.stderr)
            return 1


class SemverCmd(SubCommand):
    """Get semver version based on git-info."""

    @classmethod
    def _name(cls):
        return 'semver'

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument('-d', '--directory', help='Directory inside a git repository.', default=os.getcwd())
        return parser

    @classmethod
    def execute(cls, args):
        """Execute the command."""
        try:
            version = semantic_version.from_git(args.directory)
            print(version)
            return 0
        except Exception as ex:  # pylint: disable=broad-exception-caught
            print(ex, file=sys.stderr)
            return 1


class SemverCheckCmd(SubCommand):
    """Checks if a string is a valid semver version."""

    @classmethod
    def _name(cls):
        return 'semver-check'

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument('version', help='Version to check.')
        return parser

    @classmethod
    def execute(cls, args):
        """Execute the command."""
        if semver.Version.is_valid(args.version):
            print(f'Valid version: {args.version}')
            return 0
        else:
            print(f'Invalid version: {args.version}')
            return 1


class DockerTagCmd(SubCommand):
    """Get docker tag based on git-info."""

    @classmethod
    def _name(cls):
        return 'docker-tag'

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument('-d', '--directory', help='Directory inside a git repository.', default=os.getcwd())
        return parser

    @classmethod
    def execute(cls, args):
        """Execute the command."""
        try:
            version = docker_tag.from_git(args.directory)
            print(version)
            return 0
        except Exception as ex:  # pylint: disable=broad-exception-caught
            print(ex, file=sys.stderr)
            return 1


class DockerTagCheckCmd(SubCommand):
    """Checks if a string is a valid docker tag."""

    @classmethod
    def _name(cls):
        return 'docker-tag-check'

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument('tag', help='Version to check.')
        return parser

    @classmethod
    def execute(cls, args):
        """Execute the command."""
        if docker_tag.Tag.is_valid(args.tag):
            print(f'Valid version: {args.tag}')
            return 0
        else:
            print(f'Invalid version: {args.tag}')
            return 1


def main(argv=None):
    """
    Start the Example tool.

    :return: 0 on success.
    """
    if not argv:
        argv = sys.argv

    # Init logging for CLI
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING, stream=sys.stderr)

    # Parse arguments
    parser = argparse.ArgumentParser(prog=argv[0])

    subparser = parser.add_subparsers(title='git2version Commands', description='Valid git2version commands.')
    GitVersionCmd.init_subparser(subparser)
    SemverCmd.init_subparser(subparser)
    SemverCheckCmd.init_subparser(subparser)
    DockerTagCmd.init_subparser(subparser)
    DockerTagCheckCmd.init_subparser(subparser)

    args = parser.parse_args(argv[1:])
    try:
        # Check if a sub-command is given, otherwise print help.
        getattr(args, 'func')
    except AttributeError:
        parser.print_help()
        return 2

    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
