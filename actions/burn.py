from browser import get_context
from helpers import click_any, approve_metamask, wait_for_popup


async def run(amount: str):
    context = await get_context()
    page = await context.new_page()

    await page.goto(
        "https://inception.dachain.io/exchange",
        wait_until="domcontentloaded",
        timeout=60000
    )

    await page.wait_for_timeout(5000)

    input_box = page.locator('input[placeholder="0.0"]').first

    await input_box.click()
    await input_box.fill("")
    await input_box.type(amount)

    await page.wait_for_timeout(2000)

    clicked = await click_any(page, [
        f"BURN FOR {amount}",
        "Burn"
    ], 10000)

    if not clicked:
        raise Exception("Burn button not found")

    popup = await wait_for_popup(context)
    await approve_metamask(popup)

    return {"success": True}