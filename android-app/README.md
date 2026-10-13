# Leggacy Android beta

Leggacy 0.25.2/code 29 continues the existing Java WebView app. Target API 36; minimum Android API 26 and WebView 80. Preserve com.recipekeeper.ourtable, the original signing certificate, native recipes-v1.json, browser our-table-v1, local asset origin and legacy backup markers.

The public build contains three original labelled untested samples. It excludes private history, imported corpus and food photographs. Connected AI is omitted from the owner-approved first beta: Internet permission is absent, native connection bridges are disabled and UI connection controls are removed. Stored recipes, photos, notes, preferences and legacy connection settings are not reset. Offline template creation and imports remain available.

Use scripts/build-play.py with the existing private signing backup and supplied JDK/Build Tools 36/Platform 36/bundletool paths. Public samples are the default; scripts/public-offline-only.js is a required build input. Never generate a replacement signing key, commit the private key, or upload a private-review build.

Validation: 20 public-source tests passed; final public browser sample/scaling/offline/legacy JSON checks passed; offline draft creation/save works with newer text/DOM APIs and structuredClone/Object.hasOwn absent; no off-device requests observed. Android 16 signed upgrade preserved complete saved JSON and displayed offline creation. Earlier 193 full-source regressions and Android 15/16 baseline upgrades passed. Physical-phone and kitchen checks remain. The existing website has an inherited formatter test failure reproduced on baseline.

The original key has been enrolled with Google Play, and the public privacy policy is live. Final beta submission status is recorded in docs/BETA-STATUS.md. Full website rebrand and companion creator PRs are separate drafts.
