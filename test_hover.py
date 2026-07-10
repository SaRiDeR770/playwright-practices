from playwright.sync_api import Page, expect
def test_hover(page:"Page"):
    page.goto('https://practice.expandtesting.com/hovers')
    page.get_by_test_id('user-1').hover()
    expect(page.get_by_text('name: user1')).to_be_visible()