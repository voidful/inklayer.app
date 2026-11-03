#!/usr/bin/env python3
"""Builds the inklayer.app pages.

    python3 build.py [path/to/store_assets/public_web/published]

The home pages (English and Traditional Chinese) come from the copy below.
The privacy policy and support pages come from the published copies in the
InkLayer repository (`store_assets/public_web/published/`), the same text the
App Store and Google Play link to, wrapped in this site's header and footer.
Every claim on the home page must hold for the version in the App Store;
the panel near the end lists what the latest version added.
"""

import html
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent
PUBLISHED = Path(
    sys.argv[1]
    if len(sys.argv) > 1
    else Path.home()
    / "PycharmProjects/Codex/2026-10-08/task/InkLayer/store_assets/public_web/published"
)
APP_STORE = "https://apps.apple.com/app/id6824608659"
SUPPORT_EMAIL = "support@eric-lam.com"

# --- Icons (24×24, stroked like the app's outlined icons) --------------------

def icon(paths: str) -> str:
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>'
    )


ICONS = {
    "account": icon('<circle cx="12" cy="8" r="3.5"/><path d="M5 20c1.2-3.6 4-5.5 7-5.5s5.8 1.9 7 5.5"/><path d="M4 4l16 16"/>'),
    "offline": icon('<path d="M2.5 9.5a14 14 0 0 1 5-3"/><path d="M12 5.5a14 14 0 0 1 9.5 4"/><path d="M6 13a9 9 0 0 1 4-2"/><path d="M15.5 12a9 9 0 0 1 2.5 1"/><circle cx="12" cy="18" r="1.2"/><path d="M3 3l18 18"/>'),
    "privacy": icon('<path d="M12 3l7 3v5c0 4.6-2.9 8.4-7 10-4.1-1.6-7-5.4-7-10V6z"/><path d="M9 12l2 2 4-4"/>'),
    "folder": icon('<path d="M3.5 7.5a2 2 0 0 1 2-2h4l2 2h7a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z"/>'),
    "sync": icon('<path d="M20 11a8 8 0 0 0-14.3-4.6L4 8"/><path d="M4 4v4h4"/><path d="M4 13a8 8 0 0 0 14.3 4.6L20 16"/><path d="M20 20v-4h-4"/>'),
    "pencil": icon('<path d="M4 20l1-4L16.5 4.5a2.1 2.1 0 0 1 3 3L8 19z"/><path d="M14.5 6.5l3 3"/>'),
    "mic": icon('<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0"/><path d="M12 17.5V21"/>'),
    "present": icon('<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8"/><path d="M12 16v4"/><path d="M10 8.5l4 1.8-4 1.7z"/>'),
    "eink": icon('<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8.5 8h7"/><path d="M8.5 11.5h7"/><path d="M8.5 15h4"/>'),
    "export": icon('<path d="M12 15V3.5"/><path d="M8 7.5l4-4 4 4"/><path d="M5 12v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/>'),
    "lock": icon('<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>'),
}

# --- Hand-drawn ink ------------------------------------------------------------

CIRCLE = (
    '<svg class="circle" viewBox="0 0 400 100" preserveAspectRatio="none" aria-hidden="true">'
    '<path class="ink-stroke draw" style="--len:1100" stroke="var(--red-ink)" stroke-width="4" '
    'vector-effect="non-scaling-stroke" d="M30 22C120 4 300 2 372 22c34 10 30 40-6 54-70 26-250 26-320 8'
    'C2 72-6 44 34 26c40-16 110-20 170-18"/></svg>'
)
ARROW = (
    '<svg class="arrow" viewBox="0 0 160 120" aria-hidden="true">'
    '<path class="ink-stroke draw" style="--len:320" stroke="var(--navy-ink)" stroke-width="4" '
    'd="M10 14c40-6 96 6 118 52 6 13 9 26 10 40"/>'
    '<path class="ink-stroke draw" style="--len:80" stroke="var(--navy-ink)" stroke-width="4" '
    'd="M120 92l18 18 12-26"/></svg>'
)
SCRIBBLE = (
    '<svg class="scribble" viewBox="0 0 260 120" aria-hidden="true"><path class="ink-stroke" '
    'stroke="currentColor" stroke-width="5" d="M8 80c30-60 60-60 70-10s40 40 60-10 50-50 70 0 30 30 44 10"/></svg>'
)


