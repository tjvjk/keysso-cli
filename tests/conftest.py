"""Pytest hooks for keysso-cli tests."""

from __future__ import annotations

import logging


def pytest_configure() -> None:
    """Disable logging in tests."""
    logging.disable(logging.CRITICAL)
