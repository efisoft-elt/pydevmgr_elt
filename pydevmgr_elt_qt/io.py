from pydevmgr_core.io import find_config
import importlib

pkg_name = "pydevmgr_elt_qt"


def get_pkg_path():
    return importlib.resources.files(pkg_name)


def find_ui(resource):
    try:
        return find_config(resource)
    except ValueError:
        pass
    pkg_path = get_pkg_path()
    path = pkg_path.joinpath("uis", resource)
    if not path.exists():
        raise IOError("coud not find ui file %r" % (resource))
    return str(path)
