from playwright.sync_api import Page, expect
def test_dropdown_reload (page:'Page'):
    page.goto('https://practice.expandtesting.com/dropdown')
    page.locator('#dropdown').select_option('2')
    page.reload()
    expect(page.locator('#dropdown')).not_to_have_value('2')


def test_select_elements_reload (page:"Page"):
    page.goto('https://practice.expandtesting.com/dropdown')
    page.locator('#elementsPerPageSelect').select_option('50')
    page.reload()
    expect(page.locator('#elementsPerPageSelect')).not_to_have_value('50')