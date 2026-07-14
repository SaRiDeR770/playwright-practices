from playwright.sync_api import expect, Page

def test_secure_area(logged_in_page):
    expect(logged_in_page.get_by_text('You logged into a secure area!')).to_be_visible()