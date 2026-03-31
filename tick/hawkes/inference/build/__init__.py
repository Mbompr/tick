# License: BSD 3 clause

"""Import shim for :mod:`tick.hawkes.inference.build`."""

from importlib import import_module, machinery, util
from pathlib import Path
import sys

from tick.base.opsys import add_to_path_if_windows

add_to_path_if_windows(__file__)


def _load_hawkes_inference_module():
    module_name = __name__ + ".hawkes_inference"
    try:
        return import_module(".hawkes_inference", __name__)
    except ImportError as exc:
        package_dir = Path(__file__).resolve().parent
        repo_root = package_dir.parents[3]
        suffixes = machinery.EXTENSION_SUFFIXES

        for build_root in (repo_root / "_skbuild", repo_root / "build", repo_root):
            if build_root != repo_root and not build_root.exists():
                continue
            for suffix in suffixes:
                for candidate in sorted(
                        build_root.rglob(f"hawkes_inference*{suffix}")):
                    if candidate.name.startswith("hawkes_inference"):
                        spec = util.spec_from_file_location(module_name, candidate)
                        if spec is None or spec.loader is None:
                            continue
                        module = util.module_from_spec(spec)
                        sys.modules[module_name] = module
                        spec.loader.exec_module(module)
                        return module
        raise exc


_hawkes_inference = _load_hawkes_inference_module()
__all__ = [name for name in getattr(_hawkes_inference, "__all__",
                                    dir(_hawkes_inference))
           if not name.startswith("_")]

for _name in __all__:
    globals()[_name] = getattr(_hawkes_inference, _name)

del _hawkes_inference
