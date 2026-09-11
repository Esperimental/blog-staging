"""Exercise common editorial changes in a disposable copy; never edit source."""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

kind = sys.argv[1]
source = Path(sys.argv[2] if len(sys.argv) > 2 else ".").resolve()
assert kind in ("hugo", "eleventy")
with tempfile.TemporaryDirectory(prefix="blog-edit-trial-") as tmp:
    work = Path(tmp) / "site"
    shutil.copytree(source, work, ignore=shutil.ignore_patterns(".git", "node_modules", "public", "_site", ".sites-runtime"))
    if kind == "hugo":
        posts, authors, layout = "content/posts", "data/authors.json", "layouts/baseof.html"
        cmd = ["hugo", "--baseURL", "https://example.test/preview/"]
        output = work / "public"
    else:
        posts, authors, layout = "src/posts", "src/_data/authors.json", "src/_includes/base.njk"
        cmd = ["node", str(source / "node_modules/@11ty/eleventy/cmd.cjs"), "--pathprefix=/preview/"]
        output = work / "_site"
    def build():
        result = subprocess.run(cmd, cwd=work, text=True, capture_output=True)
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
    post = work / posts / "editing-trial.md"
    post.write_text("---\ntitle: Editing trial\ndate: 2020-01-01\nauthor: reviewer\n---\nOriginal trial body.\n")
    author_file = work / authors
    data = json.loads(author_file.read_text())
    data["reviewer"] = {"name": "Trial reviewer"}
    author_file.write_text(json.dumps(data))
    build()
    page = output / "posts/editing-trial/index.html"
    assert "Original trial body." in page.read_text()
    assert "Trial reviewer" in page.read_text()
    assert "Editing trial" in (output / "index.html").read_text()
    print("PASS: add post and second author; index discovers post")
    post.write_text(post.read_text().replace("Original trial body.", "Revised trial body."))
    build()
    assert "Revised trial body." in page.read_text()
    assert "Original trial body." not in page.read_text()
    print("PASS: edit existing post")
    template = work / layout
    template.write_text(template.read_text().replace("Notebook / 001", "Notebook / trial"))
    build()
    assert "Notebook / trial" in page.read_text()
    assert "Notebook / trial" in (output / "index.html").read_text()
    print("PASS: shared layout update reaches home and post")
    if kind == "hugo":
        config = work / "hugo.toml"
        config.write_text(config.read_text().replace("An open experiment", "Trial site title"))
    else:
        config = work / "src/_data/site.json"
        data = json.loads(config.read_text())
        data["title"] = "Trial site title"
        config.write_text(json.dumps(data))
    build()
    assert "Trial site title" in page.read_text()
    assert "Trial site title" in (output / "index.html").read_text()
    rendered = page.read_text()
    if kind == "hugo":
        assert "/preview/style." in rendered and ".css" in rendered
    else:
        assert "/preview/assets/style.css" in rendered
    print("PASS: site title update; alternate deployment prefix")
print("All editorial trials passed in disposable copy; source unchanged.")
