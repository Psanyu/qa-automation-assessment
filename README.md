# QA Automation Technical Assessment

## Overview

I was provided with a mock data quality application. The task was to write automated tests against it using **Playwright with Python (sync API)** and **pytest**. The repository and details below reflect this attempt.

## Setup

1. Extracted the zip and served the application locally:
   ```
   cd app
   python -m http.server 8080
   ```
2. Opened `http://localhost:8080/index.html` in a browser and explore the application before writing any tests.

## Tests to Implement

Wrote the following 5 tests. Each test started from `http://localhost:8080/index.html`.

### Test 1: Navigate to the Data Issues grid

Navigated to the Data Issues page and asserted that 10 issue cards as displayed.

### Test 2: Extract and validate all issue data

From the Data Issues grid, extracted the original row data from all 10 issue cards. Asserted that each card's original row contains a non-empty sfid value.

### Test 3: Select a specific issue and change its value

Located the 7th issue card on the grid. Selected the **original** value for the issue column. Asserted that the final row updated to reflect the original value.

### Test 4: Edit a final row field

Located the issue card with sfid `00Qak00000RHtuzEAD`. Edit the issue column in the final row — clear the existing value, type `123 Test Street`, and confirm the edit. Asserted the final row displays `123 Test Street`.

### Test 5: Checkbox selection count

Selected the checkboxes on the 1st, 3rd, and 5th issue cards. Assert the selection counter shows `3 issue(s) selected`. Selected all issues and assert the counter shows `10 issue(s) selected`. Deselected all and assert the counter is no longer visible.

## Requirements

- Playwright sync API with pytest
- All tests should be independently runnable
- Do not modify the application files

## Submission

- Push your test code to a Git repository (GitHub, GitLab, etc.)
- Include a README in your repo explaining how to install dependencies and run the tests
- Share the repository link in your application
