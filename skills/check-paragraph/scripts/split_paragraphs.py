#!/usr/bin/env python3
"""Split a .tex file into numbered paragraphs; print one JSON object per line."""
import json, re, sys

SECTION = re.compile(r"\x5c(?:sub)*section\*?\{((?:[^{}]|\{[^{}]*\})*)\}")


def clean(text):
    """Strip % comments (not \\%) and \\taylor{...} blocks, keeping newlines."""
    out, i, depth = [], 0, 0
    while i < len(text):
        c = text[i]
        if depth:  # inside \taylor{...}
            depth += (c == "{") - (c == "}")
            if c == "\n":
                out.append(c)
        elif text.startswith("\\taylor{", i):
            i += len("\\taylor{"); depth = 1; continue
        elif c == "%" and (i == 0 or text[i - 1] != "\\"):
            i = text.find("\n", i)
            if i < 0:
                break
            continue
        else:
            out.append(c)
        i += 1
    return "".join(out)


def main(path):
    lines = clean(open(path, encoding="utf-8").read()).split("\n")
    start = next((k for k, l in enumerate(lines) if "\\begin{document}" in l), -1) + 1
    paras, cur, cur_start, section, n = [], [], None, "", 0
    for k in range(start, len(lines)):
        line = lines[k]
        if "\\end{document}" in line:
            break
        m = SECTION.search(line)
        if m:
            section = m.group(1); line = line[:m.start()] + line[m.end():]
        if line.strip():
            if cur_start is None:
                cur_start = k
            cur.append(line); cur_end = k
            continue
        if cur:
            text = "\n".join(cur).strip()
            if paras and re.match(r"\x5cbegin\{", text):
                paras[-1]["text"] += "\n" + text; paras[-1]["line_end"] = cur_end + 1
            else:
                n += 1
                paras.append({"n": n, "line_start": cur_start + 1, "line_end": cur_end + 1,
                              "section": section, "text": text})
        cur, cur_start = [], None
    for p in paras:
        print(json.dumps(p, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
