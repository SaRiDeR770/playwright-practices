from playwright.sync_api import Page, expect
from checkbox_page import CheckboxPage
def test_checkbox_pom(page: Page):
    test_checkbox_page = CheckboxPage(page)
    test_checkbox_page.open()
    test_checkbox_page.check_first()
    expect(page.get_by_label('Checkbox 1')).to_be_checked()
