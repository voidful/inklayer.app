# inklayer.app

The InkLayer website, served by GitHub Pages at https://inklayer.app.

```sh
python3 build.py [path/to/InkLayer/store_assets/public_web/published]
```

`build.py` writes every page:

| Path | Page |
| --- | --- |
| `/`, `/index.zh-TW.html` | Home, from the copy in `build.py` |
| `/privacy/` (alias `privacy.html`), `/privacy.zh-TW.html` | Privacy Policy |
| `/support/` (alias `support.html`), `/support.zh-TW.html` | Support |
| `/404.html` | Not found |

The privacy and support pages take their text from the InkLayer repository's
`store_assets/public_web/published/` (the pages the App Store links to) and
add this site's header and footer; change the text there, then rebuild.

The home page claims only what the App Store version does; the next
version's features stay under "In InkLayer 1.1". Images in `assets/img/` come
from the App Store screenshots (`cwebp`); `og-*.png` are the social cards.
Plain HTML and CSS, readable without JavaScript; motion respects
"Reduce Motion".
