# SavorShelf standalone website — ready for publication review

Proposed new repository: David-Edmonds/savorshelf-cookbook. Nothing has been pushed or published. Do not use the portfolio repository or change its settings.

After approval, create that separate repository, upload this package, and configure GitHub Pages to publish from main /docs. No build service, credentials, paid domain or backend is required. The expected default project path is /savorshelf-cookbook/; an existing user-site custom domain may affect the final hostname. Verify the actual Pages URL before reporting publication.

The docs folder contains the complete static website and cookbook. It intentionally includes the recipe-related ChatGPT archive and cooking notes at David's explicit request. Publishing makes those included notes publicly readable. It does not include the complete raw account export or unrelated conversations. Read PUBLISHING-MANIFEST.json and docs/credits.html for scope and provenance. Individual Wikibooks recipes preserve CC BY-SA 4.0 attribution and author-history links.

Preview on Windows from this folder: python -m http.server 8080 --directory docs . Then open http://127.0.0.1:8080 . For a project-path check serve the parent folder and use /savorshelf-publishing/docs/ . Do not use file:// for the app's offline features.

The public cookbook creates a browser-local collection for each visitor; it is not a cloud-sync account. Existing browser records are not cleared. English and Spanish navigation is available; full recipe translations and a unique photo for every dish remain unfinished. Missing matching photos use a labeled neutral card, never unrelated dish artwork.
