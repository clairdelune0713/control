"""Turn the raw crawled prompts (prompts/) into a browsable reference library (library/).

library/
  README.md            how to navigate
  TEMPLATE.md          hand-written prompt skeleton (not generated, never overwritten)
  INDEX.md             every shot, grouped by scene, with tags
  TAGS.md              shots grouped by shot size / camera / dialogue / format / duration / model
  ELEMENTS.md          characters, locations, props: reference images + how prompts describe them
  REUSABLE_BLOCKS.md   section bodies reused verbatim across shots (boilerplate locks)
  sections/            every distinct variant of each prompt section, from final versions
  shots/<scene>/       one file per shot: final prompt + earlier versions
"""
import collections
import difflib
import glob
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "prompts")
OUT = os.path.join(HERE, "library")
FAMILY_SIMILARITY = 0.6

HEADER_RE = re.compile(r"^[A-Z0-9][A-Z0-9 &/\-\(\),:—'.]{3,70}$")
UUID_REF_RE = re.compile(r"<<<([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})>>>")
NEGATION_RE = re.compile(r"\b(no|not|never|without|nor|zero|avoid)\b[^.;:\n]{0,30}$", re.I)

# Section library: canonical name -> (file, predicate on normalised header)
SECTION_ORDER = [
    ("SCENE CONTEXT", lambda h: h == "SCENE CONTEXT"),
    ("OUTPUT SETTINGS", lambda h: h.startswith("OUTPUT SETTINGS")),
    ("FORMAT MODE", lambda h: h.startswith("FORMAT MODE")),
    ("ACTIVE REFERENCES", lambda h: h.startswith("ACTIVE REFERENCES")),
    ("LOCATION MAP", lambda h: h.startswith("LOCATION MAP") or h.startswith("GEOGRAPHY")),
    ("FIRST FRAME", lambda h: h.startswith("FIRST FRAME")),
    ("FRAMING", lambda h: h.startswith("FRAMING") or h == "CAMERA AND FRAMING"),
    ("ACTION TIMING", lambda h: h.startswith("ACTION TIMING") or h == "ACTION"),
    ("DIALOGUE", lambda h: h.startswith("DIALOGUE")),
    ("BREATHING", lambda h: h.startswith("BREATHING")),
    ("OPTICS", lambda h: h.startswith("OPTICS")),
    ("CAMERA", lambda h: h.startswith("CAMERA") and "LOCK" not in h),
    ("PHYSICS", lambda h: h.startswith("PHYSICS")),
    ("LIGHTING", lambda h: h.startswith("LIGHTING")),
    ("AUDIO", lambda h: h.startswith("AUDIO") or h.startswith("NO MUSIC")),
    ("LOCKS", lambda h: "LOCK" in h),
    ("POSITIVE CONSTRAINTS", lambda h: h.startswith("POSITIVE CONSTRAINTS") or h == "CONSTRAINTS"),
    ("NEGATIVE CONSTRAINTS", lambda h: h.startswith("NEGATIVE")),
    ("PERFORMANCE AND INTENT", lambda h: True),  # everything else: THE FACE, WHAT THIS SHOT IS DOING, ...
]

SIZE_PATTERNS = [
    ("Extreme close-up", r"extreme close[- ]?up|\becu\b|macro"),
    ("Insert", r"\binsert\b"),
    ("Medium close-up", r"medium close[- ]?up|\bmcu\b"),
    ("Close-up", r"close[- ]?up|\btight\b"),
    ("Medium", r"medium shot|medium wide|\bmedium\b|waist"),
    ("Wide", r"\bwide\b|establishing|full[- ]body|full shot|aerial|top[- ]down|overhead"),
]
CAMERA_PATTERNS = [
    ("Handheld", r"handheld|hand-held|shoulder-mounted"),
    ("Locked-off", r"tripod|locked[- ]off|locked\b|fixed mount|static|clamped"),
    ("Dolly / push-in", r"dolly|slider|push[- ]in|pushes in|creep"),
    ("Orbit", r"\borbit"),
    ("Tracking", r"tracking|follows? (him|her|them)|walks with"),
    ("Crane / high angle", r"crane|high[- ]angle|top[- ]down|overhead"),
    ("Drone / aerial", r"drone|aerial"),
]


def slug(s, n=60):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:n].rstrip("-") or "untitled"


def rel(path, start):
    return os.path.relpath(path, start).replace(os.sep, "/").replace(" ", "%20")


