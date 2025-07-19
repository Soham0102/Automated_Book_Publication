
import asyncio
from playwright.async_api import async_playwright
import os

async def scrape_and_screenshot(url: str, save_dir="data"):
    os.makedirs(save_dir, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()

        screenshot_path = os.path.join(save_dir, "screenshot.png")
        await page.screenshot(path=screenshot_path)
        print(f"Screenshot saved at {screenshot_path}")

        text_content = await page.inner_text("body")
        text_path = os.path.join(save_dir, "content.txt")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(text_content)
        print(f"Text content saved at {text_path}")

        await browser.close()
    return text_content

if __name__ == "__main__":
    url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    asyncio.run(scrape_and_screenshot(url))
