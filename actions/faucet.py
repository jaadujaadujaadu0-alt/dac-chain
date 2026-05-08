from browser import get_context
from helpers import click_any, approve_metamask, wait_for_popup


async def run():
    context = await get_context()
    page = await context.new_page()

    await page.goto(
        "https://inception.dachain.io/faucet",
        wait_until="domcontentloaded",
        timeout=60000
    )

    await page.wait_for_timeout(5000)

    clicked = await click_any(page, [
        "CLAIM TESTNET DACC",
        "Claim",
        "Faucet",
        "Drip"
    ], 10000)

    if not clicked:
        raise Exception("Claim button not found")

    popup = await wait_for_popup(context)
    await approve_metamask(popup)

    return {"success": True}