"""Models for YandexApi."""
#
# import pkgutil
# from pathlib import Path
#
from YandexApi.db.models.node import Node

#
#
# def load_all_models() -> None:
#     """Load all models from this folder."""
#     package_dir = Path(__file__).resolve().parent
#     modules = pkgutil.walk_packages(
#         path=[str(package_dir)],
#         prefix="backend.db.models.",
#     )
#     for module in modules:
#         __import__(module.name)  # noqa: WPS421
#

__models__ = [
    Node,
]
