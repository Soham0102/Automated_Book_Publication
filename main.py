
import asyncio
from scraper import scrape_and_screenshot
from ai_writer import rewrite_text

async def main():
    url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    print("Scraping content...")
    original = await scrape_and_screenshot(url)

    print("Rewriting with AI...")
    rewritten = rewrite_text(original)

    print("Reviewing content...")
    final_text = review_text(original, rewritten)

    print("Storing final version...")
    store_version(final_text, "chapter1_final")

    print("Workflow completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
