# THE INTAKE — deployment handoff

Everything needed to put `painbet-intake-scroll.html` on the live domain.

## What it is

A single static HTML page. **No build step, no bundler, no server-side code, no
database, no environment variables.** The repo has no `package.json` and nothing
to compile — the file you ship is the file in the repo.

It needs a static host that can serve files. That is the whole requirement.

## Files to ship

Three things, and the folder structure has to survive intact:

```
painbet-intake-scroll.html
assets/seq/                 film + door1-4, 2,192 frames   119.7 MB
assets/wheel/plate.webp     the wheel plate                  1.4 MB
```

> **`plate.webp` is easy to miss.** Ship only the HTML and `assets/seq/` and
> everything appears to work right up until the dispensary, where the wheel
> renders as prize labels floating on nothing. It is the only 404.
>
> Equally, **do not copy all of `assets/wheel/`** — the other files in there are
> superseded artwork, about 12 MB that is never loaded. Copy that one file.

All paths are relative, so the page can live at the domain root or under any
subpath (`/intake/`, `/admissions/`, …) as long as the `assets` folder sits
beside the HTML. Verified working from a subdirectory.

| Path | Contents | Size |
|---|---|---|
| `painbet-intake-scroll.html` | the page itself | 0.1 MB |
| `assets/seq/film/` | 1,444 frames, the main film | 77.4 MB |
| `assets/seq/door1/` | 169 frames, into Room 02 | 9.0 MB |
| `assets/seq/door2/` | 193 frames, into Discharge | 9.7 MB |
| `assets/seq/door3/` | 193 frames, the locker | 8.6 MB |
| `assets/seq/door4/` | 193 frames, into the Dispensary | 15.0 MB |
| `assets/wheel/plate.webp` | the daily wheel plate | 1.4 MB |
| | **total** | **121.2 MB** |

Frames are `frame_0001.webp` … numbered from 1, zero-padded to four digits. The
page builds those filenames itself, so **do not rename, renumber or re-encode
them.**

### Deliberately not needed

These are in the repo but never loaded at runtime — around 12 MB that does not
need to go to the CDN:

- `assets/wheel/plate.png`, `plate_labeled.png`, `plate_labeled.webp` — earlier
  artwork. The live page draws the wheel labels itself onto `plate.webp`.
- `assets/wheel/PLATE_SPEC.md` and the other `*-HANDOFF.md` / `*-PROMPTS.md`
  files — internal documentation.

## One dependency outside the repo

The "Enter the Ward" button at the end links to **`index.html`**, relative to
wherever the page is served from. Either ship the main site alongside it, or
change that one `href` to the correct live URL. It is the only outbound link.

## Fonts

The page pulls Archivo, Archivo Black and JetBrains Mono from Google Fonts over
CDN. **Verified: if that request is blocked or fails, the page still renders and
works** — it falls back to system fonts, with no console errors.

Self-hosting the three families is the safer option for a production domain
(no third-party request, no layout shift), but it is not required to go live.

## Hosting notes

Ordinary static hosting is fine — S3 + CloudFront, Cloudflare Pages, Netlify,
Vercel, nginx, anything. Four things are worth getting right:

**Serve over HTTP/2 or HTTP/3.** The scrub loader requests many small images in
parallel. HTTP/1.1 caps at roughly six connections per host and the film will
visibly stutter.

**Cache the frames hard.** They are immutable — new footage would arrive as a
new folder, never as a changed file:

```
/assets/seq/**   Cache-Control: public, max-age=31536000, immutable
/assets/wheel/** Cache-Control: public, max-age=31536000, immutable
*.html           Cache-Control: no-cache          # so updates land immediately
```

**Compress the HTML, not the images.** Brotli or gzip on `.html` is worth it
(152 KB of markup and script). WebP is already compressed; re-compressing it
wastes CPU for nothing.

**Confirm `.webp` is served as `image/webp`.** Correct on every modern host, but
worth checking on a hand-rolled nginx config.

## Bandwidth, realistically

The full sequence set is 121 MB, but **nobody downloads all of it.** Frames load
in a window around the scroll position and stay cached once fetched. Measured on
a cold open at 390 px wide: **723 frames, 8.6 MB in the first few seconds.**
A visitor who scrolls the whole way through pulls more, but only the scenes they
actually reach.

Worth sizing CDN egress against real traffic rather than against the 121 MB
figure.

## Before it goes live

- [ ] Page loads and the corridor scrubs as you scroll
- [ ] `.webp` returns `image/webp`, not `application/octet-stream`
- [ ] No 404s under `/assets/seq/` in the network tab
- [ ] "Enter the Ward" at the end goes somewhere real
- [ ] The five stations gate correctly: quiz, wallet, discharge, locker,
      dispensary — a fast swipe must not skip past one
- [ ] The daily wheel spins and lands on the wedge it says it landed on
- [ ] Checked on a real phone, not just a narrow desktop window

## Where the moving parts live

All inside `painbet-intake-scroll.html`, if anything needs adjusting later:

- `SCENES` — scene order, frame ranges, copy
- `FILM` / `DOOR_FILMS` — the frame sequences and their counts
- `WHEEL` / `WEDGES` / `WEDGE_BG` — prizes, odds, and the wheel's painted wedges
  (see `assets/wheel/PLATE_SPEC.md`)
- `PACE` — walking speed and the auto-play timings
