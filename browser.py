import os
from playwright.async_api import async_playwright
from config import EXTENSION_DIR, USER_DATA_DIR, CDP_PORT, DISPLAY, APP_URL

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
        channel="chromium",
        headless=False,
        chromium_sandbox=False,
        timeout=120000,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            f"--remote-debugging-port={CDP_PORT}",
            f"--disable-extensions-except={EXTENSION_DIR}",
            f"--load-extension={EXTENSION_DIR}",
        ],
    )

    _context = context

    page = context.pages[0] if context.pages else await context.new_page()

    await page.goto(
        APP_URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    await page.bring_to_front()

    return _context


async def get_context():
    global _context

    if _context is None:
        raise Exception("Browser not started. Call /boot first.")

    return _context


async def browser_status():
    global _context

    if _context is None:
        return {
            "running": False,
            "error": "browser not started"
        }

    return {
        "running": True,
        "pages": len(_context.pages)
    }