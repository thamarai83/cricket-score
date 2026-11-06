
from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    context = p.chromium.launch_persistent_context(
        user_data_dir="whatsapp_profile",
        headless=False,
        viewport={"width": 1280, "height": 800}
    )

    page = context.pages[0] if context.pages else context.new_page()

    page.goto("https://web.whatsapp.com/")

    input("Login to WhatsApp if required. Press Enter after chats appear...")

    # Step 1: Identify WhatsApp search box
    search_box = page.get_by_placeholder("Search or start a new chat")

    search_box.wait_for(state="visible", timeout=15000)

    print("WhatsApp search box found successfully!")

    # Step 2: Search for a contact
    search_box.fill("phillip.m")

    print("Searching for Phillip...")

    # Wait temporarily to inspect the search results
    page.wait_for_timeout(2000)

    # Keep browser open for inspection
    input("Inspect the search results, then press Enter...")

    context.close()
