# Hugo versus Eleventy: prototype comparison

Date: 10 September 2026. Decision: **Hugo for this standalone blog**. `blog-staging` is the permanent proving ground; `blog` and `site` remain separate production repositories.

## Evidence

- [Hugo live prototype](https://esperimental.github.io/blog-staging/)
- [Eleventy live prototype](https://esperimental.github.io/tmp-blog-eleventy/)
- [Hugo build, editorial trials and deployment](https://github.com/Esperimental/tmp-blog-hugo/actions/runs/34432031330)
- [Eleventy successful build and deployment](https://github.com/Esperimental/tmp-blog-eleventy/actions/runs/34431356672)
- Each repository contains scripts/editorial-trials.py. It modifies a disposable source copy, builds after each change and checks the generated result.

## What stayed equivalent

Two matching Markdown posts, matching author data, identical CSS, and closely matching homepage/post markup. Repository source links differ appropriately. The second post is a formatting fixture, not a real experiment report. Both are static builds deployed using GitHub Actions and Pages.

This is not a pixel-identical rendering comparison: generators have their own Markdown/code rendering defaults. Hugo also generates a posts section index, giving four checked HTML pages versus Eleventy's three.

## Results

| Check | Eleventy 3.1.6 | Hugo 0.166.0 |
| --- | --- | --- |
| Build and Pages deployment | Passed in Actions | Passed in Actions |
| Existing internal links/assets | 10 references across 3 HTML pages passed locally | 14 references across 4 HTML pages passed in Actions |
| Add a Markdown post and second author | Passed locally | Passed in Actions |
| Index discovers added post | Passed locally | Passed in Actions |
| Edit existing post body | Passed locally | Passed in Actions |
| Change shared layout | Passed locally on home and post | Passed in Actions on home and post |
| Change site title | Passed locally on home and post | Passed in Actions on home and post |
| Alternate /preview/ path in editing trials | Passed locally | Passed in Actions |
| Public home, both posts and CSS | Retrieved successfully | Retrieved successfully, HTTP 200 |
| Browser visual review | Outstanding | Completed on the published staging site |

The editorial trials use a clearly marked temporary post dated 2020, a second author, a changed notebook label and a changed site title. Nothing from those trials is published. Scripts use temporary directories and leave original source unchanged.

Reproduce Eleventy trials after npm ci:
```sh
python3 scripts/editorial-trials.py eleventy .
```

Reproduce Hugo trials with Hugo on PATH:
```sh
python3 scripts/editorial-trials.py hugo .
```

Hugo executes these trials in its current workflow. Eleventy's trials were run locally and the script is preserved in its repository; they have not been added to its workflow.

## Maintenance differences

| Area | Eleventy implementation | Hugo implementation |
| --- | --- | --- |
| Generator installation | Node.js + one direct npm dependency; installation added 129 packages | One pinned Hugo release executable |
| Dependency reproducibility | package-lock.json + npm ci | Hugo version pinned in workflow; no project packages |
| Templates | Nunjucks, close to HTML with expressions and tags | Go templates, more specialised syntax |
| Site metadata | JSON | TOML |
| Shared author defaults | Directory data file | Section cascade |
| URL prefix | SITE_PATH_PREFIX + url filter | baseURL + relURL/RelPermalink |
| Custom processing | Straightforward JavaScript extension point | Hugo template/functions system |
| Extra output | Only explicitly configured pages | Section index appears naturally |

“No project packages” refers to the Hugo site build; both workflows still use GitHub Actions with their own dependencies. Neither prototype needs a theme, Sass pipeline, client-side framework, Go compiler or application backend.

## What went wrong and what it means

Eleventy's early deployment attempts stopped at Configure Pages because the repository had not been configured for Actions publishing. Selecting that source and rerunning resolved it. Hugo's first deployment passed after the repository was configured. That difference is setup chronology, not evidence that one generator deploys more reliably.

Local Hugo binary download was blocked in this workspace; GitHub Actions downloaded and ran it successfully. Eleventy installed locally in 57 seconds and in the first Actions run in five seconds. These are environment-specific observations.

Live HTTP checks passed. The Hugo staging site also received a completed browser review of its home page, post layout, bundled image and fingerprinted stylesheet.

## Timing observations, not a benchmark

Eleventy reported 0.08–0.09 seconds for its small local builds. Hugo reported 9–10 ms for its initial Actions builds. Different machines, outputs and runtimes mean these values are not a fair speed comparison. Both are comfortably fast enough for this scope, and workflow startup/deployment time matters more.

## Recommendation and trade-off

Choose Hugo for the standalone blog: the tested publishing and editing requirements all work, while this implementation avoids an npm dependency tree. The principal cost is learning and maintaining Go-template syntax.

Eleventy remains a good choice if custom JavaScript data processing becomes central, or its template/configuration style proves more comfortable during ongoing work. Neither prototype demonstrated a decisive functional limitation.

## Next steps

1. Use `blog-staging` for layout, workflow and content-pipeline changes.
2. Promote proven revisions into `blog`.
3. Keep `site` as a separate front door and games as separate products.
4. Use these records as evidence for a later narrative post; this document is an engineering comparison, not the finished story.
