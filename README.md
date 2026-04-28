<div align="center">

# GUST, by [Nautilus Labs](https://github.com/nautilus-os)

![version](https://img.shields.io/badge/version-1.0-blue?style=flat-square)
![license](https://img.shields.io/badge/license-AGPLv3-green?style=flat-square)
![no service workers](https://img.shields.io/badge/service%20workers-absolutely%20not-red?style=flat-square)

</div>

---

## What is this?

GUST is a full-featured web proxy that lives entirely inside a single HTML file, allowing you to use it without any setup, hosting, or terminal access. It was built by the Nautilus Labs team to be a replacement for every single other proxy out there, and to put an end to school blocked proxies once and for all. 

---

## Why schools can't block it 

Every single web proxy out there relies on something called a **Service Worker**, a background script that intercepts network requests before they reach the browser. It's an integral part of any other web proxy you use, allowing the proxy to communicate with its server and proxy your requests, but Service Workers ALWAYS require a live server to function. That means traditional proxies only work when hosted at a specific URL. Block that URL, and the proxy is dead. You're probably already familiar with the cat-and-mouse game between you and your admin, where someone makes a link, it gets used for a day or two, then gets blocked.

School network filters, admin installed extensions (think Securly,  Lightspeed Systems, Securly, Linewize, Blocksi, etc.) and admin-controlled browsers (like Chromebook MDM policies) are very good at exactly this. Your school maintains blocklists, with specific sites added every day to this list of sites you can't access. Many filtering extensions also have more advanced features, where they read a links metadata to detect proxy patterns and automatically add them to the blocklist. An even higher number of these extensions control what can run in the background, which is a big achilles heel for every single current proxy site available. 
GUST doesn't use Service Workers at all. Heres what we came up with instead:

<img width="1440" height="1040" alt="image" src="https://github.com/user-attachments/assets/f5403020-c0b4-4d89-b795-cfa11b898c78" /><br>

Instead, it uses **libcurl.js**, a full HTTP library compiled to WebAssembly, to make requests directly through a WebSocket tunnel called the WISP protocol. (Thanks to Mercury Workshop for these) The entire proxy engine runs as plain JavaScript inside a single HTML file. This means:

- ✅ **It can run as a local file** (`file://`), with no server and no domain to block
- ✅ **It can be hosted anywhere static files work**: GitHub Pages, Vercel, Netlify, a USB drive, a Google Doc, a Google Site, etc.
- ✅ **It has no Service Worker to kill**, because it never registered one
- ✅ **It survives tab crashes and memory pressure**, cause it has no background worker to lose
- ✅ **It can be renamed, embedded in an iframe, or wrapped in another HTML file**, giving the filter nothing to latch onto
- ✅ **It can be copy-pasted into any WYSIWYG HTML editor on the web**, because again, it's just HTML with CSS and JS inlined
- ✅ **It can be compiled into a blob: or data: url and opened that way**, again, HTML

The short version: most blockers can only block URLs. GUST is a file. You can't block a file without obliterating a cruical part of the student user experience, and even if they take that drastic step, well, HTML can be hosted or opened in litrally anything. It's the frame of the world wide web. no more whack-a-mole, cat-and-mouse game of finding unblocked links and your school blocking them!

---

## Pics
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/93db1bf0-2e4e-431e-a273-79f9229df4f4" />
<img width="1919" height="969" alt="image" src="https://github.com/user-attachments/assets/fcc15a77-dde1-4d22-bfc7-d809acfe2891" />
<img width="1920" height="973" alt="image" src="https://github.com/user-attachments/assets/c1388250-65a4-4878-9481-a2539c33079e" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3d332a9f-7713-419d-9350-bbe6c104a892" />
<img width="1920" height="973" alt="image" src="https://github.com/user-attachments/assets/3254ba60-0636-4ae9-962c-7173c0b358de" />
<img width="1920" height="973" alt="image" src="https://github.com/user-attachments/assets/0914ae53-eb7c-432a-9566-55c6923818ed" />
<img width="1920" height="973" alt="image" src="https://github.com/user-attachments/assets/17fb9ac8-15c8-4881-b65f-a0dc92324256" />

---

## How it works

When you type a URL, GUST fetches the entire page through a WebAssembly HTTP client, rewrites every resource URL, injects a proxy runtime script, and renders the result in a sandboxed iframe. Here's what that looks like step by step:

<img width="1440" height="1178" alt="image" src="https://github.com/user-attachments/assets/c2cbd934-4c5f-4341-95ae-190c9f66d828" /><br>


Every page GUST loads gets a small script injected before anything else runs. This script intercepts virtually every way a page can try to escape the proxy: `location.href`, `window.open`, form submissions, `XMLHttpRequest`, `fetch`, `WebSocket`, `Worker`, `EventSource`, history API pushes, anchor clicks, and even the Navigation API used by modern SPAs. It also spoofs `document.cookie`, `localStorage`, `sessionStorage`, and IndexedDB so pages behave as if they're on their real origin. All network traffic also flows through a WISP WebSocket server, so your real IP is never exposed to the sites you visit. The WISP server acts as a TCP/TLS relay, and the destination server only ever sees the relay's address, not yours. You can self-host a WISP server or use a public one, and GUST supports server switching in settings.

---

## Features

GUST ships with more features than a proxy arguably needs, but we wanted your proxy browser experience to be as close to your normal one as possible.

**Browser UX**
- Multi-tab browsing with drag-to-reorder, mute, and tab caching
- Bookmarks bar with favicon support
- New tab page with favorites, clock, and customizable wallpaper
- Recent browser history (stored locally)
- Address bar with search engine integration (Brave, Bing)
- All expected nav buttons

**Privacy & blocking**
- Built-in ad and tracker blocker with cosmetic filtering and customizable CSS filter rules
- User-agent spoofing (request headers and `navigator.userAgent`)
- WebRTC blocking to prevent IP leaks
- Cookie jar isolation per origin

**Developer tools**
- Real-time request log with filtering, search, and type badges
- DOM element inspector with styles, box model, and attributes panels
- Browser metrics panel (heap, cache, network, page performance)
- Drag-to-resize side panels, left/right panel position toggle

**File handling**
- Built-in PDF viewer (PDF.js, paginated with zoom)
- Built-in image viewer (zoom, pan, download)
- Built-in video and audio players
- Built-in text/code viewer with syntax highlighting
- Range request support for video seeking
- File downloading is proxied through GUST

**Settings**
- WISP server configuration with per-instance storage isolation
- Concurrent request thread controls
- Font size slider, panel width persistence
- Bookmarks bar toggle, clock format (12/24h)
- Keyboard shortcut editor
- Full reset option (for when things go wrong, which they sometimes do)
- A whole ton of options dude just look at it yourself (28 options!)

---

## Getting started

**Option 1:  Just open the file**

Download `index.html` and open it in any modern browser. That's it. That's the whole setup.

**Option 2: Host it**

Drop `index.html` on any static host. GitHub Pages, Vercel, Cloudflare Pages, Netlify, your university's free web hosting that's been running since 2003. They all work fine.

**Option 3: Embed it**

Put it inside another HTML file as an `<iframe>`. Works from a Blob URL. Works from a data URI (though large). Basically works from anywhere.

---

## Tech stack

| Library | Version | Purpose |
|---------|---------|---------|
| libcurl.js | latest | HTTP client (WebAssembly) |
| WISP protocol | — | WebSocket TCP tunneling |
| PDF.js | 4.2.67 | In-browser PDF rendering |
| Font Awesome | 6.5.1 | Icons |
| JetBrains Mono | — | Monospace font |
| Space Grotesk | — | UI font |
| iso-639-1 | 2.1.11 | Language codes (for the language feature that is currently broken) |

---

## Credits

| Person | What they actually did |
|--------|----------------------|
| **lanefiedler** | Built the original proxy framework and UI shell, which was built upon to become the proxy you see today |
| **dinguschan** | Redesigned the browser interface, rewrote large portions of the proxy JS, added most of the current features |
| **x8rr** | Ported GUST to SVG, Bug reports, feedback, light assistance, and the parts of this README |
| **Mercury Workshop** | Created the WISP protocol, the WebSocket tunneling layer that makes this all possible |
| **ading2210** | Built libcurl.js, which is curl compiled to WebAssembly (absolute clutchup) |
| **Mozilla Foundation** | PDF.js, honestly dude I can't write an entire PDF handler thats just too much and this already exists |

---

## Known bugs and limitations

- Some complex web features can't be fully proxied: native WebSockets from within a page, WebRTC (intentionally blockable via settings), and service workers inside proxied pages
- Some links can't be followed inside GUST. For now just drag the link to the omnibox :/.
- The language/spellcheck feature is listed in settings and labeled `[BROKEN]`. We know. It'l be fixed eventually
- Very JavaScript-heavy SPAs may have edge cases in navigation interception.

---

<div align="center">

Made with ❤️ by Nautilus Labs

</div>
