# heleo.space website

Source for [heleo.space](https://heleo.space), the Heleospace company website. It is plain static HTML with a small Python generator, a little JavaScript, and a PHP contact form. There are no dependencies to install.

## Layout

| Path | What it is |
|---|---|
| `_build/build.py` | Page text, header, footer and nav. Generates the HTML in `site/`. |
| `_build/brand_assets.py` | Makes every logo file, favicon and the brand kit zip from `_build/brand/heleospace-logo-source.svg`. |
| `site/` | The web root. Generated HTML plus the hand-written files below. |
| `site/assets/` | Stylesheet, JavaScript and images (hand-written). |
| `site/contact/*.php` | Contact form handler and human check (hand-written). |
| `site/updates/posts/` | Update posts in Markdown (hand-written). |
| `.github/workflows/deploy.yml` | Optional FTP deploy, off by default. |
| `netlify.toml` | Preview builds for pull requests. |

Do not hand-edit generated HTML, because the next build overwrites it.

## Run it locally

```
python3 _build/build.py
cd site && python3 -m http.server
```

Then open http://localhost:8000. Use the local server rather than opening the files directly, because updates load with JavaScript. The PHP contact form only works on a host with PHP.

## Change a page

Edit `_build/build.py`, run `python3 _build/build.py`, and commit both `_build/` and the regenerated `site/`. Site-wide settings such as the contact email and social links are at the top of that file.

## Add an update post

1. Add a Markdown file to `site/updates/posts/`, for example `first-lab-results.md` (lower-case letters, numbers and dashes only):

   ```
   ---
   title: First radiation test results
   date: 2026-12-15
   category: Research
   summary: One sentence that appears on the card and at the top of the post.
   image: https://www.nasa.gov/wp-content/uploads/2023/03/iss066e152098.jpg
   image_alt: Describe the image
   image_credit: NASA
   author: Heleospace
   ---

   Write the post here in Markdown: paragraphs, **bold**, lists, tables, links, > quotes.
   ```

2. Add the file name (without `.md`) to `site/updates/posts.json`.

The post appears on the home page (latest 3) and at /updates/, newest first. Add `draft: true` to hide a post.

## Logo

To change the logo, replace `_build/brand/heleospace-logo-source.svg`, then run `python3 _build/brand_assets.py` and `python3 _build/build.py`. PNG files are rendered with Google Chrome. If the logo's proportions change, update the size in `LOGO` in `_build/build.py` and in `site/assets/css/site.css`.

## Media

All photos and video must be public domain or freely licensed, and each source must be listed on the /credits/ page. Most media loads from its source; the URLs are in the `M` list in `_build/build.py`. Local copies go in `site/assets/media/`. `hero-launch.mp4` there is the Pexels model rocket clip listed on /credits/ (Kindel Media), scaled to 1080p with its edges slightly cropped and its audio removed.

## Analytics

Set `GA_ID` at the top of `_build/build.py`. Analytics loads only after a visitor clicks **Accept** in the cookie banner, and the choice can be changed from **Cookie settings** in the footer. With `GA_ID` empty, no banner shows and nothing loads.

## Contact form

The form posts to `site/contact/send.php`, which sends mail with PHP `mail()`. Spam protection is a human-check sum, a hidden honeypot field, a minimum fill time and a limit per visitor per hour. Settings are at the top of `send.php`.

## 404 page

`site/.htaccess` points missing pages at `404.html`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
