from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    page.goto(
        "https://www.naukri.com/",
        wait_until="domcontentloaded"
    )

    print("Naukri opened!")
    print("URL:", page.url)
    print("TITLE:", page.title())

    browser.close()
