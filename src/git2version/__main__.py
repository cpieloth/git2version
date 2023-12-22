"""Entry point for package."""

import sys

import git2version.cmdline


def main():
    """Execute the CLI entry point."""
    return git2version.cmdline.main()


if __name__ == '__main__':
    sys.exit(main())
