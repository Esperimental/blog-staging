# Hugo blog

Minimal Hugo implementation selected after comparison with [the Eleventy experiment](https://github.com/Esperimental/tmp-blog-eleventy).

The same source tree is used by two repositories:

- [`blog-staging`](https://github.com/Esperimental/blog-staging) is the development source and publishes the preview site.
- [`blog`](https://github.com/Esperimental/blog) is its GitHub fork and publishes only manually reviewed production revisions.

Development starts in staging. Promotion and synchronization use Git commits and cross-repository pull requests—never file copying. See [the manual review and promotion workflow](PROMOTION.md).

Same two sample posts and author data; Hugo templates replace Nunjucks. No external theme, npm packages, Sass or Go modules.

Requires Hugo 0.166.0 (the standard Linux binary works).

```sh
hugo --baseURL https://example.test/blog-staging/
python3 scripts/check-output.py public /blog-staging/
hugo server
```

Select **Settings → Pages → Source → GitHub Actions** once in each repository. A push to `main` publishes that repository's site; pull requests build without deploying.

- Posts: `content/posts/`
- Settings: `hugo.toml`
- Authors: `data/authors.json`
- Layouts: `layouts/`
- CSS source: `assets/style.css`
- Workflow: `.github/workflows/pages.yml`

The stylesheet is minified and fingerprinted during the build so browsers do not keep stale CSS after a deployment.

Posts without local media can be single Markdown files. Posts with images use a leaf bundle:

```text
content/posts/my-post/
├── index.md
└── image.webp
```

Reference the image with ordinary Markdown:

```md
![Useful alt text](image.webp "Optional visible caption")
```

The custom Markdown image renderer resolves the adjacent page resource and adds intrinsic dimensions, lazy loading and the optional caption. This keeps post content portable and avoids shortcode syntax for normal images.

[Setup guide](SETUP.md). Branding and the second sample post remain provisional.
