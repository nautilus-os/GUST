<div align="center">

# GUST Browser

**simply better**

*by [Nautilus Labs](https://github.com/nautilus-os)*

![version](https://img.shields.io/badge/version-1.0-blue?style=flat-square)
![license](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![no service workers](https://img.shields.io/badge/service%20workers-absolutely%20not-red?style=flat-square)

</div>

---

## What is this?

GUST is a full-featured web proxy that lives entirely inside a single HTML file. No installation. No server setup. No npm, no Webpack, no 47-step build process. Just one file you can open, share, or host anywhere. It works.

It was built by the Nautilus Labs team and features more functionality than a proxy has any right to have, including tabs, bookmarks, an ad blocker, a developer log panel, an element inspector, a file viewer, history tracking, browser metrics, and a settings panel with more knobs than a recording studio.

We're proud of it, mostly.

---

## Why schools can't block it *(yes, this section is for you)*

Most web proxies rely on something called a **Service Worker**, a background script that intercepts network requests before they reach the browser. It's clever tech, but it has one fatal weakness: Service Workers require a live server to function. That means traditional proxies only work when hosted at a specific URL. Block that URL, and the proxy is dead.

School network filters and admin-controlled browsers (like Chromebook MDM policies) are very good at exactly this. They maintain blocklists. They detect proxy patterns. They kill Service Workers. It's practically their hobby.

GUST doesn't use Service Workers at all.

<img width="1440" height="1040" alt="image" src="https://github.com/user-attachments/assets/f5403020-c0b4-4d89-b795-cfa11b898c78" />


Instead, it uses **libcurl.js**, a full HTTP library compiled to WebAssembly, to make requests directly through a WebSocket tunnel called the WISP protocol. The entire proxy engine runs as plain JavaScript inside a single HTML file. This means:

- ✅ **It can run as a local file** (`file://`), with no server and no domain to block
- ✅ **It can be hosted anywhere static files work**: GitHub Pages, Vercel, Netlify, a USB drive, a Google Doc
- ✅ **It has no Service Worker to kill**, because it never registered one
- ✅ **It survives tab crashes and memory pressure**, with no background worker to lose
- ✅ **It can be renamed, embedded in an iframe, or wrapped in another HTML file**, giving the filter nothing to latch onto

The short version: most blockers can only block URLs. GUST is a file. You can't block a file you've never seen.

> **A note on responsibility:** With great unblockability comes great responsibility. Don't use this to do things you'd regret, and don't use it to harm others. We built it for freedom of information, not chaos.

---

## How it works

When you type a URL, GUST fetches the entire page through a WebAssembly HTTP client, rewrites every resource URL, injects a proxy runtime script, and renders the result in a sandboxed iframe. Here's what that looks like step by step:

<img width="1440" height="1178" alt="image" src="https://github.com/user-attachments/assets/c2cbd934-4c5f-4341-95ae-190c9f66d828" />


### The proxy runtime

Every page GUST loads gets a small script injected before anything else runs. This script intercepts virtually every way a page can try to escape the proxy: `location.href`, `window.open`, form submissions, `XMLHttpRequest`, `fetch`, `WebSocket`, `Worker`, `EventSource`, history API pushes, anchor clicks, and even the Navigation API used by modern SPAs. It also spoofs `document.cookie`, `localStorage`, `sessionStorage`, and IndexedDB so pages behave as if they're on their real origin.

It does a lot. It's about 1,500 lines of JavaScript. We're not entirely sure how it got this long.

### The WISP tunnel

All network traffic flows through a WISP WebSocket server. Your real IP is never exposed to the sites you visit. The WISP server acts as a TCP/TLS relay. The destination server only ever sees the relay's address, not yours. You can self-host a WISP server or use a public one.

---

## Features

GUST ships with more features than a proxy arguably needs. We regret nothing.

**Browser chrome**
- Multi-tab browsing with drag-to-reorder, mute, and tab caching
- Bookmarks bar with favicon support
- New tab page with favorites, clock, and customizable wallpaper
- Full browser history (last 20 sites, stored locally)
- Address bar with search engine integration (Brave, Bing)

**Privacy & blocking**
- Built-in ad and tracker blocker with cosmetic filtering
- Custom CSS filter rules (AdBlock-style)
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

**Settings**
- WISP server configuration with per-instance storage isolation
- Concurrent request thread controls
- Font size slider, panel width persistence
- Bookmarks bar toggle, clock format (12/24h)
- Keyboard shortcut editor
- Full reset option (for when things go wrong, which they sometimes do)

---

## Getting started

**Option 1 — Just open the file**

Download `index.html` and open it in any modern browser. That's it. That's the whole setup.

**Option 2 — Host it**

Drop `index.html` on any static host. GitHub Pages, Vercel, Cloudflare Pages, Netlify, your university's free web hosting that's been running since 2003. They all work fine.

**Option 3 — Embed it**

Put it inside another HTML file as an `<iframe>`. Works from a Blob URL. Works from a data URI (though large). Basically works from anywhere.

---

## Technical stack

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
| **lanefiedler** | Built the original proxy framework and UI shell, which somehow became all of this |
| **dinguschan** | Redesigned the browser interface, rewrote large portions of the proxy JS, added most features |
| **x8rr** | Bug reports, feedback, light assistance, and the parts of this README that don't sound like a robot wrote them |
| **Mercury Workshop** | Created the WISP protocol, the WebSocket tunneling layer that makes this all possible |
| **ading2210** | Built libcurl.js, which is curl compiled to WebAssembly and is either genius or cursed (probably both) |
| **Mozilla Foundation** | PDF.js, because rendering PDFs in a browser proxy is apparently something we needed |

---

## Known limitations

- Some complex web features can't be fully proxied: native WebSockets from within a page, WebRTC (intentionally blockable via settings), and service workers inside proxied pages
- The language/spellcheck feature is listed in settings and labeled `[BROKEN]`. We know. It stays because removing it would mean admitting defeat
- Very JavaScript-heavy SPAs may have edge cases in navigation interception. If you find one, open an issue
- The proxy runtime is injected into every page. This is necessary and also slightly rude

---

<div align="center">

Made with ❤️ by Nautilus Labs · [GitHub](https://github.com/nautilus-os/GUST)

*"It's a single HTML file. It really shouldn't do all this."*

</div>
