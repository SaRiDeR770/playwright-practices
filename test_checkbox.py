from playwright.sync_api import Page, expect
def test_checkbox(page: 'Page'):
    page.goto('https://practice.expandtesting.com/checkboxes')
    page.get_by_label('Checkbox 1').check()
    expect(page.get_by_label('Checkbox 1')).to_be_checked()
