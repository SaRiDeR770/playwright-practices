from playwright.sync_api import Page, expect
def test_iframe_2(page:"Page"):
    page.goto('https://practice.expandtesting.com/iframe')
    page.frame_locator('#email-subscribe').locator('#email').fill('sardor770@mail.ru')
    expect(page.frame_locator('#email-subscribe').locator('#email')).to_have_value('sardor770@mail.ru')