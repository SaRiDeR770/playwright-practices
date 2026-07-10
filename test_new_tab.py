from playwright.sync_api import Page, expect
def test_new_tab(page:"Page"):
    page.goto('https://practice.expandtesting.com/windows')
    with page.context.expect_page() as new_page_info:
        page.get_by_role('link', name = 'Click here').click()
    new_page = new_page_info.value
    expect(new_page.get_by_text('Example of a new window page for Automation Testing Practice')).to_be_visible()
