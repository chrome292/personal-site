# conormaloney.me — static site

## Deploy (drag and drop)
1. Netlify → project "conormaloney" → Deploys.
2. Drag the `site` folder (not the zip, not this outer folder) onto the deploy drop zone.
3. Domain settings: make sure https://conormaloney.me is the primary domain (www redirects to it).

## Deploy (Git, optional)
Push this whole folder to a repo and link it. netlify.toml publishes `site/` and runs `python3 build.py`.

## Editing
All copy lives in `build.py`. Change it, run `python3 build.py`, redeploy `site/`.
- Add GitHub / HARDWEAR links: add them to the LINKS list at the top of build.py.
- Changing the domain: edit SITE at the top of build.py.
Small edits can also be made directly in the site/*.html files, but build.py will overwrite them next time it runs.

## After deploying
- Google Search Console: add the domain, submit https://conormaloney.me/sitemap.xml.
- Check the link preview: paste the URL into https://www.linkedin.com/post-inspector/ .
