from playwright.sync_api import sync_playwright
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

RESUME = Path(__file__).parent / "Rishabh_singh_Resume_.pdf"

PROFILE_URL = "https://www.naukri.com/mnjuser/profile"

CDP_URL = "http://127.0.0.1:9222"


# ============================================================
# HELPERS
# ============================================================

def wait(page, seconds):
    page.wait_for_timeout(seconds * 1000)


def screenshot(page, filename):
    page.screenshot(
        path=filename,
        full_page=True
    )
    print(f"Screenshot saved: {filename}")


def get_naukri_page(context):

    # Use an already-open Naukri tab
    for page in context.pages:
        if "naukri.com" in page.url:
            return page

    # Otherwise create a new tab
    return context.new_page()


# ============================================================
# RESUME UPLOAD
# ============================================================

def upload_resume(page):

    print("\n========== RESUME UPLOAD ==========")

    # Check resume exists
    if not RESUME.exists():
        raise FileNotFoundError(
            f"Resume not found: {RESUME}"
        )

    print("Resume found:")
    print(RESUME)

    # Open Naukri profile
    page.goto(
        PROFILE_URL,
        wait_until="domcontentloaded"
    )

    wait(page, 4)

    print("Profile loaded:")
    print(page.url)

    # Find Update Resume button
    update_resume = page.get_by_role(
        "button",
        name="Update resume"
    )

    if not update_resume.is_visible():
        raise RuntimeError(
            "Update resume button not found."
        )

    print("Update resume button found.")

    # Click and select the PDF
    with page.expect_file_chooser(timeout=10000) as fc_info:

        update_resume.click()

    file_chooser = fc_info.value

    file_chooser.set_files(
        str(RESUME)
    )

    print("Resume selected.")

    # Wait for upload to complete
    wait(page, 5)

    print("Resume upload completed.")

    screenshot(
        page,
        "after-resume-upload.png"
    )


# ============================================================
# MAIN
# ============================================================

with sync_playwright() as p:

    print("Connecting to Chrome...")

    browser = p.chromium.connect_over_cdp(
        CDP_URL
    )

    context = browser.contexts[0]

    print("Connected to Chrome.")

    page = get_naukri_page(context)

    try:

        # ONLY ACTION
        upload_resume(page)

        print("\n===================================")
        print("RESUME UPLOAD SUCCESSFUL")
        print("===================================")

    except Exception as e:

        print("\n===================================")
        print("AUTOMATION FAILED")
        print("===================================")

        print(
            type(e).__name__,
            e
        )

        screenshot(
            page,
            "automation-error.png"
        )

        raise

    finally:

        # Do NOT close your real Chrome
        print("Chrome will remain open.")