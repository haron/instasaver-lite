#!/usr/bin/env -S uv run -q
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "playwright",
#   "install-playwright"
# ]
# ///
import sys
import asyncio
from playwright.async_api import async_playwright
from install_playwright import install
from pathlib import Path


async def save_image(url, browser):
    page = await browser.new_page()
    img_id = url.split("/")[4]
    await page.goto(url, wait_until="load")
    await page.wait_for_function("() => document.readyState == 'complete'")
    await page.evaluate("window.scrollBy(0, 100);")
    await page.wait_for_timeout(500)
    await page.evaluate("window.scrollBy(0, 500);")
    await page.wait_for_timeout(5000)
    img_url = await page.evaluate("document.querySelector('div img[style*=cover]').src")
    resp = await page.request.get(img_url)
    img_bytes = await resp.body()
    dest = Path(f"{img_id}.jpg")
    with open(dest, "wb") as f:
        f.write(img_bytes)


async def main(urls):
    async with async_playwright() as p:
        install(p.webkit)
        browser = await p.webkit.launch()
        for url in urls:
            await save_image(url, browser)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