def first_unnegated(pattern, text):
    for m in re.finditer(pattern, text, re.I):
        if not NEGATION_RE.search(text[max(0, m.start() - 40):m.start()]):
            return m.start()
    return None


def parse_raw(path):
    t = open(path).read()
    meta = dict(re.findall(r"^- \*\*(.+?):\*\* (.+)$", t, re.M))
    dur = re.search(r"\*\*Duration:\*\* (\S+?)s · \*\*Aspect:\*\* (\S+) · \*\*Resolution:\*\* (\S+)", t)
    refs = {}
    for m in re.finditer(r"^- `([0-9a-f-]{36})` → \*\*(.+?)\*\* \((.+?)\)(?: · (\S+))?", t, re.M):
        refs[m.group(1)] = {"name": m.group(2), "category": m.group(3).replace("auto:", ""), "img": m.group(4)}
    prompt = t.split("```text\n", 1)[1].split("\n```", 1)[0]
    shots = re.findall(r"### Shot \d+\n\n```text\n(.*?)\n```", t, re.S)
    gens = re.findall(r"^- (\S+ \S+) · `([0-9a-f-]+)` · (\S+)$", t, re.M)
    folder = os.path.relpath(os.path.dirname(path), RAW)
    return {
        "path": path,
        "folder": folder,
        "model": meta.get("Model", "?"),
        "duration": dur.group(1) if dur else "?",
        "aspect": dur.group(2) if dur else "?",
        "resolution": dur.group(3) if dur else "?",
        "created": meta.get("Created", "").replace(" UTC", ""),
        "takes": len(gens),
        "gens": gens,
        "refs": refs,
        "prompt": prompt,
        "shots": shots,
    }


def readable(text, refs):
    return UUID_REF_RE.sub(lambda m: f"<<<{refs[m.group(1)]['name']}>>>" if m.group(1) in refs else m.group(0), text)


def split_sections(prompt):
    secs, cur, buf, pre = [], None, [], []
    for line in prompt.split("\n"):
        s = line.strip().rstrip(":")
        if HEADER_RE.match(s) and sum(c.isalpha() for c in s) >= 4 and not s.startswith(("0:", "1.", "2.")):
            if cur:
                secs.append((cur, "\n".join(buf).strip()))
            cur, buf = s, []
        elif cur:
            buf.append(line)
        else:
            pre.append(line)
    if cur:
        secs.append((cur, "\n".join(buf).strip()))
    if "\n".join(pre).strip():
        secs.insert(0, ("(PREAMBLE)", "\n".join(pre).strip()))
    return secs


def canonical(header):
    h = header.split(" — ")[0].strip()
    for name, pred in SECTION_ORDER:
        if pred(h) or pred(header):
            return name
    return "PERFORMANCE AND INTENT"


def scene_context(p):
    for h, body in p["sections"]:
        if h == "SCENE CONTEXT":
            return body
    return p["prompt"]


def title_of(p):
    text = re.sub(r"\s+", " ", readable(scene_context(p), p["refs"])).strip()
    text = re.sub(r"<<<(.+?)>>>", r"\1", text)
    sent = ""
    for part in re.split(r"(?<=[.!?])\s", text):
        sent = f"{sent} {part}".strip()
        if len(sent) >= 40:
            break
    return sent if len(sent) <= 120 else sent[:117].rsplit(" ", 1)[0] + "…"


def tags_of(p):
    secs = {canonical(h): b for h, b in p["sections"]}
    ctx = scene_context(p)
    framing = " ".join(secs.get(k, "") for k in ("FRAMING", "FIRST FRAME", "FORMAT MODE", "OUTPUT SETTINGS", "OPTICS"))
    tags = {}

    def pick(patterns, *texts):
        for text in texts:
            hits = [(first_unnegated(rx, text), name) for name, rx in patterns]
            hits = [h for h in hits if h[0] is not None]
            if hits:
                return min(hits)[1]
        return None

    tags["size"] = pick(SIZE_PATTERNS, ctx, framing, p["prompt"]) or "Unspecified"
    cam_text = secs.get("CAMERA", "") + " " + secs.get("FORMAT MODE", "") + " " + secs.get("OUTPUT SETTINGS", "")
    tags["camera"] = pick(CAMERA_PATTERNS, cam_text, p["prompt"]) or "Unspecified"
    headers = " ".join(h for h, _ in p["sections"])
    has_dialogue = "DIALOGUE" in headers or "THE LINE" in headers or "THE WORD" in headers \
        or first_unnegated(r"\b(says|speaks|whispers|asks|replies|answers)\b", p["prompt"]) is not None
    wordless = re.search(r"\bwordless\b|no dialogue", p["prompt"], re.I)
    tags["dialogue"] = "Dialogue" if has_dialogue and not (wordless and "DIALOGUE" not in headers) else "Wordless"
    multi = p["shots"] or first_unnegated(r"hard cut|\bshot 1\b|two shots|three shots", p["prompt"]) is not None
    tags["format"] = "Multi-shot" if multi else "Single take"
    tags["music"] = "No music" if re.search(r"no music|no score", p["prompt"], re.I) else "Music allowed / unspecified"
    tags["duration"] = f"{p['duration']}s"
    tags["model"] = p["model"]
    return tags


