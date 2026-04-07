# License: BSD 3 clause

import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from tick.base import opsys


class Test(unittest.TestCase):
    def test_build_loader_prefers_local_extension_candidates(self):
        active_suffix = max(opsys.importlib.machinery.EXTENSION_SUFFIXES,
                            key=len)
        wrong_suffix = ".cpython-bad.so"

        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = (Path(tmpdir) / "repo").resolve()
            package_dir = repo_root / "tick" / "base" / "build"
            wrong = repo_root / "_skbuild" / "abi" / "tick" / "base" / "build" / (
                f"base{wrong_suffix}"
            )
            right = repo_root / "_skbuild" / "abi" / "tick" / "base" / "build" / (
                f"base{active_suffix}"
            )
            wrong.parent.mkdir(parents=True, exist_ok=True)
            right.parent.mkdir(parents=True, exist_ok=True)
            wrong.write_text("wrong")
            right.write_text("right")

            chosen = []

            class Loader:
                def exec_module(self, module):
                    module.marker = "loaded"

            with mock.patch.dict(sys.modules, {}, clear=False), \
                 mock.patch.object(
                     opsys.importlib, "import_module",
                     side_effect=AssertionError("local build should win")), \
                 mock.patch.object(
                     opsys.importlib.util, "spec_from_file_location",
                     side_effect=lambda name, candidate: (
                         chosen.append(candidate),
                         types.SimpleNamespace(loader=Loader()))[1]), \
                 mock.patch.object(
                     opsys.importlib.util, "module_from_spec",
                     return_value=types.SimpleNamespace()):
                module = opsys.load_extension("base", "tick.base.build",
                                              str(package_dir / "__init__.py"),
                                              repo_root=repo_root)

            self.assertEqual([path.resolve() for path in chosen],
                             [right.resolve()])
            self.assertEqual(module.marker, "loaded")

    def test_build_loader_does_not_swallow_other_missing_modules(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = (Path(tmpdir) / "repo").resolve()
            package_dir = repo_root / "tick" / "base" / "build"
            package_dir.mkdir(parents=True, exist_ok=True)

            with mock.patch.object(opsys.importlib, "import_module",
                                   side_effect=ModuleNotFoundError(
                                       "missing dependency", name="numpy")):
                with self.assertRaises(ModuleNotFoundError) as ctx:
                    opsys.load_extension("base", "tick.base.build",
                                         str(package_dir / "__init__.py"),
                                         repo_root=repo_root)

        self.assertEqual(ctx.exception.name, "numpy")


if __name__ == "__main__":
    unittest.main()
