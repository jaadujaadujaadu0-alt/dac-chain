from browser import get_context
from config import CRATE_URL
from helpers import click_any


async def run():
    context = await get_context()

    page = await context.new_page()

    await page.goto(
        CRATE_URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    await page.wait_for_timeout(5000)

    free_clicked = await click_any(page, [
        "OPEN FREE",
        "Open Free"
    ], 10000)

    if not free_clicked:
        raise Exception("OPEN FREE button not found")

    await page.wait_for_timeout(3000)

    open_clicked = await click_any(page, [
        "OPEN FOR 150 QE",
        "OPEN FOR"
    ], 10000)

    if not open_clicked:
        raise Exception("OPEN FOR 150 QE button not found")

    return {
        "success": True,
        "action": "crate"
    }