def build_families(prompts):
    by_folder = collections.defaultdict(list)
    for p in sorted(prompts, key=lambda p: p["created"]):
        by_folder[p["folder"]].append(p)
    families = []
    for folder, ps in sorted(by_folder.items()):
        fams = []
        for p in ps:
            ctx = scene_context(p)[:1500]
            best, best_r = None, 0
            for fam in fams:
                r = max(difflib.SequenceMatcher(None, ctx, scene_context(q)[:1500]).ratio() for q in fam)
                if r > best_r:
                    best, best_r = fam, r
            if best is not None and best_r >= FAMILY_SIMILARITY:
                best.append(p)
            else:
                fams.append([p])
        for i, fam in enumerate(fams, 1):
            families.append({"folder": folder, "num": i, "versions": fam, "final": fam[-1]})
    return families


def scene_label(folder):
    return folder.split(os.sep)[-1] if folder != "_root" else "Unfiled (project root)"


def scene_sort_key(folder):
    return (folder == "_root", folder)


def fence(text):
    return f"````text\n{text.strip()}\n````"


def write(path, lines):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("\n".join(lines).rstrip() + "\n")


def main():
    prompts = [parse_raw(f) for f in glob.glob(os.path.join(RAW, "**", "*.md"), recursive=True)]
    for p in prompts:
        p["sections"] = split_sections(p["prompt"])
        p["tags"] = tags_of(p)
    families = build_families(prompts)

    for d in ("shots", "sections"):
        shutil.rmtree(os.path.join(OUT, d), ignore_errors=True)

    # ---------- shots/ ----------
    for fam in families:
        f = fam["final"]
        fam["title"] = title_of(f)
        fam["id"] = f"{slug(scene_label(fam['folder']), 20)}-{fam['num']:02d}"
        fam["path"] = os.path.join(OUT, "shots", slug(scene_label(fam["folder"]), 30),
                                   f"{fam['num']:02d}_{slug(fam['title'], 50)}.md")
        fam["chars"] = sorted({r["name"] for r in f["refs"].values() if r["category"] == "character"})
        fam["places"] = sorted({r["name"] for r in f["refs"].values() if r["category"] == "environment"})
        fam["props"] = sorted({r["name"] for r in f["refs"].values() if r["category"] == "prop"})
        fam["takes"] = sum(v["takes"] for v in fam["versions"])

    for fam in families:
        f, d = fam["final"], os.path.dirname(fam["path"])
        t = f["tags"]
        lines = [
            f"# {fam['id']} · {fam['title']}",
            "",
            f"[← Index]({rel(os.path.join(OUT, 'INDEX.md'), d)}) · Scene: **{scene_label(fam['folder'])}**",
            "",
            "| | |", "|---|---|",
            f"| Shot size | {t['size']} |",
            f"| Camera | {t['camera']} |",
            f"| Format | {t['format']} · {t['duration']} · {f['aspect']} · {f['resolution']} |",
            f"| Sound | {t['dialogue']} · {t['music']} |",
            f"| Model | {t['model']} |",
            f"| Characters | {', '.join(fam['chars']) or '—'} |",
            f"| Location | {', '.join(fam['places']) or '—'} |",
            f"| Props | {', '.join(fam['props']) or '—'} |",
            f"| Iterations | {len(fam['versions'])} prompt version(s), {fam['takes']} generation(s) total |",
            "",
            "**Sections:** " + " → ".join(h for h, _ in f["sections"]),
            "",
            "## Final prompt (latest version)",
            "",
            f"_Element IDs replaced with names. Original with IDs: [{os.path.basename(f['path'])}]({rel(f['path'], d)})_",
            "",
            fence(readable(f["prompt"], f["refs"])),
        ]
        for i, s in enumerate(f["shots"], 1):
            lines += ["", f"### Multi-shot prompt {i}", "", fence(readable(s, f["refs"]))]
        lines += ["", "### Generated videos", ""]
        lines += [f"- {g[0]} · [video]({g[2]})" for g in f["gens"]]
        if len(fam["versions"]) > 1:
            lines += ["", "## Earlier versions", "",
                      "Oldest first. Compare against the final to see what the author changed between attempts.", ""]
            for i, v in enumerate(fam["versions"][:-1], 1):
                lines += [f"<details><summary>v{i} · {v['created']} · {v['takes']} generation(s) · "
                          f"{os.path.basename(v['path'])}</summary>", "", fence(readable(v["prompt"], v["refs"])), "",
                          *[f"- [video]({g[2]})" for g in v["gens"]], "", "</details>", ""]
        write(fam["path"], lines)

    # ---------- INDEX.md ----------
    by_scene = collections.defaultdict(list)
    for fam in families:
        by_scene[fam["folder"]].append(fam)
    lines = ["# Shot index", "",
             f"{len(families)} shots ({len(prompts)} prompt versions) from the CONTROL project, grouped by scene. "
             "Each link opens the final prompt plus earlier iterations. See also [TAGS.md](TAGS.md) to browse by "
             "shot type, and [README.md](README.md) for how the library is organised.", ""]
    for folder in sorted(by_scene, key=scene_sort_key):
        lines.append(f"- [{scene_label(folder)}](#{slug(scene_label(folder), 80)}) — {len(by_scene[folder])} shots")
    for folder in sorted(by_scene, key=scene_sort_key):
        lines += ["", f"## {scene_label(folder)}", "",
                  "| # | Shot | Size | Camera | Dur | Sound | Characters | Ver. |",
                  "|---|---|---|---|---|---|---|---|"]
        for fam in by_scene[folder]:
            t = fam["final"]["tags"]
            title = fam["title"].replace("|", "/")
            lines.append(f"| {fam['num']:02d} | [{title}]({rel(fam['path'], OUT)}) | {t['size']} | {t['camera']} | "
                         f"{t['duration']} | {t['dialogue']} | {', '.join(fam['chars']) or '—'} | {len(fam['versions'])} |")
    write(os.path.join(OUT, "INDEX.md"), lines)

    # ---------- TAGS.md ----------
    groups = [("Shot size", "size"), ("Camera", "camera"), ("Dialogue", "dialogue"), ("Format", "format"),
              ("Duration", "duration"), ("Model", "model")]
    lines = ["# Browse by tag", "", "Tags are inferred automatically from each final prompt's text "
             "(SCENE CONTEXT / FRAMING / CAMERA sections), so treat them as a good first filter, not ground truth.", ""]
    for label, key in groups:
        lines.append(f"- [{label}](#{slug(label)})")
    for label, key in groups:
        lines += ["", f"## {label}"]
        vals = collections.defaultdict(list)
        for fam in families:
            vals[fam["final"]["tags"][key]].append(fam)
        order = sorted(vals, key=lambda v: (-len(vals[v]), v)) if key != "duration" else \
            sorted(vals, key=lambda v: float(v[:-1]) if v[:-1].replace(".", "").isdigit() else 999)
        for v in order:
            lines += ["", f"### {v} ({len(vals[v])})", ""]
            lines += [f"- [{fam['id']}]({rel(fam['path'], OUT)}) {fam['title']}" for fam in vals[v]]
    lines += ["", "## Character", ""]
    chars = collections.defaultdict(list)
    for fam in families:
        for c in fam["chars"]:
            chars[c].append(fam)
    for c in sorted(chars):
        lines += [f"### {c} ({len(chars[c])})", ""]
        lines += [f"- [{fam['id']}]({rel(fam['path'], OUT)}) {fam['title']}" for fam in chars[c]] + [""]
    write(os.path.join(OUT, "TAGS.md"), lines)

    # ---------- sections/ ----------
    sec_variants = collections.defaultdict(dict)  # canonical -> body -> [(header, fam)]
    for fam in families:
        f = fam["final"]
        for h, body in f["sections"]:
            if h == "(PREAMBLE)" or not body:
                continue
            body = readable(body, f["refs"])
            sec_variants[canonical(h)].setdefault(body, []).append((h, fam))
    sec_index = []
    for i, (name, _) in enumerate(SECTION_ORDER, 1):
        variants = sec_variants.get(name, {})
        if not variants:
            continue
        fname = f"{i:02d}_{slug(name)}.md"
        sec_index.append((name, fname, len(variants), sum(len(u) for u in variants.values())))
        lines = [f"# {name}", "", f"[← Template](../TEMPLATE.md) · [All sections](README.md)", "",
                 f"{len(variants)} distinct variants across {sum(len(u) for u in variants.values())} final shot prompts. "
                 "Most-reused first, then by scene. Each variant links to the shot it came from.", ""]
        ordered = sorted(variants.items(), key=lambda kv: (-len(kv[1]), scene_sort_key(kv[1][0][1]["folder"]),
                                                            kv[1][0][1]["num"]))
        for body, uses in ordered:
            fam0 = uses[0][1]
            t = fam0["final"]["tags"]
            hdrs = sorted({h for h, _ in uses})
            src = ", ".join(f"[{fam['id']}]({rel(fam['path'], os.path.join(OUT, 'sections'))})" for _, fam in uses[:8])
            if len(uses) > 8:
                src += f" +{len(uses) - 8} more"
            lines += [f"## {fam0['id']} · {fam0['title'][:90]}", "",
                      f"`{' / '.join(hdrs)}` · {t['size']} · {t['camera']} · {t['duration']}"
                      + (f" · **reused verbatim in {len(uses)} shots**" if len(uses) > 1 else ""), "",
                      f"Used in: {src}", "", fence(body), ""]
        write(os.path.join(OUT, "sections", fname), lines)
    lines = ["# Section library", "", "Every distinct body of each prompt section, taken from the **final** version "
             "of every shot. Use these when writing one section of your own prompt and you want to see how it was "
             "phrased for a similar shot.", "", "| Section | Variants | Shots using it |", "|---|---|---|"]
    lines += [f"| [{n}]({fn}) | {v} | {u} |" for n, fn, v, u in sec_index]
    write(os.path.join(OUT, "sections", "README.md"), lines)

    # ---------- REUSABLE_BLOCKS.md ----------
    blocks = []
    for name, variants in sec_variants.items():
        for body, uses in variants.items():
            fams = {id(fam) for _, fam in uses}
            if len(fams) >= 3 and len(body) > 80:
                blocks.append((len(fams), name, body, uses))
    blocks.sort(key=lambda b: (-b[0], b[1]))
    lines = ["# Reusable blocks", "", "Section bodies the author pasted **verbatim** into 3 or more different shots. "
             "These are the house boilerplate: safe to copy as-is into your own prompts and adjust only the "
             "element names.", ""]
    for n, name, body, uses in blocks:
        hdrs = sorted({h for h, _ in uses})
        lines += [f"## {' / '.join(hdrs)} — used in {n} shots", "",
                  "Used in: " + ", ".join(f"[{fam['id']}]({rel(fam['path'], OUT)})" for _, fam in uses[:10])
                  + (" …" if len(uses) > 10 else ""), "", fence(body), ""]
    write(os.path.join(OUT, "REUSABLE_BLOCKS.md"), lines)

    # ---------- ELEMENTS.md ----------
    elements = {}
    for fam in families:
        f = fam["final"]
        refs_body = next((b for h, b in f["sections"] if canonical(h) == "ACTIVE REFERENCES"), "")
        for uid, r in f["refs"].items():
            e = elements.setdefault(r["name"], {"category": r["category"], "ids": set(), "imgs": [], "descs": {}})
            e["ids"].add(uid)
            if r["img"] and r["img"] not in e["imgs"]:
                e["imgs"].append(r["img"])
            m = re.search(rf"<<<{uid}>>>:\s*(.+?)(?=\n\s*\n|\n<<<|\Z)", refs_body, re.S)
            if m:
                e["descs"].setdefault(readable(m.group(1).strip(), f["refs"]), []).append(fam)
    lines = ["# Elements", "", "Every character, location and prop element referenced in the prompts, with its "
             "reference image and the distinct ways the ACTIVE REFERENCES section described it (latest shot first). "
             "In the prompts an element is written `<<<name>>>` (originally `<<<element-uuid>>>`).", ""]
    cats = [("character", "Characters"), ("environment", "Locations"), ("prop", "Props")]
    for cat, label in cats:
        names = sorted(n for n, e in elements.items() if e["category"] == cat)
        lines.append(f"- **{label}:** " + ", ".join(f"[{n}](#{slug(n, 80)})" for n in names))
    for cat, label in cats:
        lines += ["", f"## {label}"]
        for n in sorted(x for x, e in elements.items() if e["category"] == cat):
            e = elements[n]
            lines += ["", f"### {n}", "", f"IDs: {', '.join(f'`{i}`' for i in sorted(e['ids']))}"]
            if e["imgs"]:
                lines += ["", " ".join(f"[![{n}]({u})]({u})" for u in e["imgs"][:3])]
            descs = sorted(e["descs"].items(), key=lambda kv: max(f["final"]["created"] for f in kv[1]), reverse=True)
            if descs:
                lines += ["", f"{len(descs)} distinct description(s):", ""]
                for desc, fams in descs[:6]:
                    lines.append(f"- {desc.replace(chr(10), ' ')}  \n  ↳ " +
                                 ", ".join(f"[{fam['id']}]({rel(fam['path'], OUT)})" for fam in fams[:6]))
                if len(descs) > 6:
                    lines.append(f"- … {len(descs) - 6} more in the shot files")
    write(os.path.join(OUT, "ELEMENTS.md"), lines)

    # ---------- README.md ----------
    lines = [
        "# CONTROL prompt library", "",
        f"Reference library built from the {len(prompts)} distinct video prompts ({sum(p['takes'] for p in prompts)} "
        f"generations) of the Higgsfield project *CONTROL* by @pietromalegori. Near-identical prompts in the same "
        f"scene were grouped into **{len(families)} shots**, each with its final (latest) prompt and its earlier "
        "iterations.", "",
        "## Where to start", "",
        "| If you want to… | Open |", "|---|---|",
        "| Write a new prompt from scratch | [TEMPLATE.md](TEMPLATE.md) — the skeleton every prompt follows |",
        "| Find a shot similar to the one you're planning | [TAGS.md](TAGS.md) (by size, camera, dialogue, duration…) |",
        "| Browse the film scene by scene | [INDEX.md](INDEX.md) |",
        "| See how one section (CAMERA, LIGHTING, AUDIO…) was written across shots | [sections/](sections/README.md) |",
        "| Copy the boilerplate locks (no music, no glowing lenses, real-time only…) | [REUSABLE_BLOCKS.md](REUSABLE_BLOCKS.md) |",
        "| See how characters / locations / props are described | [ELEMENTS.md](ELEMENTS.md) |",
        "| Learn how the author iterated a shot | any shot file → *Earlier versions* |", "",
        "## Layout", "",
        "```", "library/",
        "  README.md            this file",
        "  TEMPLATE.md          annotated prompt skeleton (hand-written)",
        "  INDEX.md             all shots by scene",
        "  TAGS.md              all shots by shot size / camera / dialogue / format / duration / model / character",
        "  ELEMENTS.md          characters, locations, props",
        "  REUSABLE_BLOCKS.md   blocks reused verbatim in 3+ shots",
        "  sections/            every variant of each section, from final prompts",
        "  shots/<scene>/NN_<title>.md   final prompt + metadata + earlier versions",
        "prompts/               raw crawl (one file per prompt, original element UUIDs)",
        "```", "",
        "## Notes", "",
        "- In library files, `<<<element-uuid>>>` references are replaced with readable names like "
        "`<<<char_captain>>>`. On Higgsfield you attach the element and the app inserts its ID.",
        "- \"Final\" means the most recent prompt in a group of similar prompts. It is usually the most refined, "
        "but not necessarily the take used in the film.",
        "- Tags and shot groups are generated by heuristics, so occasionally a shot is mis-tagged or split in two.",
        "",
        "## Regenerating", "",
        "```bash", "python3 crawl_prompts.py   # re-download raw prompts into prompts/",
        "python3 build_library.py  # rebuild library/ (TEMPLATE.md is kept)", "```",
    ]
    write(os.path.join(OUT, "README.md"), lines)

    print(f"{len(prompts)} prompts → {len(families)} shots; {len(blocks)} reusable blocks; "
          f"{len(elements)} elements; sections: {', '.join(f'{n}={v}' for n, _, v, _ in sec_index)}")


if __name__ == "__main__":
    main()
