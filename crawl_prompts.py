"""Crawl video-generation prompts from the Higgsfield CONTROL project into .md files."""
import json
import os
import re
import time
import urllib.request
from datetime import datetime, timezone

API = "https://fnf-api-gw.higgsfield.ai/fnf"
ROOT_ID = "2a03b5dd-e706-4a8b-b653-ee946addade1"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")
UA = {"User-Agent": "Mozilla/5.0"}


def get(url):
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.load(r)
        except Exception:
            if attempt == 4:
                raise
            time.sleep(2 * (attempt + 1))


def fetch_items():
    items, seen, cursor = [], set(), None
    while True:
        url = f"{API}/folders/{ROOT_ID}/items/v2?include_subfolders=true&size=50"
        if cursor:
            url += f"&cursor={cursor}"
        d = get(url)
        added = 0
        for it in d.get("items", []):
            job = it.get("job")
            key = (job or {}).get("folder_job_id") or (job or {}).get("id") or json.dumps(it, sort_keys=True)
            if key not in seen:
                seen.add(key)
                items.append(it)
                added += 1
        if not d.get("cursor") or not d.get("items") or not added:
            return items
        cursor = d["cursor"]


folder_cache = {}


def folder_name(fid):
    if fid not in folder_cache:
        try:
            folder_cache[fid] = get(f"{API}/folders/{fid}")
        except Exception:
            folder_cache[fid] = {"name": fid, "path": f"/{fid}/"}
    return folder_cache[fid]


def folder_path(fid):
    if not fid or fid == ROOT_ID:
        return "_root"
    ids = [p for p in folder_name(fid)["path"].strip("/").split("/") if p and p != ROOT_ID]
    return os.path.join(*[safe(folder_name(i)["name"]) for i in ids])


def safe(s):
    return re.sub(r"[^\w\-. ]+", "_", s).strip() or "_"


def main():
    items = fetch_items()
    videos = [it["job"] for it in items if it.get("type") == "job"
              and ((it["job"].get("results") or {}).get("raw") or {}).get("type") == "video"]
    # The same job can be listed in the root and in a subfolder; keep the most specific one.
    by_id = {}
    for j in videos:
        prev = by_id.get(j["id"])
        if prev is None or folder_path(prev.get("folder_id")).count(os.sep) < folder_path(j.get("folder_id")).count(os.sep) \
                or folder_path(prev.get("folder_id")) == "_root":
            by_id[j["id"]] = j
    videos = list(by_id.values())
    print(f"{len(items)} items, {len(videos)} unique video jobs")

    # Group identical prompts (re-rolls) within the same folder.
    groups = {}
    for j in sorted(videos, key=lambda j: j["created_at"]):
        p = j.get("params") or {}
        shots = [s.get("prompt", "") if isinstance(s, dict) else str(s) for s in (p.get("multi_prompt") or [])]
        key = (folder_path(j.get("folder_id")), p.get("prompt", ""), tuple(shots))
        groups.setdefault(key, []).append(j)

    counters = {}
    for (fpath, prompt, shots), jobs in groups.items():
        j0 = jobs[0]
        p = j0.get("params") or {}
        n = counters[fpath] = counters.get(fpath, 0) + 1
        ts = datetime.fromtimestamp(j0["created_at"], tz=timezone.utc)
        d = os.path.join(OUT, fpath)
        os.makedirs(d, exist_ok=True)
        fname = f"{n:03d}_{ts:%Y%m%d_%H%M%S}_{j0['id'][:8]}.md"

        refs = p.get("reference_elements") or []
        lines = [
            f"# {fpath.replace(os.sep, ' / ')} — prompt {n:03d}",
            "",
            f"- **Model:** {j0.get('job_set_type')}",
            f"- **Duration:** {p.get('duration')}s · **Aspect:** {p.get('aspect_ratio')} · "
            f"**Resolution:** {p.get('resolution') or str(p.get('width')) + 'x' + str(p.get('height'))}",
            f"- **Created:** {ts:%Y-%m-%d %H:%M:%S} UTC",
            f"- **Generations with this prompt:** {len(jobs)}",
        ]
        if refs:
            lines += ["", "## Reference elements", ""]
            for r in refs:
                imgs = " ".join(m["url"] for m in r.get("medias") or [] if m.get("url"))
                lines.append(f"- `{r.get('id')}` → **{r.get('name')}** ({r.get('category')})"
                             + (f" · {imgs}" if imgs else ""))
        lines += ["", "## Prompt", "", "```text", prompt.strip(), "```"]
        if any(s.strip() for s in shots):
            lines += ["", "## Multi-shot prompts", ""]
            for i, s in enumerate(shots, 1):
                lines += [f"### Shot {i}", "", "```text", s.strip(), "```", ""]
        lines += ["", "## Generations", ""]
        for j in jobs:
            t = datetime.fromtimestamp(j["created_at"], tz=timezone.utc)
            lines.append(f"- {t:%Y-%m-%d %H:%M:%S} · `{j['id']}` · {j['results']['raw']['url']}")
        with open(os.path.join(d, fname), "w") as f:
            f.write("\n".join(lines) + "\n")

    print(f"{len(groups)} prompt files written to {OUT}")


if __name__ == "__main__":
    main()
