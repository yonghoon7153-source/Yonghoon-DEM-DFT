"""Runtime configuration.  Everything is overridable by environment variable."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def _path(name: str, default: Path) -> Path:
    return Path(os.environ.get(name, default)).expanduser().resolve()


#: The one address people type.  In development Vite listens here and proxies
#: /api to the backend; in `make serve` the backend listens here and serves the
#: built frontend itself.  Either way the bookmark is the same.
DEFAULT_PORT = 5003
#: Where the backend listens during development, behind Vite's proxy.
DEFAULT_API_PORT = 8000


@dataclass
class Settings:
    data_dir: Path = field(default_factory=lambda: _path("WORKBENCH_DATA", REPO_ROOT / "data"))
    database_url: str = ""
    port: int = int(os.environ.get("WORKBENCH_PORT", DEFAULT_PORT))
    api_port: int = int(os.environ.get("WORKBENCH_API_PORT", DEFAULT_API_PORT))
    #: Rejecting oversized uploads early keeps a stray file from filling the disk.
    max_upload_bytes: int = int(os.environ.get("WORKBENCH_MAX_UPLOAD_MB", "512")) * 1024 * 1024
    #: Points per curve sent to the browser; the server downsamples to this.
    default_plot_points: int = int(os.environ.get("WORKBENCH_PLOT_POINTS", "1200"))
    #: Shared password.  Empty means there is no door at all -- which is the
    #: normal state on a lab network.  `bml share` sets it before opening a
    #: tunnel, and refuses to open one without it (ADR 0014).
    password: str = os.environ.get("WORKBENCH_PASSWORD", "").strip()
    #: Only needed in development, where the browser talks to Vite on one port
    #: and could reach the API on another.  `make serve` is single-origin, so
    #: none of this applies there.
    cors_origins: tuple[str, ...] = tuple(
        origin.strip() for origin in os.environ.get(
            "WORKBENCH_CORS",
            f"http://localhost:{DEFAULT_PORT},http://127.0.0.1:{DEFAULT_PORT},"
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",") if origin.strip()
    )

    def __post_init__(self) -> None:
        if not self.database_url:
            self.database_url = os.environ.get(
                "WORKBENCH_DB", f"sqlite:///{self.data_dir / 'workbench.db'}")

    @property
    def web_dist(self) -> Path:
        """The built frontend, when there is one."""
        return _path("WORKBENCH_WEB_DIST", REPO_ROOT / "apps/web/dist")

    @property
    def uploads_dir(self) -> Path:
        return self.data_dir / "uploads"

    @property
    def runs_dir(self) -> Path:
        return self.data_dir / "runs"

    def ensure_dirs(self) -> None:
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        self.runs_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
