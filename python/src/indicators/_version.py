"""The package version, defined once.

The build reads this value (``[tool.setuptools.dynamic]`` in
``pyproject.toml``), and :mod:`indicators` re-exports it, so a release only
ever bumps the number in this one file.
"""

__version__ = "0.2.0"
