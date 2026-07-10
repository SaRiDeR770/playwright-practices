from playwright.sync_api import Page, expect
def test_checkbox_default(page: 'Page'):
    page.goto('https://practice.expandtesting.com/checkboxes')
    expect(page).to_have_url('https://practice.expandtesting.com/checkboxes')
    expect(page).to_have_title('Check Boxes page for Automation Testing Practice')
    expect(page.locator('#checkbox2')).to_be_checked()