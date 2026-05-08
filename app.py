from desktop import start_desktop
from fastapi import FastAPI, HTTPException
from browser import boot_browser, browser_status
from actions import reset, faucet, burn, stake, crate

app = FastAPI(title="Dachain Automation Bot")


@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/boot")
async def boot():
    try:
        start_desktop()
        await boot_browser()

        return {
            "success": True,
            "message": "desktop + browser started",
            "novnc": "http://localhost:6080/vnc.html"
        }

    except Exception as e:
        raise HTTPException(500, str(e))
        
@app.get("/status")
async def status():
    return await browser_status()


@app.post("/reset")
async def reset_tabs():
    try:
        return await reset.run()
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/faucet")
async def faucet_claim():
    try:
        return await faucet.run()
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/burn")
async def burn_qe(amount: str = "0.05"):
    try:
        return await burn.run(amount)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/stake")
async def stake_dacc(amount: str = "0.05"):
    try:
        return await stake.run(amount)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/crate")
async def open_crate():
    try:
        return await crate.run()
    except Exception as e:
        raise HTTPException(500, str(e))