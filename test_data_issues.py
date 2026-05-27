import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8080/index.html"


@pytest.fixture()
def issues_page(page: Page):
    """Land on the Data Issues grid, ready for test interaction."""
    page.goto(BASE_URL, wait_until="networkidle")

    # wait for modal to appear then dismiss it
    modal_btn = page.locator("#welcomeModal button")
    modal_btn.wait_for(state="visible", timeout=5000)
    modal_btn.click()

    # app lives inside two nested iframes
    outer = page.frame_locator('iframe[title="Application Container"]')

    # wait for loading spinner to fully disappear before touching anything
    outer.locator("#spinnerOverlay").wait_for(state="hidden", timeout=8000)

    app = outer.frame_locator('iframe[title="GenericCRM Application"]')

    # make sure the button is ready before clicking
    solve_btn = app.locator("#solveBtn")
    expect(solve_btn).to_be_visible(timeout=8000)
    solve_btn.click()

    expect(app.locator("#page-issues")).to_be_visible(timeout=8000)

    # give the issue cards a moment to fully render
    expect(app.locator('[data-testid="issue_grid"]').first).to_be_visible(timeout=8000)

    return app


# ── Test 1 ────────────────────────────────────────────────────────────────────

def test_data_issues_grid_loads_10_records(issues_page):
    expect(issues_page.locator('[data-testid="issue_grid"]')).to_have_count(10)


# ── Test 2 ────────────────────────────────────────────────────────────────────

def test_all_original_rows_contain_sfid(issues_page):
    cards = issues_page.locator('[data-testid="issue_grid"]')
    expect(cards).to_have_count(10)

    for i in range(cards.count()):
        # sfid is always the last td in the original row
        sfid = (
            cards.nth(i)
            .locator('tr[data-row-type="original"] td')
            .last.inner_text()
            .strip()
        )
        assert sfid, f"card {i + 1}: sfid is empty"


# ── Test 3 ────────────────────────────────────────────────────────────────────

def test_selecting_original_on_7th_card_updates_final_row(issues_page):
    card = issues_page.locator('[data-testid="issue_grid"]').nth(6)

    original_value = (
        card.locator('tr[data-row-type="original"] .cell-issue span')
        .inner_text()
        .strip()
    )

    radio = card.locator('tr[data-row-type="original"] input[type="radio"]')
    expect(radio).to_be_visible(timeout=5000)
    radio.click()

    # app fires a randomDelay(500-1000ms) save; bump timeout to 5s to be safe
    expect(
        card.locator('tr[data-row-type="final"] .cell-editable span')
    ).to_have_text(original_value, timeout=5000)


# ── Test 4 ────────────────────────────────────────────────────────────────────

def test_inline_edit_on_final_row_persists_value(issues_page):
    card = issues_page.locator('[data-record-id="00Qak00000RHtuzEAD"]')
    editable = card.locator('tr[data-row-type="final"] .cell-editable')

    expect(editable).to_be_visible(timeout=5000)
    editable.click()

    inp = editable.locator("input.inline-edit-input")
    inp.wait_for(state="visible", timeout=5000)

    inp.triple_click()
    inp.fill("123 Test Street")
    inp.press("Enter")

    # bump timeout to 5s to cover the full randomDelay(500-1000ms) save
    expect(editable.locator("span")).to_have_text("123 Test Street", timeout=5000)


# ── Test 5 ────────────────────────────────────────────────────────────────────

def test_selection_counter_reflects_checkbox_state(issues_page):
    cards = issues_page.locator('[data-testid="issue_grid"]')
    confirm_bar = issues_page.locator("#confirmBar")
    counter = issues_page.locator(".confirm-bar-text")

    # select cards 1, 3, 5
    for i in [0, 2, 4]:
        cb = cards.nth(i).locator(".issue-checkbox")
        expect(cb).to_be_visible(timeout=5000)
        cb.check()

    expect(counter).to_contain_text("3 issue(s) selected", timeout=5000)

    # select all
    select_all = issues_page.locator("#selectAll")
    expect(select_all).to_be_visible(timeout=5000)
    select_all.check()
    expect(counter).to_contain_text("10 issue(s) selected", timeout=5000)

    # deselect all — bar should hide
    select_all.uncheck()
    expect(confirm_bar).not_to_be_visible(timeout=5000)
