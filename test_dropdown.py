from playwright.sync_api import Page, expect
def test_dropdown(page: 'Page'):
    page.goto('https://practice.expandtesting.com/dropdown')
    page.locator('#dropdown').select_option('2')
    expect(page.locator('#dropdown')).to_have_value('2')