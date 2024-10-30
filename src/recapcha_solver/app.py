import os
import uvicorn
from fastapi import FastAPI
from playwright.async_api import async_playwright
from playwright_recaptcha import recaptchav2
from retry_async import retry

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@retry(exceptions=Exception, is_async=True, tries=10, delay=5, backoff=2)
async def solve_recaptcha(page) -> str:
    async with recaptchav2.AsyncSolver(page) as solver:
        return await solver.solve_recaptcha(wait=True)


@app.get("/recaptchav2/solver")
async def recaptchav2_solver(url: str):
    async with async_playwright() as playwright:
        browser = await playwright.firefox.launch()
        page = await browser.new_page()
        await page.goto(url)

        token = await solve_recaptcha(page)
    return {"recaptcha_token": token}


def main():
    uvicorn.run(
        "recapcha_solver.app:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=os.getenv("API_PORT", 9987),
        reload=os.getenv("API_RELOAD", True),
        workers=os.getenv("API_WORKERS", 4),
    )
