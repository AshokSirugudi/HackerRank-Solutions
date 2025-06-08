# config.py - This file contains the login utility function for HackerRank using Playwright.
# This version is designed for robustness against dynamic page loading and bot detection,
# includes a fix for the 'httponly' cookie error, and adds common browser headers to combat 403 errors.
# It will also keep the browser open after successful login for your inspection.

import os
import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import time
import json

# Load environment variables
load_dotenv()

def login_hackerrank(username, password):
    """
    Logs into HackerRank using Playwright, extracts authenticated cookies,
    and returns an authenticated requests.Session object.
    Returns None if login fails.
    """
    session = requests.Session()

    login_url = "https://www.hackerrank.com/auth/login"
    dashboard_url_part = "https://www.hackerrank.com/dashboard"

    print("\n--- DEBUG INFO (HackerRank Login Process via Playwright) ---")
    print(f"DEBUG: Input username received by login function: '{username}'")

    browser = None
    page = None

    try:
        with sync_playwright() as p:
            print("DEBUG: Launching Chromium browser in VISIBLE mode (headless=False) for debugging...")
            browser = p.chromium.launch(headless=False, timeout=60000)
            context = browser.new_context()
            page = context.new_page()

            print(f"DEBUG: Navigating to login page: {login_url}")
            page.goto(login_url, wait_until="domcontentloaded", timeout=90000)
            print("DEBUG: Page loaded DOM. Waiting for network idle...")
            page.wait_for_load_state("networkidle", timeout=90000)
            print("DEBUG: Giving page an additional moment to render dynamic elements (3s)...")
            time.sleep(3)

            print(f"DEBUG: Attempting to fill username field...")
            username_selector = 'input[name="username"]'
            alt_username_selectors = [
                'input[placeholder="Your username or email"]',
                'input[aria-label="Your username or email"]',
                '#username'
            ]
            found_username_field = False
            try:
                page.locator(username_selector).wait_for(state="visible", timeout=20000)
                page.fill(username_selector, username, timeout=15000)
                found_username_field = True
                print("DEBUG: Username field filled using primary selector.")
            except Exception as e:
                print(f"DEBUG: Primary username selector failed: {e}. Trying alternative selectors.")
                for selector in alt_username_selectors:
                    try:
                        page.locator(selector).wait_for(state="visible", timeout=10000)
                        page.fill(selector, username, timeout=10000)
                        found_username_field = True
                        print(f"DEBUG: Username field filled using alternative selector: {selector}")
                        break
                    except Exception:
                        continue
            if not found_username_field:
                raise Exception("Could not locate or fill username field using any known selectors.")

            print("DEBUG: Attempting to fill password field...")
            password_selector = 'input[name="password"]'
            alt_password_selectors = [
                'input[placeholder="Your password"]',
                'input[aria-label="Your password"]',
                '#password'
            ]
            found_password_field = False
            try:
                page.locator(password_selector).wait_for(state="visible", timeout=20000)
                page.fill(password_selector, password, timeout=15000)
                found_password_field = True
                print("DEBUG: Password field filled using primary selector.")
            except Exception as e:
                print(f"DEBUG: Primary password selector failed: {e}. Trying alternative selectors.")
                for selector in alt_password_selectors:
                    try:
                        page.locator(selector).wait_for(state="visible", timeout=10000)
                        page.fill(selector, password, timeout=10000)
                        found_password_field = True
                        print(f"DEBUG: Password field filled using alternative selector: {selector}")
                        break
                    except Exception:
                        continue
            if not found_password_field:
                raise Exception("Could not locate or fill password field using any known selectors.")

            print("DEBUG: Attempting to click login button or press Enter...")
            login_button_selector = 'button:has-text("Log In")'
            alt_login_button_selectors = [
                'button[type="submit"]',
                'button.auth-button',
                'input[type="submit"][value="Log In"]'
            ]
            button_clicked = False
            try:
                page.locator(login_button_selector).wait_for(state="enabled", timeout=20000)
                page.click(login_button_selector, timeout=20000)
                button_clicked = True
                print("DEBUG: Login button clicked using primary selector.")
            except Exception as e:
                print(f"DEBUG: Primary login button click failed: {e}. Trying alternative selectors.")
                for selector in alt_login_button_selectors:
                    try:
                        page.locator(selector).wait_for(state="enabled", timeout=15000)
                        page.click(selector, timeout=15000)
                        button_clicked = True
                        print(f"DEBUG: Login button clicked using alternative selector: {selector}")
                        break
                    except Exception:
                        continue

            if not button_clicked:
                print("DEBUG: Direct button click failed. Simulating 'Enter' key press.")
                if found_password_field:
                    page.locator(password_selector).press('Enter')
                    print("DEBUG: 'Enter' key pressed on password field.")
                else:
                    raise Exception("Could not click login button or simulate Enter key.")

            print("DEBUG: Clicked login button/pressed Enter. Waiting for navigation to dashboard...")
            page.wait_for_url(lambda url: dashboard_url_part in url, timeout=90000)
            print(f"DEBUG: Successfully navigated to: {page.url}")
            print("DEBUG: Login appears successful via Playwright.")

            cookies = context.cookies()
            print(f"DEBUG: Extracted {len(cookies)} cookies from Playwright session.")

            for cookie in cookies:
                filtered_cookie_args = {
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'domain': cookie['domain'],
                    'path': cookie['path'],
                    'secure': cookie.get('secure', False),
                    'expires': cookie.get('expires'),
                }
                session.cookies.set(**filtered_cookie_args)
            print("DEBUG: Cookies transferred to requests.Session (with 'httponly' and 'samesite' filtered).")

            # --- NEW SECTION: Add common browser headers to the requests.Session ---
            print("DEBUG: Adding standard browser headers to the requests.Session...")
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Referer': 'https://www.hackerrank.com/dashboard', # Crucial: referer should be a valid page
                'X-Requested-With': 'XMLHttpRequest', # Often expected for API calls
            })
            print("DEBUG: Headers updated.")
            # --- END NEW SECTION ---

            print("\n--- Login successful! Browser will remain open for manual inspection. ---")
            print("You can now manually verify login on the browser window that just appeared.")
            input("Press Enter in this terminal to close the browser and proceed with the script...")
            
            browser.close()
            return session

    except Exception as e:
        print(f"An unexpected error occurred during Playwright execution: {e}")
        import traceback
        traceback.print_exc()
        
        screenshot_path = "playwright_login_fail.png"
        try:
            if page:
                page.screenshot(path=screenshot_path)
                print(f"DEBUG: Screenshot saved to {screenshot_path}")
        except Exception as ss_e:
            print(f"DEBUG: Could not save screenshot: {ss_e}")

        if browser and page and login_url in page.url:
            print("DEBUG: Still on the login page. Checking for visible error messages on the web page...")
            try:
                error_message_selectors = [
                    'text="Authentication failed! Invalid credentials."',
                    '.error-message',
                    '.form-error',
                    'div[data-qa*="error-message"]',
                    '[role="alert"]'
                ]
                found_error_text = False
                for selector in error_message_selectors:
                    try:
                        error_locator = page.locator(selector)
                        if error_locator.count() > 0 and error_locator.is_visible(timeout=2000):
                            error_text = error_locator.text_content(timeout=1000)
                            if error_text:
                                print(f"DEBUG: Found error message on page: '{error_text.strip()}' using selector: {selector}")
                                found_error_text = True
                                break
                    except Exception:
                        pass
                if not found_error_text:
                    print("DEBUG: No explicit error message element found or visible by common locators on the page.")
            except Exception as e_msg:
                print(f"DEBUG: Could not retrieve error message during final check: {e_msg}")
        
        if browser:
            print("\n--- Playwright paused for manual inspection. Press Ctrl+C in terminal to continue/exit ---")
            page.pause()
            browser.close()
        return None