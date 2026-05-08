from playwright.async_api import TimeoutError


async def click_any(page, patterns, timeout=3000):
    for pattern in patterns:
        try:
            btn = page.get_by_role("button", name=pattern).first
            await btn.wait_for(state="visible", timeout=timeout)
            await btn.click()
            return True
        except Exception:
            pass
    return False


async def approve_metamask(popup):
    # robust selectors for newer metamask UIs
    selectors = [
        'button:has-text("Confirm")',
        'button:has-text("Approve")',
        'button:has-text("Sign")',
        'button:has-text("Connect")',
        'button:has-text("Next")',
        'button:has-text("Submit")',
        '[data-testid="confirm-footer-button"]',
        '[data-testid="page-container-footer-next"]',
        '[data-testid="page-container-footer-next"] button',
        'button[type="submit"]'
    ]

    for _ in range(20):
        if popup.is_closed():
            return True

        for selector in selectors:
            try:
                btn = popup.locator(selector).first

                if await btn.is_visible(timeout=1500):
                    await btn.click()
                    await popup.wait_for_timeout(2000)
                    break
            except Exception:
                continue
        else:
            return False

    return False


async def wait_for_popup(context, timeout=30000):
    popup = await context.wait_for_event("page", timeout=timeout)
    await popup.wait_for_load_state("domcontentloaded")
    await popup.bring_to_front()
    await popup.wait_for_timeout(3000)
    return popup