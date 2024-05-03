"""

Collects all router objects from *.py files in this directory into routers list.
The routers list is a convenient way to add all routes conveniently into the fastAPI app.

"""

import importlib
from pathlib import Path

from app.config import log

base_path = Path(__file__).parent

routers = []
for path_to_module in base_path.glob("**/*.py"):
    if path_to_module.stem[0] == "_":
        continue  # ignore sunder and dunder-files
    # adding all routers dynamically
    parent_name = path_to_module.relative_to(base_path).parent.name
    package = __name__ if parent_name == "" else ".".join([__name__, parent_name])

    log.info(f"adding router from {path_to_module.stem} to routers")
    router = importlib.import_module(f".{path_to_module.stem}", package=package)
    routers.append(router)
    log.info(f"added router from {path_to_module.stem} to routers")

log.info(f"loaded routers")


tags_metadata = [
    {
        "name": "latest",
        "description": "Endpoints that have already been converted to the latest version.",
    },
    {
        "name": "obsolete",
        "description": "Endpoints that are obsolete",
    },
    {
        "name": "service_name_xy",
        "description": "Routes used in xy.",
    },
    {"name": "todo", "description": "Endpoints that need to be removed or transferred to new framework"},
]

__all__ = ["routers", "tags_metadata"]
