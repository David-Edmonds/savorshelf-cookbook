# Measurement and content repair update — September 20, 2026

This is a partial content repair, not completion of the full collection. 56,690 explicitly stated ingredient amounts were parsed across 21,804 source recipes. 12,203 exact ingredient phrases were linked inside their original method steps. Original text is retained for comparison. Unknown amounts, ambiguous liquid ounces, ranges, compound quantities and unspecified cup/spoon standards are not guessed. Partial source recipes retain disabled scaling.

Three authored, source-credited adaptations now add complete quantities, inline/divided steps, substitutions, portion yields and estimated times: buttered toast, mashed potatoes and scrambled eggs. This brings existing adaptations to 76, leaving 40,817 recipes requiring further content work. They are not kitchen-tested. All 76 adaptations have step references for every ingredient. Images remain outside this update.

The shared ingredient and step display now supports approximate mass conversions, metric-volume to clearly labeled US fluid ounces, and explicit-US volume to metric. The kitchen preference can retain original units. Unspecified cup and spoon standards are not converted, and volume is never converted to weight without ingredient density. Fahrenheit/Celsius display preserves negative signs and respects the existing temperature preference. Saved data is not rewritten.

Conversion references: https://www.nist.gov/pml/owm/metric-si/metric-kitchen/metric-kitchen-cooking-measurement-equivalencies and https://www.nist.gov/pml/owm/metric-si/metric-kitchen/metric-kitchen-culinary-measurement-tips . Recipe-specific sources and adaptation choices are recorded on the three updated cards and in content-overrides.json.

Rebuild with build-catalog.py; overrides require matching original source hashes. Resumable remaining-work records are written outside the app to outputs/SavorShelf-Content-Repairs/remaining.jsonl. Nine Node tests and three parser tests passed, including full collection schema and source-method preservation, divided scaling, negative temperatures and duplicate-safe saving. Local browser checks passed for conversion display, saving, storage preservation, responsive layout and offline reload. Android APK, signing identity and portfolio are unchanged. No physical-phone tests.

# Recipe collection publication — September 20, 2026

The web cookbook includes 40,893 collection records, alongside the original cards: 42,345 visible recipes after overlapping IDs are hidden. Source-wording publication was explicitly approved by the owner. All have descriptions; 40,820 retain original quantities and methods, and 73 are completed adaptations. This is not a claim that all recipes are culinary-verified. Images were not required for this publication.

Public data is split into lazy-loaded recipe chunks; personal recipes remain in the existing browser storage. Unknown yields are explicitly one source batch, never one serving, and automatic scaling is disabled for these entries. Source quantities and cooking steps are preserved exactly. Longer source names are accepted by the web validator; old Android versions can reject those longer names when importing. The Android APK and signing identity are unchanged.

Validation: all 40,893 recipes pass the recipe validator and full source comparisons. Three automated data tests pass. Browser checks passed for browsing, save preservation, duplicate-safe saving, offline revisits, and widths 320/390/768/1280. Existing UX checks passed across five tabs. No physical-phone or cooking test was performed.

# SavorShelf

A standalone cookbook website with recipes, cultural discovery, kitchen preferences and an Android download.

Website address configured in GitHub Pages: https://david-edmonds.github.io/savorshelf-cookbook/

This repository is separate from the portfolio. GitHub Pages serves main /docs. The site intentionally includes 685 recipe-related ChatGPT entries and cooking notes with the owner's publication approval. It excludes the complete account export, unrelated conversations, private signing materials and the raw 55k recipe-source work list.

The current snapshot has 1,458 structured cards; worldwide recipe enrichment and complete image/translation coverage remain unfinished. AI illustrations are labeled. Visitors' own edits stay in their browser unless exported/shared; there is no automatic device synchronization. See the site's privacy, getting-started and source-credit pages.

The included APK is SavorShelf 0.18.0, signed with the original certificate. Physical-phone installation remains untested. GitHub publishes changes to docs when main changes. Review the exact content and approval scope before expanding public data.