def layers_art(labels: dict) -> str:
    """Three sheets stacked, drawn in the app's three inks."""
    sheets = [
        ("var(--navy-ink)", 190, labels["pdf"]),
        ("var(--green-ink)", 120, labels["text"]),
        ("var(--red-ink)", 50, labels["ink"]),
    ]
    parts = []
    for color, y, label in sheets:
        parts.append(
            f'<path d="M70 {y}l170 0c14 0 22 4 30 12l58 52c6 6 2 10-6 10H150c-12 0-20-4-28-12l-58-52c-6-6-4-10 6-10z" '
            f'fill="var(--paper)" fill-opacity="0.92" stroke="{color}" stroke-width="3.5" stroke-linejoin="round"/>'
            f'<text class="layer-label" x="352" y="{y + 44}">{html.escape(label)}</text>'
        )
    # A little writing on the top sheet and a line of text on the middle one.
    parts.append(
        '<path class="ink-stroke" stroke="var(--red-ink)" stroke-width="3" '
        'd="M140 70c12-10 22 8 32-2s22 8 34-2 20 6 30 0"/>'
        '<path class="ink-stroke" stroke="var(--green-ink)" stroke-width="3" opacity="0.6" d="M150 142h90M162 154h60"/>'
    )
    return (
        '<div class="layers-art" role="img" aria-label="'
        + html.escape(labels["aria"])
        + '"><svg viewBox="0 0 460 300" aria-hidden="true">'
        + "".join(parts)
        + "</svg></div>"
    )


# --- Copy ---------------------------------------------------------------------

