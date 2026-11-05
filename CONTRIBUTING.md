# Contributing to heleo.space

Thank you for helping. Every change goes through a pull request and is reviewed before it reaches the live site.

1. Create a branch (or fork the repo) and make your change.
   - Page text, header and footer: edit `_build/build.py`, then run `python3 _build/build.py` and commit both `_build/` and the regenerated `site/`.
   - A new update post: add a Markdown file to `site/updates/posts/` and its name to `site/updates/posts.json` (see README).
2. Open a pull request against `main` and describe what changed and why.
3. A preview link appears on the pull request within a minute or two. Check your change there.
4. The site owner reviews the preview and merges, asks for changes, or closes the pull request.

Rules
- Do not add names of people, partners or contributors, or any financial, investment or fundraising content, to the site.
- Use only images and video that are public domain or free to use, and add each source to the Credits page.
- Never commit passwords, keys or personal email addresses.
- The contact form (PHP) works only on the live site, not on preview links.
