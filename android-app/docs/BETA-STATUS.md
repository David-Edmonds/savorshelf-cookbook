# Leggacy closed-test display update — 15 October 2026

Google Play accepted Leggacy 0.25.3 (30) and the tester-access change to testers-community@googlegroups.com. Publishing overview displays **Changes in review**, with automated quick checks running. Checks must finish successfully before Google review. This is a closed Alpha update, not a public production release. Managed publishing is off; eligible testers can receive the update after approval. Existing country coverage is unchanged (178 regions including Rest of World).

The update removes the two deprecated system-bar colour calls Play identified, improves edge-to-edge and display-cutout handling, and keeps controls clear of system bars and the keyboard. Package, original signer, saved recipes and backups remain compatible. The final logo, three labelled untested samples and offline-only configuration are retained.

Validation: 193/193 full-source tests and 20/20 public-source tests passed. APK/AAB signatures, bundle validation and 81 staged asset matches passed. An actual signed 29-to-30 Android 16 emulator upgrade preserved the complete saved JSON, including after relaunch. Light/dark, portrait/landscape cutouts, keyboard and both navigation modes were checked. Physical-phone and older Android execution were not performed for this update. Play's separate display-warning reanalysis has not yet been confirmed.

See play-submission.json, DISPLAY-UPDATE-0.25.3.txt and display-update-native-validation.json. The dated delivery folder contains build artifacts, test logs and play-submitted.png. The record below describes the original beta submission and remains historical.

---

# Leggacy closed-beta submission — 13 October 2026

**Leggacy 0.25.2 (29) was submitted to Google Play for closed Alpha testing.** Play displays **Changes in review**, with automated quick checks still running. This records acceptance of the submission request; Google approval and tester availability remain pending. The app is not live or publicly searchable.

The 14 submitted changes include the version 29 release, United Kingdom and United States availability, the one-address Leggacy owner beta list, feedback channel, final store listing/artwork, rating, audience, privacy policy, ads, Data safety, health declaration and Food & Drink category. Additional access, Advertising ID, government and financial declarations are saved. Managed publishing is off, so the closed beta can become available to eligible testers after approval. No tester invitations were sent. Zero genuine opt-ins have been established.

The approved final logo is integrated into native icons/splash, web assets and store artwork. Icon and feature graphic carry the AI disclosure. Four screenshots show actual app screens. IARC terms were accepted with owner approval; ratings include ESRB Everyone and PEGI 3. Publisher support and rating contact: leftfieldstudioapps@gmail.com.

The encrypted original signing key was enrolled with Google Play. The displayed app-signing certificate matches the retained original SHA-256: f6eac7b4b42570c9c29a73504a73a0f228e09d4a645651c7d9ff2370581b5eb3. Package com.recipekeeper.ourtable, storage identifiers, backup compatibility and saved collections are preserved. No replacement signing key was generated. The private backup was not uploaded or included in source packages.

The first beta is offline: connected AI is omitted with owner approval, native connection bridges are guarded and the public manifest has no Internet permission. It includes three original clearly labelled untested sample recipes and excludes the private/imported corpus and bundled food photographs. Existing saved recipes remain intact. Offline recipe creation, editing, scaling, cooking, shopping and backup workflows remain available.

[Live privacy policy](https://david-edmonds.github.io/savorshelf-cookbook/android-privacy.html)

## Verification and limits

Current version 29: 20/20 public-source tests passed; browser sample, scaling, offline reload, complete legacy JSON equality and offline draft creation/save passed. Creation also passed with newer text/DOM methods, Object.hasOwn and structuredClone disabled. No off-device requests or page errors were observed. APK/AAB original signatures, bundle validation and all 81 staged asset matches passed. Android 16 signed upgrade preserved complete saved JSON and showed offline creation. Earlier full-source 193/193 regressions and Android 15/16 baseline upgrades preserved all 31 synthetic saved recipes.

Physical-phone and kitchen tests have not been performed. Full execution on Android 8/WebView 80 was not performed; missing newer browser methods were simulated. The existing cookbook website retains an inherited formatter/source-data test failure reproduced on unchanged baseline f37b5ff. Play's only release warning concerns an optional deobfuscation map; this build does not use R8/Proguard obfuscation.

The earlier version 28 submission was withdrawn before availability; its draft release was discarded and replaced with version 29 after a compatibility fix. Only version 29 is in the final release. Older artifacts remain historical.

This is a restricted closed beta. Production/open-testing eligibility still requires the account's genuine tester requirement and production-access approval. Full cookbook and creator rebrand PRs remain drafts; policy-only PRs #2 and #3 are merged and the privacy policy is live.

## Deliverables

- Leggacy-0.25.2.apk and Leggacy-0.25.2.aab: verified final build.
- play-submission.json and play-beta-submitted.jpg: submission receipt and Console proof.
- Leggacy-0.25.2-public-source.zip: sanitized public source.
- Leggacy-0.25.2-PRIVATE-source.zip: private source recovery, excluding signing credentials.
- Leggacy-local-history.bundle: recoverable local Git history.
- Leggacy-store-assets-final.zip: final store artwork, copy and release status.