COPY = {
    "en": {
        "lang": "en",
        "file": "index.html",
        "other_file": "/index.zh-TW.html",
        "other_label": "繁體中文",
        "other_lang": "zh-Hant",
        "suffix": "en",
        "title": "InkLayer — Handwriting, PDFs and notes on one canvas",
        "description": "InkLayer puts handwriting, PDFs and Markdown notes on one canvas, in files you own. For iPhone, iPad and Mac. No account, no ads, no tracking.",
        "nav": [("#features", "Features"), ("#yours", "Your files"), ("#pricing", "Pricing"), ("/support/", "Support")],
        "cta": "Get InkLayer",
        "eyebrow": "For iPhone, iPad and Mac",
        "h1": 'Handwriting, PDFs and notes, on <span class="inked">one canvas{circle}</span>.',
        "lede": "InkLayer keeps every layer separate and every file yours: write on PDFs without changing them, link Markdown notes, and lay it all out side by side.",
        "cta_note": "Free to download · No account needed",
        "badge_alt": "Download on the App Store",
        "hero_alt": "InkLayer on a Mac: a canvas with notes, a PDF page and handwriting",
        "phone_alt": "InkLayer on iPhone: handwriting on a PDF",
        "promises": [("account", "No account"), ("offline", "Works offline"), ("privacy", "No ads, no tracking"), ("folder", "Files you own")],
        "features": [
            {
                "id": "pdf", "kicker": "PDF annotation",
                "h2": 'Write on any PDF. <span class="marker">The original stays untouched.</span>',
                "p": "Mark up lecture slides, papers and contracts with Apple Pencil or a stylus. Your handwriting lives beside the PDF, so the file you imported never changes, and exporting puts it all together when you need it.",
                "checks": ["Pens, highlighters, shapes and a lasso", "Select text to copy, translate or quote in a note", "Handwriting you can search, recognised on the device"],
                "img": "ipad-pdf", "alt": "InkLayer on iPad: a PDF with handwriting, highlights and drawings", "device": "tablet",
            },
            {
                "id": "layers", "kicker": "Layers",
                "h2": "Everything is a layer.",
                "p": "The PDF, typed text, handwriting and images stay separate. Hide what you don't need, lock what's finished, and choose where new ink goes.",
                "checks": ["Show, hide and lock each layer", "Drag layers into the order you want", "Export with or without your ink"],
                "art": {"pdf": "PDF", "text": "Text & images", "ink": "Handwriting", "aria": "Three layers: a PDF at the bottom, text and images above it, handwriting on top"},
            },
            {
                "id": "notes", "kicker": "Markdown notes",
                "h2": "Notes that link to each other.",
                "p": "Write in Markdown with links between notes, backlinks, tags and maths. A graph shows how your ideas connect. Every note is an ordinary .md file.",
                "checks": ["[[Links]], backlinks and tags", "Inline and display maths", "Handwriting right on the note"],
                "img": "mac-note", "alt": "InkLayer on a Mac: a Markdown note with handwriting", "device": "window",
            },
            {
                "id": "canvas", "kicker": "Infinite canvas",
                "h2": "A desk for all your ideas.",
                "p": "Lay out pages, PDF pages, notes, images, video and recordings side by side on an infinite canvas, then write across all of them. When it's time to share, play it as slides.",
                "checks": ["Cards you can move, resize and lock", "Paper pages with grids and lines", "Masking tape to quiz yourself"],
                "img": "ipad-canvas", "alt": "InkLayer on iPad: a canvas of cards, a PDF and a mind map in ink", "device": "tablet",
            },
        ],
        "yours_h2": "Your notes. Your files.",
        "yours_p": "There's no cloud account to sign up for. A library is a folder on your device, and it stays readable without InkLayer.",
        "cards": [
            ("folder", "Yours to keep", "A library is a folder of Markdown, PDFs and small sidecar files. Open it with other apps; back it up anywhere."),
            ("privacy", "Private by design", "No account, no ads, no analytics. Handwriting, speech and translation are handled on the device, and nothing you write is sent to us."),
            ("sync", "Sync your way", "Keep your library in iCloud Drive, or sync it through your own Google Drive or WebDAV server. When two edits clash, both are kept."),
        ],
        "chips": [("iCloud Drive", False), ("Google Drive", False), ("WebDAV", False)],
        "grid_h2": "Made for the way you work.",
        "grid": [
            ("pencil", "Apple Pencil", "Pressure-sensitive ink, palm rejection, and shapes that straighten themselves."),
            ("mic", "Recordings", "Record while you write and your notes replay with it, stroke by stroke. A transcript makes every word searchable."),
            ("present", "Present", "Play PDFs and canvas pages as slides, with a laser pointer."),
            ("eink", "E-ink mode", "No animation and higher contrast, for e-paper tablets."),
            ("export", "Export", "Export a PDF with your ink, or a canvas as a PDF, an image or a video."),
            ("lock", "Encrypted backups", "Export the whole library, optionally encrypted with a passphrase."),
        ],
        "soon_badge": "New",
        "soon_h2": "InkLayer 1.1",
        "soon": [
            ("iCloud Drive and Google Drive sync", "Keep a library in sync across your devices; when two edits clash, both are kept."),
            ("PDF text into notes", "Select text to copy, translate or add to a note, or circle a passage with the lasso to quote it with its page."),
            ("Transcripts and live captions", "Turn recordings into searchable text on the device, tap a sentence to hear it, and follow a class with live captions."),
            ("Search inside PDFs", "Library search now finds the text of your PDFs and your recording transcripts."),
            ("Flowcharts", "Join canvas cards with arrows that follow them as you move them."),
            ("Databases", "Arrange documents in tables you can filter and sort, and export them as one PDF."),
            ("Writing feel", "Finer brushes, and ink that keeps closer to the tip of your pen."),
            ("Your toolbar, your keys", "Choose the tools you see. ⌘T adds a text box, ⌘/ lists every shortcut, and input methods keep working."),
        ],
        "soon_note": "Out now on iPhone and iPad; the Mac update is in App Review. Transcripts and live captions need iOS, iPadOS or macOS 26; translation needs iOS or iPadOS 18, or macOS 15.",
        "pricing_h2": "Free to start. Yours for good.",
        "pricing_p": "Every feature is in the free version. Lifetime removes one limit, once.",
        "plans": [
            ("Free", "Free download", ["Every feature", "Handwriting in 3 documents", "Typing, reading and exporting without limits"], False),
            ("InkLayer Lifetime", "One purchase, no subscription", ["Handwriting in every document", "Future on-device feature updates included", "One purchase for iPhone, iPad and Mac"], True),
        ],
        "plans_note": "Nothing you write is ever locked, with or without Lifetime. The price is set by your App Store region.",
        "closing_h2": "Start on one canvas.",
        "closing_p": "Free to download. No account. Open it and write.",
        "footer": [("/viewer/", "Web Viewer"), ("/privacy/", "Privacy Policy"), ("/support/", "Support"), (f"mailto:{SUPPORT_EMAIL}", "Contact")],
        "skip": "Skip to content",
    },
    "zh": {
        "lang": "zh-Hant",
        "file": "index.zh-TW.html",
        "other_file": "/",
        "other_label": "English",
        "other_lang": "en",
        "suffix": "zh",
        "title": "InkLayer — 手寫、PDF 與筆記，都在同一張畫布上",
        "description": "InkLayer 把手寫、PDF 與 Markdown 筆記放在同一張畫布上，存成屬於你的檔案。支援 iPhone、iPad 與 Mac。不需要帳號，沒有廣告與追蹤。",
        "nav": [("#features", "功能"), ("#yours", "你的檔案"), ("#pricing", "價格"), ("/support.zh-TW.html", "支援")],
        "cta": "免費下載",
        "eyebrow": "iPhone、iPad、Mac 都能用",
        "h1": '手寫、PDF 與筆記，<br>都在<span class="inked">同一張畫布{circle}</span>上。',
        "lede": "InkLayer 讓每一層各自分開，每個檔案都屬於你：在 PDF 上書寫而不改動原檔、用連結串起 Markdown 筆記，再把一切並排在畫布上。",
        "cta_note": "免費下載 · 不需要帳號",
        "badge_alt": "在 App Store 下載",
        "hero_alt": "Mac 上的 InkLayer：放著筆記、PDF 頁面與手寫的畫布",
        "phone_alt": "iPhone 上的 InkLayer：在 PDF 上手寫",
        "promises": [("account", "不需要帳號"), ("offline", "離線也能用"), ("privacy", "沒有廣告與追蹤"), ("folder", "檔案屬於你")],
        "features": [
            {
                "id": "pdf", "kicker": "PDF 註記",
                "h2": '在任何 PDF 上書寫，<span class="marker">原檔一字不改。</span>',
                "p": "用 Apple Pencil 或觸控筆標註講義、論文與合約。手寫存在 PDF 旁邊，匯入的檔案永遠不會被修改；需要時再匯出合在一起的 PDF。",
                "checks": ["原子筆、螢光筆、形狀與套索", "選取文字，拷貝、翻譯或引用到筆記", "在裝置上辨識手寫，可以搜尋"],
                "img": "ipad-pdf", "alt": "iPad 上的 InkLayer：有手寫、螢光筆與圖畫的 PDF", "device": "tablet",
            },
            {
                "id": "layers", "kicker": "圖層",
                "h2": "每一樣東西，都是一個圖層。",
                "p": "PDF、打字、手寫與圖片各自分開。隱藏用不到的、鎖住已完成的，也能指定新的筆跡要寫在哪一層。",
                "checks": ["每一層都能顯示、隱藏與鎖定", "拖曳就能調整圖層順序", "匯出時可選擇要不要帶上手寫"],
                "art": {"pdf": "PDF", "text": "文字與圖片", "ink": "手寫", "aria": "三個圖層：最下面是 PDF，中間是文字與圖片，最上面是手寫"},
            },
            {
                "id": "notes", "kicker": "Markdown 筆記",
                "h2": "會互相連結的筆記。",
                "p": "用 Markdown 書寫，筆記之間可以連結，有反向連結、標籤與數學式。關聯圖讓你看見想法怎麼串在一起。每則筆記都是一般的 .md 檔案。",
                "checks": ["[[連結]]、反向連結與標籤", "行內與獨立的數學式", "直接在筆記上手寫"],
                "img": "mac-note", "alt": "Mac 上的 InkLayer：有手寫的 Markdown 筆記", "device": "window",
            },
            {
                "id": "canvas", "kicker": "無限畫布",
                "h2": "一張放得下所有想法的桌子。",
                "p": "把頁面、PDF 頁面、筆記、圖片、影片與錄音並排在無限畫布上，再跨越它們書寫。要分享時，直接當投影片播放。",
                "checks": ["卡片可以移動、縮放與鎖定", "方格、橫線等各種紙張", "遮蓋膠帶，拿來考自己"],
                "img": "ipad-canvas", "alt": "iPad 上的 InkLayer：卡片、PDF 與手繪心智圖組成的畫布", "device": "tablet",
            },
        ],
        "yours_h2": "你的筆記，你的檔案。",
        "yours_p": "沒有雲端帳號要你註冊。筆記庫就是你裝置上的一個資料夾，不開 InkLayer 也讀得到。",
        "cards": [
            ("folder", "永遠是你的", "筆記庫是由 Markdown、PDF 與小小的附屬檔組成的資料夾。其他 App 也打得開，想備份到哪裡都可以。"),
            ("privacy", "從設計就重視隱私", "沒有帳號、沒有廣告、沒有分析。手寫辨識、語音轉文字與翻譯都在裝置上完成，你寫的內容不會傳給我們。"),
            ("sync", "用你的方式同步", "把筆記庫放在 iCloud 雲碟，或透過你自己的 Google 雲端硬碟、WebDAV 伺服器同步。兩邊同時修改時，兩個版本都會保留。"),
        ],
        "chips": [("iCloud 雲碟", False), ("Google 雲端硬碟", False), ("WebDAV", False)],
        "grid_h2": "細節裡的用心。",
        "grid": [
            ("pencil", "Apple Pencil", "感壓筆觸、防誤觸，畫好的形狀會自動修整。"),
            ("mic", "錄音", "邊寫邊錄，播放時筆記會跟著聲音一筆一筆重現；逐字稿讓每句話都搜尋得到。"),
            ("present", "簡報", "把 PDF 與畫布頁面當投影片播放，還有雷射筆。"),
            ("eink", "電子紙模式", "關閉動畫、提高對比，適合電子紙平板。"),
            ("export", "匯出", "匯出含手寫的 PDF，或把畫布匯出成 PDF、圖片或影片。"),
            ("lock", "加密備份", "整個筆記庫一次匯出，也可以用密碼加密。"),
        ],
        "soon_badge": "新功能",
        "soon_h2": "InkLayer 1.1",
        "soon": [
            ("iCloud 雲碟與 Google 雲端硬碟同步", "在多台裝置間同步筆記庫；兩邊同時修改時，兩個版本都會保留。"),
            ("PDF 文字擷取到筆記", "選取文字就能拷貝、翻譯或加到筆記；用套索圈住一段，連同頁碼引用到筆記。"),
            ("逐字稿與即時字幕", "在裝置上把錄音轉成可以搜尋的文字，點一句就從那裡播放；上課時開即時字幕。"),
            ("搜尋 PDF 內文", "筆記庫搜尋也找得到 PDF 裡的文字和錄音逐字稿。"),
            ("流程圖", "用箭頭連起畫布上的卡片，移動卡片時箭頭會跟著走。"),
            ("資料庫", "用表格整理文件，可以篩選、排序，並合成一份 PDF 匯出。"),
            ("書寫手感", "筆刷可以調得更細，筆跡更貼近筆尖。"),
            ("你的工具列與快速鍵", "自己決定工具列放哪些工具。⌘T 開文字框、⌘/ 看所有快速鍵，打注音也不會被打斷。"),
        ],
        "soon_note": "iPhone 與 iPad 已可更新，Mac 版正在審核。逐字稿與即時字幕需要 iOS、iPadOS 或 macOS 26；翻譯需要 iOS／iPadOS 18 或 macOS 15。",
        "pricing_h2": "先免費用，喜歡再買斷。",
        "pricing_p": "免費版就有所有功能。終身版只解除一個限制，一次就好。",
        "plans": [
            ("免費版", "免費下載", ["所有功能", "在 3 份文件中手寫", "打字、閱讀與匯出不受限制"], False),
            ("InkLayer 終身版", "一次購買，沒有訂閱", ["每一份文件都能手寫", "之後裝置上的功能更新都包含在內", "iPhone、iPad、Mac 共用一次購買"], True),
        ],
        "plans_note": "不論有沒有購買，你寫下的內容都不會被鎖住。價格依你所在地區的 App Store 而定。",
        "closing_h2": "從一張畫布開始。",
        "closing_p": "免費下載，不需要帳號，打開就能寫。",
        "footer": [("/viewer/", "網頁檢視器"), ("/privacy.zh-TW.html", "隱私權政策"), ("/support.zh-TW.html", "支援"), (f"mailto:{SUPPORT_EMAIL}", "聯絡我們")],
        "skip": "跳到內容",
    },
}

