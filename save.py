import sys
import asyncio
from playwright.async_api import async_playwright


async def save_image(url, browser):
    page = await browser.new_page()
    img_id = url.split("/")[4]
    await page.goto(url, wait_until="load")
    await page.wait_for_function("() => document.readyState == 'complete'");
    await page.evaluate(f'window.scrollBy(0, 999);')
    await page.wait_for_timeout(5000)
    img_url = await page.evaluate(f"document.querySelector('div img[style*=cover]').src")
    resp = await page.request.get(img_url)
    img_bytes = await resp.body()
    with open(f"{img_id}.jpg", 'wb') as f:
        f.write(img_bytes)


async def main(urls):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for url in urls:
            await save_image(url, browser)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
