from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import CONFIG

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/log_file")
async def get_log_file(name: str | None = None):
    log_dir_path = Path(CONFIG.LOG.DIR)
    if name is None:
        name = str(Path(CONFIG.LOG.PATH).relative_to(log_dir_path))

    if isinstance(name, str):
        if name.startswith("../"):
            raise HTTPException(status_code=403, detail="Files in parent folders are forbidden.")

    log_path = log_dir_path / name

    if log_path.exists():
        # Set the Content-Length header based on the file size
        file_size = log_path.stat().st_size
        headers = {"Content-Length": str(file_size)}
        return FileResponse(log_path, headers=headers)
    else:
        raise HTTPException(status_code=404, detail="Log File not found.")


@router.get("/available_log_files")
async def get_available_log_files():
    log_dir_path = Path(CONFIG.LOG.DIR)
    return [x.name for x in log_dir_path.glob("*") if x.is_file()]
