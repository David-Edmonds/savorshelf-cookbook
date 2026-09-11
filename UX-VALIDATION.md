# Website UX update — September 11, 2026

The existing cookbook now has equal-width scope buttons, consistent mobile spacing, a compact search/filter panel, clearer cards, and a responsive three-column desktop grid. Meal and time remain easy to reach; finer filters stay grouped. Missing recipe details remain labeled.

Search waits 120 ms after typing and reuses the existing index. Select filters and scope tabs update results without rebuilding the screen. Search can be cleared independently. Pagination moves to the results; returning from a recipe restores its card focus and scroll position. At most 24 result cards are rendered at once. Saved recipe data is not migrated.

## Validation

Real local Chromium browser checks passed: filter focus, open groups, query clearing, filter removal, scope switching, empty results, pagination, recipe return focus/scroll, reload persistence, unchanged saved collection, index reuse, and all five tabs at 320/390/768/1280 pixels. Local search/result rendering measured approximately 1–27 ms in the sampled queries, excluding the intentional 120 ms debounce. These are desktop measurements, not physical-phone performance results.

The website page/link/language/deep-link/archive checks also passed. The 685-entry cooking archive and signed 0.18.0 APK are unchanged. This update does not add recipes or rebuild Android. Live AI generation and physical-phone installation were not tested.

## Run the interaction checks

Install Python and Playwright, then run:

```powershell
python -m pip install playwright
python -m playwright install chromium
python tests/ux-browser.py
```

Optional: set PLAYWRIGHT_CHROMIUM_EXECUTABLE to an existing Chromium executable. The test starts a temporary localhost server and uses an isolated browser context. It also verifies offline loading of the updated styles. Screenshots are written to tests/ux-mobile.png and tests/ux-desktop.png.

## Integrating into the Android source later

Port cookbook-ui.js, language-ui.js, public-edition.js, ux-polish.css and the stylesheet link deliberately into the current source. Keep public-edition.js website-only. sw.js controls only website caching. Do not overwrite the separate recipe-expansion work or change the Android signing identity.

## Contrast follow-up

Fixed the dark-theme search field rendering light text on white. Website surfaces now follow the selected theme together. Text-entry fields and selects use cream backgrounds with navy text in both themes, with stronger boundaries, opaque placeholders, and a distinct active scope outline in dark mode. The standalone site also keeps native select colors consistent under a dark OS preference.

Run `python tests/contrast-browser.py`: 98 visible controls across light/dark system themes, five tabs, recipe dialog and editor passed computed text/placeholder contrast of at least 4.5:1 and mobile overflow checks. Dark cookbook and creator screenshots were visually inspected. This is focused contrast validation, not a full accessibility certification or physical-phone test.
