# git2version

Generate a semantic version based on git.

Command line usage:

```shell
$  git2version semver
1.0.1-pre.121+gc26e6ca
```

Python API usage:

```python
import os

from git2version import semantic_version

version = semantic_version.from_git(os.getcwd())
print(version)
```

For more information read the documentation located in [docs/](docs/).
