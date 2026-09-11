"""Validate every generated HTML local link and basic blog content."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import sys

root = Path(sys.argv[1])
prefix = sys.argv[2]
assert prefix.startswith("/") and prefix.endswith("/")
checked = []
class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key not in ("href", "src") or not value or value.startswith("#"):
                continue
            url = urlsplit(value)
            if url.scheme or url.netloc:
                continue
            assert url.path.startswith(prefix), value
            target = root / unquote(url.path[len(prefix):])
            if url.path.endswith("/"):
                target /= "index.html"
            assert target.is_file(), (value, target)
            checked.append(value)

pages = list(root.rglob("*.html"))
assert len(pages) >= 3
for path in pages:
    Links().feed(path.read_text())
home = (root / "index.html").read_text()
assert home.index("Hello world") < home.index("A second entry")
assert "The inventor" in (root / "posts/hello-world/index.html").read_text()
styles = list(root.glob("style.*.css"))
assert len(styles) == 1 and styles[0].stat().st_size > 0
print(f"PASS: {len(pages)} HTML pages, {len(checked)} local references; newest first and author rendered")
