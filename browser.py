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
            "--no-first-run",
            f"--disable-extensions-except={EXTENSION_DIR}",
            f"--load-extension={EXTENSION_DIR}",
        ],
    )

    _context = context

    await context.wait_for_event("page", timeout=20000)

    bg = None
    for page in context.pages:
        if "chrome-extension://" in page.url:
            bg = page
            break

    if not bg:
        raise Exception("MetaMask extension did not load")

    extension_id = bg.url.split("/")[2]

    for p in context.pages:
        try:
            await p.close()
        except:
            pass

    metamask = await context.new_page()

    await metamask.goto(
        f"chrome-extension://{extension_id}/home.html",
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
        return {"running": False}

    return {
        "running": True,
        "pages": len(_context.pages)
    }
