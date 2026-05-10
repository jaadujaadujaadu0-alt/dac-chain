import os
from playwright.async_api import async_playwright
from config import EXTENSION_DIR, USER_DATA_DIR, DISPLAY, APP_URL

_playwright = None
_context = None


async def boot_browser():
    global _playwright, _context

    if _context:
        return _context

    os.environ["DISPLAY"] = DISPLAY

    if _playwright is None:
        _playwright = await async_playwright().start()

    context = await _playwright.chromium.launch_persistent_context(
        USER_DATA_DIR,
        headless=False,
        chromium_sandbox=False,
        timeout=120000,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            f"--disable-extensions-except={EXTENSION_DIR}",
            f"--load-extension={EXTENSION_DIR}",
        ],
    )

    _context = context

    await context.new_page()
    return context


async def get_context():
    if _context is None:
        raise Exception("Call /boot first")
    return _context


async def browser_status():
    if _context is None:
        return {"running": False}
    return {"running": True}