# --- Page parts -------------------------------------------------------------------

SCRIPT = """<script>
if ('IntersectionObserver' in window) document.documentElement.classList.add('js');
addEventListener('DOMContentLoaded', () => {
  if (!('IntersectionObserver' in window)) return;
  const seen = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        seen.unobserve(entry.target);
      }
    }
  }, { rootMargin: '0px 0px -10% 0px' });
  document.querySelectorAll('.reveal').forEach((el) => seen.observe(el));
});
</script>"""


def head(c: dict, title: str, description: str, path: str, alternate: str) -> str:
    url = f"https://inklayer.app{path}"
    return f"""<!doctype html>
<html lang="{c['lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="theme-color" content="#f5fbf6" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#1a1e1c" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="{c['other_lang']}" href="https://inklayer.app{alternate}">
  <link rel="alternate" hreflang="{c['lang']}" href="{url}">
  <link rel="icon" href="/favicon.png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="InkLayer">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://inklayer.app/assets/img/og-{c['suffix']}.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="apple-itunes-app" content="app-id=6824608659">
  <link rel="stylesheet" href="/assets/css/site.css">
  {SCRIPT}
</head>"""


def header(c: dict, home: bool) -> str:
    links = "".join(
        f'<a href="{href if home or not href.startswith("#") else ("/" if c["suffix"] == "en" else "/index.zh-TW.html") + href}">{html.escape(label)}</a>'
        for href, label in c["nav"]
    )
    home_href = "/" if c["suffix"] == "en" else "/index.zh-TW.html"
    return f"""<a class="skip" href="#main">{c['skip']}</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{home_href}"><img src="/assets/img/icon-128.png" alt="" width="34" height="34">InkLayer</a>
    <nav class="nav" aria-label="InkLayer">{links}<a class="lang" href="{c['other_file']}" hreflang="{c['other_lang']}" lang="{c['other_lang']}">{c['other_label']}</a></nav>
    <a class="header-cta" href="{APP_STORE}">{html.escape(c['cta'])}</a>
  </div>
</header>"""


