import pytest
from playwright.sync_api import Page, expect

@pytest.mark.parametrize('value', ['10', '20', '50', '100'])
def test_elements_per_page(page: Page, value):
    page.goto('https://practice.expandtesting.com/dropdown')
    page.locator('#elementsPerPageSelect').select_option(value)
    expect(page.locator('#elementsPerPageSelect')).to_have_value(value)