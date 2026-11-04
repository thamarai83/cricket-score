import re

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
)

MATCH_CARD_SELECTOR = 'a[href*="/live-cricket-scores/"][class*="bg-cbWhite"]'
LIVE_STATUS = re.compile(
    r"\b(?:live|need\s+\d+\s+runs?|require\s+\d+\s+runs?|stumps|"
    r"innings break|day\s+\d+)\b",
    re.IGNORECASE,
)
COMPLETED_STATUS = re.compile(
    r"\b(?:won|drawn|draw|tied|no result|abandoned)\b",
    re.IGNORECASE,
)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    try:
        page.goto(
            "https://www.cricbuzz.com/",
            wait_until="domcontentloaded",
            timeout=30000,
        )

        match_cards = page.locator(MATCH_CARD_SELECTOR)

        try:
            match_cards.first.wait_for(state="visible", timeout=15000)
        except PlaywrightTimeoutError:
            print("No match cards appeared on Cricbuzz.")
        else:
            card_texts = [
                match_cards.nth(index).inner_text().strip()
                for index in range(match_cards.count())
            ]
            live_score = next(
                (text for text in card_texts if LIVE_STATUS.search(text)),
                None,
            )
            previous_score = next(
                (text for text in card_texts if COMPLETED_STATUS.search(text)),
                None,
            )

            if live_score:
                print("Live match score:")
                print(live_score)
            elif previous_score:
                print("No live match found. Previous match score:")
                print(previous_score)
            else:
                print("No live match or completed match score was found.")

        page.screenshot(path="score.png", full_page=True)
        print("Saved screenshot to score.png")
    finally:
        browser.close()