def footer(c: dict) -> str:
    links = "".join(f'<a href="{href}">{html.escape(label)}</a>' for href, label in c["footer"])
    return f"""<footer class="site-footer">
  <div class="wrap">
    <a class="brand" href="{'/' if c['suffix'] == 'en' else '/index.zh-TW.html'}"><img src="/assets/img/icon-128.png" alt="" width="34" height="34">InkLayer</a>
    <span>© 2026 voidful</span>
    <nav aria-label="Footer">{links}<a href="{c['other_file']}" hreflang="{c['other_lang']}" lang="{c['other_lang']}">{c['other_label']}</a></nav>
  </div>
</footer>"""


def badge(c: dict) -> str:
    return (
        f'<a class="store-badge" href="{APP_STORE}">'
        f'<img src="/assets/img/app-store-badge.svg" alt="{html.escape(c["badge_alt"])}" width="162" height="54"></a>'
    )


def device(kind: str, src: str, alt: str) -> str:
    img = f'<img src="/assets/img/{src}.webp" alt="{html.escape(alt)}" loading="lazy" decoding="async">'
    if kind == "window":
        return f'<div class="window"><div class="bar"><i></i><i></i><i></i></div>{img}</div>'
    return f'<div class="tablet">{img}</div>'


def home(c: dict) -> str:
    s = c["suffix"]
    h1 = c["h1"].replace("{circle}", CIRCLE)
    promises = "".join(f"<li>{ICONS[i]}{html.escape(t)}</li>" for i, t in c["promises"])
    features = []
    for n, f in enumerate(c["features"]):
        checks = "".join(f"<li>{html.escape(x)}</li>" for x in f["checks"])
        media = layers_art(f["art"]) if "art" in f else device(f["device"], f"{f['img']}-{s}", f["alt"])
        features.append(
            f"""<section class="feature reveal{' flip' if n % 2 else ''}" id="{f['id']}">
      <div class="feature-copy">
        <p class="kicker">{html.escape(f['kicker'])}</p>
        <h2>{f['h2']}</h2>
        <p>{html.escape(f['p'])}</p>
        <ul class="checks">{checks}</ul>
      </div>
      <div class="media">{media}</div>
    </section>"""
        )
    chips = "".join(f'<span class="chip{" soon" if soon else ""}">{html.escape(t)}</span>' for t, soon in c["chips"])
    cards = []
    for n, (i, h, p) in enumerate(c["cards"]):
        extra = f'<div class="sync-row">{chips}</div>' if n == 2 else ""
        cards.append(f'<article class="card reveal"><div class="glyph">{ICONS[i]}</div><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p>{extra}</article>')
    tiles = "".join(
        f'<article class="tile reveal"><h3>{ICONS[i]}{html.escape(h)}</h3><p>{html.escape(p)}</p></article>' for i, h, p in c["grid"]
    )
    soon = "".join(f"<li><strong>{html.escape(h)}</strong><span>{html.escape(p)}</span></li>" for h, p in c["soon"])
    plans = []
    for name, price, items, featured in c["plans"]:
        lis = "".join(f"<li>{html.escape(x)}</li>" for x in items)
        plans.append(f'<article class="plan reveal{" featured" if featured else ""}"><h3>{html.escape(name)}</h3><p class="price">{html.escape(price)}</p><ul>{lis}</ul></article>')
    return f"""{head(c, c['title'], c['description'], '/' if s == 'en' else '/index.zh-TW.html', c['other_file'])}
<body>
{header(c, True)}
<main id="main">
  <section class="hero">
    <div class="wrap">
      <div class="hero-copy">
        <p class="eyebrow">{html.escape(c['eyebrow'])}</p>
        <h1>{h1}</h1>
        <p class="lede">{html.escape(c['lede'])}</p>
        <div class="cta-row">{badge(c)}<span class="cta-note">{html.escape(c['cta_note'])}</span></div>
      </div>
      <div class="stage">
        {ARROW}
        <div class="window"><div class="bar"><i></i><i></i><i></i></div><img src="/assets/img/mac-canvas-{s}.webp" alt="{html.escape(c['hero_alt'])}" width="2000" height="1250" fetchpriority="high"></div>
        <div class="phone"><img src="/assets/img/iphone-pdf-{s}.webp" alt="{html.escape(c['phone_alt'])}" width="640" height="1391" loading="lazy"></div>
      </div>
    </div>
  </section>
  <div class="wrap">
    <ul class="promises">{promises}</ul>
    <div id="features">
    {''.join(features)}
    </div>
    <section id="yours">
      <div class="section-head reveal"><h2>{html.escape(c['yours_h2'])}</h2><p>{html.escape(c['yours_p'])}</p></div>
      <div class="cards">{''.join(cards)}</div>
    </section>
    <section>
      <div class="section-head reveal"><h2>{html.escape(c['grid_h2'])}</h2></div>
      <div class="grid">{tiles}</div>
    </section>
    <section class="soon-panel reveal" id="next">
      <span class="badge-11">{html.escape(c['soon_badge'])}</span>
      <h2>{html.escape(c['soon_h2'])}</h2>
      <ul class="soon-list">{soon}</ul>
      {f'<p class="soon-note">{html.escape(c["soon_note"])}</p>' if c.get("soon_note") else ""}
    </section>
    <section id="pricing">
      <div class="section-head reveal"><h2>{html.escape(c['pricing_h2'])}</h2><p>{html.escape(c['pricing_p'])}</p></div>
      <div class="plans">{''.join(plans)}</div>
      <p class="plans-note">{html.escape(c['plans_note'])}</p>
    </section>
    <section class="closing reveal">
      {SCRIBBLE.replace('class="scribble"', 'class="scribble" style="left:-40px;top:20px"')}
      {SCRIBBLE.replace('class="scribble"', 'class="scribble" style="right:-30px;bottom:10px;transform:scaleX(-1)"')}
      <h2>{html.escape(c['closing_h2'])}</h2>
      <p>{html.escape(c['closing_p'])}</p>
      <div class="cta-row">{badge(c)}</div>
    </section>
  </div>
</main>
{footer(c)}
</body>
</html>
"""


