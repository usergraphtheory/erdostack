"""Build hook: bundle the repo-root skills/ and references/ into the wheel.

The skills live at the repository root so every host (plugins, the skills CLI,
npm) reads the same markdown. The Python package needs its own copy inside the
wheel, so build_py copies them to erdostack/_bundle/ at build time.
All metadata lives in pyproject.toml.
"""

import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py

ROOT = Path(__file__).parent.resolve()
BUNDLED = ("skills", "references")


class BuildWithBundle(build_py):
    def run(self):
        super().run()
        target = Path(self.build_lib) / "erdostack" / "_bundle"
        for name in BUNDLED:
            source = ROOT / name
            if not source.is_dir():
                continue
            destination = target / name
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(source, destination)


setup(cmdclass={"build_py": BuildWithBundle})
