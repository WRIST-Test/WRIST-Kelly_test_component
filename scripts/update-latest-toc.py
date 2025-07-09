#!/usr/bin/env python3
import os
import re

README = "README.md"
LATEST_DIR = "latest"
START_MARKER = "<!-- LATEST_START -->"
END_MARKER   = "<!-- LATEST_END -->"

def build_toc():
    entries = sorted(os.listdir(LATEST_DIR))
    lines = []
    for e in entries:
        path = os.path.join(LATEST_DIR, e)
        if os.path.isdir(path):
            # directory: keep the same behavior
            lines.append(f"* **{e}/**")
            for sub in sorted(os.listdir(path)):
                lines.append(f"  * [{sub}]({path}/{sub})")
        else:
            # file: do *not* append `/{e}` again
            lines.append(f"* [{e}]({path})")
    return "\n".join(lines)

def inject_toc(readme_text: str, toc_md: str) -> str:
    try:
        before, rest = readme_text.split(START_MARKER, 1)
        _, after  = rest.split(END_MARKER,   1)
    except ValueError:
        raise RuntimeError("Could not find both START and END markers in README.md")

    return (
        before
      + "Table of Contents:\n"
      + START_MARKER
      + "\n\n"
      + toc_md.strip()       # your generated bullets
      + "\n\n"
      + END_MARKER
      + after
    )

def main():
    with open(README, "r", encoding="utf-8") as f:
        content = f.read()

    toc = build_toc()
    new_content = inject_toc(content, toc)
    if new_content == content:
        print("WARNING: No changes made to README.md")
        return

    with open(README, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ Injected latest TOC into", README)

if __name__ == "__main__":
    main()
