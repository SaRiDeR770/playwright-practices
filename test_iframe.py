from playwright.sync_api import Page, expect
def test_iframe(page:"Page"):
    page.goto('https://practice.expandtesting.com/iframe')
    page.frame_locator('#email-subscribe').locator('#email').fill('sardor.saidov.315@gmail.com')
    expect(page.frame_locator('#email-subscribe').locator('#email')).to_have_value('sardor.saidov.315@gmail.com')