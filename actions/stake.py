from browser import get_context
from config import EXCHANGE_URL
from helpers import click_any, approve_metamask, wait_for_popup


async def run(amount: str):
    context = await get_context()

    page = await context.new_page()

    await page.goto(
        EXCHANGE_URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    await page.wait_for_timeout(5000)

    inputs = page.locator('input[placeholder="0.0"]')
    stake_input = inputs.nth(1)

    await stake_input.wait_for(
        state="visible",
        timeout=15000
    )

    await stake_input.click()
    await stake_input.fill("")
    await stake_input.type(amount, delay=100)

    await page.wait_for_timeout(2000)

    clicked = await click_any(page, [
        "STAKE DACC",
        "Stake"
    ], 10000)

    if not clicked:
        raise Exception("Stake button not found")

    popup = await wait_for_popup(context)

    await approve_metamask(popup)

    return {
        "success": True,
        "action": "stake",
        "amount": amount
    }