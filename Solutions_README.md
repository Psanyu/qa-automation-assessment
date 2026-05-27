# QA Automation Technical Assessment

**Live Report:** [cheery-druid-9fcecd.netlify.app](https://cheery-druid-9fcecd.netlify.app)
**Repository:** [github.com/Psanyu/qa-automation-assessment](https://github.com/Psanyu/qa-automation-assessment)

---

## Problem Statement

Automate functional validation of a mock data quality web application using **Playwright (Python sync API) + pytest**. The application simulates a CRM data issue review workflow where users can inspect, select, and edit data records. The challenge involved navigating nested iframes, handling asynchronous UI updates with random delays, and writing stable, independently runnable tests.

---

## Workflow

### 1. Exploration
Served the app locally and manually explored the interface before writing any tests:
```bash
cd "automation assesment"
python -m http.server 8080
```
Opened `http://localhost:8080/index.html` and mapped out the page structure — two nested iframes, a welcome modal, a loading spinner, and a dynamically rendered issue card grid.

### 2. Key Challenges Identified
- **Nested iframes** — the app renders inside `index.html` → `vf-container.html` → `app.html`, requiring chained `frame_locator()` calls
- **`data-testid="issue_grid"`** is only applied to every 3rd card (`idx % 3 == 0`) — not all 10. Used `[data-record-id]` instead to reliably locate all cards
- **Spinner uses `opacity: 0`** (not `display: none`) — Playwright's `state="hidden"` never resolved; removed that wait and relied on element-level visibility checks instead
- **Random async delays** of 500–5000ms on card rendering and 500–1000ms on save operations — addressed with `expect()` retries and appropriate timeouts
- **`triple_click()`** not available in this Playwright version — replaced with `click(click_count=3)`

### 3. Stability Fixes Applied
- Added `slow_mo: 100` in `conftest.py` to smooth out race conditions
- Used `scroll_into_view_if_needed()` before interacting with cards below the viewport
- Fixture waits for all 10 cards (`to_have_count(10, timeout=10000)`) before any test begins

### 4. Tests Implemented

| # | Test | What it validates |
|---|------|-------------------|
| 1 | `test_data_issues_grid_loads_10_records` | Navigates to Data Issues page and asserts 10 cards are displayed |
| 2 | `test_all_original_rows_contain_sfid` | Extracts original row data from all 10 cards and asserts each sfid is non-empty |
| 3 | `test_selecting_original_on_7th_card_updates_final_row` | Selects original radio on card 7, waits for async save, asserts final row reflects original value |
| 4 | `test_inline_edit_on_final_row_persists_value` | Edits Street field on record `00Qak00000RHtuzEAD`, types `123 Test Street`, asserts saved correctly |
| 5 | `test_selection_counter_reflects_checkbox_state` | Checks 1st/3rd/5th → asserts 3 selected; selects all → 10 selected; deselects all → counter hidden |

---

## Results

All **5 tests pass** consistently.

```
test_data_issues_grid_loads_10_records                    PASSED
test_all_original_rows_contain_sfid                       PASSED
test_selecting_original_on_7th_card_updates_final_row     PASSED
test_inline_edit_on_final_row_persists_value              PASSED
test_selection_counter_reflects_checkbox_state            PASSED

5 passed in ~26s
```

Full interactive Allure report: [cheery-druid-9fcecd.netlify.app](https://cheery-druid-9fcecd.netlify.app)

---

## Setup & Run

### Install dependencies
```bash
pip install pytest playwright pytest-playwright allure-pytest
python -m playwright install chromium
```

### Serve the app
```bash
cd "automation assesment"
python -m http.server 8080
```

### Run tests
```bash
# headless
python -m pytest test_data_issues.py -v

# headed (watch the browser)
python -m pytest test_data_issues.py -v --headed

# with Allure report
python -m pytest test_data_issues.py -v --headed --alluredir=allure-results
allure serve allure-results
```
