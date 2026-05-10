import os
from playwright.async_api import async_playwright
from config import EXTENSION_DIR, USER_DATA_DIR, DISPLAY

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
            "--disable-blink-features=AutomationControlled",
            f"--disable-extensions-except={EXTENSION_DIR}",
            f"--load-extension={EXTENSION_DIR}",
            "--no-first-run",
        ],
    )

    _context = context

    # close junk tabs
    for p in context.pages:
        try:
            await p.close()
        except:
            pass

    # open metamask directly
    metamask = await context.new_page()
    await metamask.goto(
        "chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html",
        wait_until="domcontentloaded",
        timeout=60000
    )

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
