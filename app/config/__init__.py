import datetime as dt
import logging
from pathlib import Path

from omegaconf import OmegaConf

base_conf = OmegaConf.load(Path(__file__).parent.resolve() / "base.yml")
local_config_file = Path(__file__).parent.resolve() / "local.yml"
if not local_config_file.exists():
    raise FileNotFoundError(
        f"Please create a local configuration file: " f" {str(local_config_file.parent.name)}/{local_config_file.name}"
    )
local_conf = OmegaConf.load(local_config_file)
CONFIG = OmegaConf.merge(base_conf, local_conf)

project_root_dir = Path(__file__).parents[2].resolve()
if not CONFIG.get("LOG").get("NAME"):
    raise ValueError("no LOG.NAME provided, please set LOG.NAME in config")

if not CONFIG.get("LOG").get("DIR"):
    # no instructions, fallback to default
    path_to_log_dir = project_root_dir / "_logs"
else:
    conf_path = Path(CONFIG.LOG.DIR)

    if conf_path.anchor:
        # fully qualified path
        path_to_log_dir = conf_path
    else:
        # relative path
        path_to_log_dir = project_root_dir / CONFIG.LOG.DIR

CONFIG.LOG.NAME = f"{dt.datetime.now():%Y%m%dT%H%M%S}_{CONFIG.LOG.NAME}"
CONFIG.LOG.PATH = str(path_to_log_dir / CONFIG.LOG.NAME)
CONFIG.LOG.DIR = str(path_to_log_dir)

logging.basicConfig(filename=CONFIG.LOG.PATH, encoding='utf-8', level=logging.DEBUG)
log = logging.getLogger(__name__)
log.info(f"Setting up logger")
log.debug(f"Log path is {CONFIG.LOG.PATH}")
log.info("Logging is initialized: Hello!")