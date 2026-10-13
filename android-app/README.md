# Leggacy Android app â€” public source projection

This continues the existing Java WebView app, preserving `com.recipekeeper.ourtable`, `com.recipekeeper.app.MainActivity`, the original signer, `recipes-v1.json`, `our-table-v1` and the local asset origin. It is not a new scaffold. Version 0.25.0/code 27 targets API 36.

The owner selected three original untested public sample drafts. Private historical recipes/notes, imported catalog text and bundled food photographs are excluded. Existing installations retain their saved recipes, photos, notes, ratings and preferences; the public source has no copy of those user records. New installs have exactly three samples. The final owner-supplied cookbook/egg logo is integrated into native launcher and splash resources and web icons.

Run `node --test tests/*.test.cjs` (pass the file list explicitly in PowerShell). Build with Python `scripts/build-play.py --public-samples`, supplying `--jdk`, `--tools` (Build Tools 36), `--platform` (Platform 36), `--bundletool`, and `--signing-backup` as local paths. The existing private backup is never included here. The script refuses another certificate; it builds and verifies APK/AAB, derives a signed bundle APK and compares all packaged web assets to staged source. Never generate a replacement key.

Local validation: full private-source regression suite 193/193; public browser sample/scaling/offline tests passed; complete 31-recipe prior state equal in browser and Android 15 signed 0.24.0 upgrade/relaunch; public bundle clean install has three samples. Android 16 execution passed; physical-phone execution remains untested. No Play upload or deployment is implied by this PR. Actual optional provider authentication and calls are untested and unconfigured.

Support: leftfieldstudioapps@gmail.com. Bundled privacy page is `web/privacy.html`; public web policy publication and store declarations remain release gates. The full private corpus/source is retained only in the owner's local recovery package.
