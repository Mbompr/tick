# License: BSD 3 clause

# Templating update - 19/02/2018
#  Importing DLLs has gotten a bit strange and now requires
#  updating the path for DLLs to be found before hand

import importlib
import importlib.machinery
import importlib.util
import sys
from pathlib import Path

from tick.base.opsys import add_to_path_if_windows

add_to_path_if_windows(__file__)


def _load_extension(module_name):
    try:
        module = importlib.import_module(f".{module_name}", __name__)
    except ImportError:
        package_dir = Path(__file__).resolve().parent
        repo_root = package_dir.parents[2]
        relative_build_dir = package_dir.relative_to(repo_root)
        for candidate in sorted(
                (repo_root / "build").glob(f"*/{relative_build_dir}/{module_name}*")):
            if not candidate.is_file():
                continue
            if not any(str(candidate).endswith(suffix)
                       for suffix in importlib.machinery.EXTENSION_SUFFIXES):
                continue
            qualified_name = f"{__name__}.{module_name}"
            spec = importlib.util.spec_from_file_location(qualified_name,
                                                          candidate)
            if spec is None or spec.loader is None:
                continue
            module = importlib.util.module_from_spec(spec)
            sys.modules[qualified_name] = module
            spec.loader.exec_module(module)
            break
        else:
            raise
    globals()[module_name] = module
    return module


base = _load_extension("base")
