from config import APP_URL
from browser import get_context


async def run():
    context = await get_context()

    home = await context.new_page()

    await home.goto(
        APP_URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    for page in context.pages:
        try:
            if page == home:
                continue

            url = page.url

            if url.startswith("chrome-extension://"):
                continue

            await page.close()
        except Exception:
            pass

    await home.bring_to_front()

    return {
        "success": True,
        "action": "reset"
    }