# --- Legal pages ---------------------------------------------------------------

LINKS = [
    ('src="inklayer_icon.png"', 'src="/assets/img/icon-128.png"'),
    ('href="inklayer_privacy_zh-TW.html"', 'href="/privacy.zh-TW.html"'),
    ('href="inklayer_privacy.html"', 'href="/privacy/"'),
    ('href="inklayer_support_zh-TW.html"', 'href="/support.zh-TW.html"'),
    ('href="inklayer_support.html"', 'href="/support/"'),
    ('href="inklayer_zh-TW.html"', 'href="/index.zh-TW.html"'),
    ('href="inklayer.html"', 'href="/"'),
]


def legal(source: str, c: dict, path: str, alternate: str) -> str:
    text = (PUBLISHED / source).read_text()
    title = re.search(r"<title>(.*?)</title>", text, re.S).group(1).strip()
    description = re.search(r'<meta name="description" content="([^"]*)"', text)
    body = re.search(r"<main>(.*)</main>", text, re.S).group(1)
    body = re.sub(r'\s*<img src="inklayer_icon.png"[^>]*>', "", body, count=1)
    for a, b in LINKS:
        body = body.replace(a, b)
    left = re.findall(r'(?:href|src)="inklayer[^"]*"', body)
    assert not left, (source, left)
    return f"""{head(c, title, html.unescape(description.group(1)) if description else title, path, alternate)}
<body>
{header(c, False)}
<main id="main">
  <div class="wrap">
    <article class="doc">{body}</article>
  </div>
</main>
{footer(c)}
</body>
</html>
"""


def write(path: str, content: str) -> None:
    target = SITE / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)


def main() -> None:
    en, zh = COPY["en"], COPY["zh"]
    write("index.html", home(en))
    write("index.zh-TW.html", home(zh))
    privacy = legal("inklayer_privacy.html", en, "/privacy/", "/privacy.zh-TW.html")
    write("privacy/index.html", privacy)
    write("privacy.html", privacy)
    write("privacy.zh-TW.html", legal("inklayer_privacy_zh-TW.html", zh, "/privacy.zh-TW.html", "/privacy/"))
    support = legal("inklayer_support.html", en, "/support/", "/support.zh-TW.html")
    write("support/index.html", support)
    write("support.html", support)
    write("support.zh-TW.html", legal("inklayer_support_zh-TW.html", zh, "/support.zh-TW.html", "/support/"))
    write("404.html", legal_404(en))
    print("built", SITE)


def legal_404(c: dict) -> str:
    return f"""{head(c, 'Page not found — InkLayer', 'This page does not exist.', '/404.html', '/')}
<body>
{header(c, False)}
<main id="main">
  <div class="wrap">
    <article class="doc"><h1>Page not found</h1><p>This page does not exist. <a href="/">InkLayer home</a> · <a href="/support/">Support</a></p></article>
  </div>
</main>
{footer(c)}
</body>
</html>
"""


if __name__ == "__main__":
    main()
