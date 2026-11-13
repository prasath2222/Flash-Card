import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from visual_concepts_data import KEEP_VERIFIED_EXISTING, VISUAL_QUERIES

HEADERS = {
    "User-Agent": "EducationalFlashcardsBot/2.1 (https://github.com/flashcards-app; dev@flashcards.local)"
}

CACHE_PATH = "scripts/image_resolve_cache.json"
INDEX_PATH = "index.html"
ACCURATE_PATH = "scripts/accurate_images.json"
WIKI_THUMBS_PATH = "scripts/wiki_thumbs.json"
BACKUP_PATH = "data/backup_original_cards.json"

DECK_NAMES = [
    "split1DeckCards",
    "split2DeckCards",
    "split5DeckCards",
    "split6DeckCards",
    "split7DeckCards",
    "split8DeckCards",
]

# Reject non-photo artifacts, logos, diagrams, maps, charts, historical engravings, watermarks
BAD_FILE_RE = re.compile(
    r"(logo|icon|diagram|chart|graph|map|flag|coat_of_arms|emblem|crest|seal|signature|"
    r"formula|symbol|gray\d|blausen|plaque|poster|obituary|thumbnail\.jpg|istock|"
    r"watermark|screenshot|qr_code|barcode|locator|distribution|chromosome|spectrum|"
    r"timeline|floorplan|blueprint|schematic|vector|clipart|cartoon|comic|stamp|"
    r"herald|monogram|glyph|typograph|nullgraph|wellcome|k%c3%b6hler|kohler|"
    r"bundesarchiv|lccn20|title_page|frontispiece|manuscript|cat03|luhrs_tower|"
    r"mathematics_lecture|brooklyn_botanic|commons-logo|ambox|question_book|nuvola|gnome-)",
    re.I,
)

ART_ALLOW_NUMS = {1338, 1339, 1340, 1341}

STOPWORDS = {
    "in", "on", "at", "to", "by", "for", "of", "the", "a", "an", "and", "or",
    "with", "from", "into", "over", "under", "out", "up", "down", "vs", "v",
}


def canonical_url(u: str) -> str:
    if not u:
        return ""
    u = u.strip()
    u = u.replace("https://thumb.wikimedia.org", "https://upload.wikimedia.org")
    # Remove noisy wiki tracking query params on commons URLs
    if "wikimedia.org" in u and "?" in u:
        u = u.split("?")[0]
    return u


def base_filename(u: str) -> str:
    clean = u.split("?")[0].rstrip("/").split("/")[-1]
    clean = urllib.parse.unquote(clean).lower()
    clean = re.sub(r"^\d+px-", "", clean)
    return clean


def is_clean_photo_url(url: str, width: int = 960, height: int = 640, card_num: int = 0) -> bool:
    if not url or "unsplash.com" in url or url.startswith("data:"):
        return False
    if "upload.wikimedia.org" not in url:
        return False
    u_no_q = url.split("?")[0]
    if not re.search(r"\.jpe?g$", u_no_q, re.I):
        return False
    if re.search(r"\.(ogv|pdf|tif|tiff|webm|xcf|djvu)\.jpg$", u_no_q, re.I):
        return False
    fn = base_filename(url)
    if BAD_FILE_RE.search(url) or BAD_FILE_RE.search(fn):
        if card_num not in ART_ALLOW_NUMS:
            return False
    if width and height:
        if width < 480 or height < 300:
            return False
        ratio = width / max(1, height)
        if ratio < 0.45 or ratio > 2.85:
            return False
    return True


def fetch_json(url: str, retries: int = 4):
    wait = 2.0
    for attempt in range(retries):
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                ra = e.headers.get("Retry-After")
                sleep_s = float(ra) + 0.5 if ra and ra.isdigit() else wait
                print(f"  [HTTP {e.code}] backing off {sleep_s:.1f}s...", flush=True)
                time.sleep(sleep_s)
                wait *= 2
                continue
            return {}
        except Exception:
            if attempt < retries - 1:
                time.sleep(wait)
                wait *= 1.5
                continue
            return {}
    return {}


def fetch_wiki_batch(titles: list[str]) -> dict[str, str]:
    results = {}
    unique_titles = sorted(set(titles))
    for i in range(0, len(unique_titles), 35):
        batch = unique_titles[i : i + 35]
        params = urllib.parse.urlencode(
            {
                "action": "query",
                "titles": "|".join(batch),
                "redirects": "1",
                "prop": "pageimages",
                "piprop": "thumbnail",
                "pithumbsize": "960",
                "format": "json",
            }
        )
        data = fetch_json("https://en.wikipedia.org/w/api.php?" + params)
        query = data.get("query", {})
        norm = {n["from"]: n["to"] for n in query.get("normalized", [])}
        redir = {r["from"]: r["to"] for r in query.get("redirects", [])}
        by_title = {}
        for p in query.get("pages", {}).values():
            th = p.get("thumbnail", {})
            src = canonical_url(th.get("source", ""))
            w = th.get("width", 0)
            h = th.get("height", 0)
            if is_clean_photo_url(src, w, h):
                by_title[p.get("title")] = src
        for orig in batch:
            t = norm.get(orig, orig)
            t = redir.get(t, t)
            if t in by_title:
                results[orig] = by_title[t]
        time.sleep(0.25)
    return results


def commons_search_candidates(query_str: str, require_kw_in_title: bool = True) -> list[str]:
    clean_q = query_str.replace("intitle:", "").strip()
    kws = [
        k.lower()
        for k in re.findall(r"[a-zA-Z]{3,}", clean_q)
        if k.lower() not in STOPWORDS
    ]
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "generator": "search",
            "gsrsearch": f"filetype:bitmap {query_str}",
            "gsrnamespace": "6",
            "gsrlimit": "12",
            "prop": "imageinfo",
            "iiprop": "url|mime|size",
            "iiurlwidth": "960",
            "format": "json",
        }
    )
    data = fetch_json("https://commons.wikimedia.org/w/api.php?" + params)
    pages = list(data.get("query", {}).get("pages", {}).values())
    pages.sort(key=lambda p: p.get("index", 999))

    scored = []
    for idx, p in enumerate(pages):
        ii = (p.get("imageinfo") or [{}])[0]
        if ii.get("mime") != "image/jpeg":
            continue
        w = ii.get("width", 0)
        h = ii.get("height", 0)
        url = canonical_url(ii.get("thumburl") or ii.get("url") or "")
        if not is_clean_photo_url(url, w, h):
            continue
        title_l = p.get("title", "").lower()
        kw_hits = sum(1 for kw in kws if kw in title_l or (len(kw) > 4 and kw[:-1] in title_l))
        if require_kw_in_title and kws and kw_hits == 0:
            continue
        # Rank higher when multiple keywords appear in filename and higher in Commons rank
        score = kw_hits * 10 - idx
        scored.append((score, url))

    scored.sort(key=lambda x: -x[0])
    return [u for _, u in scored]


def build_search_tiers(q: str) -> list[tuple[str, bool]]:
    clean = q.replace("intitle:", "").strip()
    kws = [k for k in re.findall(r"[a-zA-Z]{3,}", clean) if k.lower() not in STOPWORDS]
    tiers = []
    if len(kws) >= 2:
        # Primary: require first keyword in File title + second keyword for rich relevance in 1 call
        tiers.append((f"intitle:{kws[0]} {kws[1]}", True))
        # Secondary: full phrase requiring >=1 keyword in filename
        tiers.append((clean, True))
        tiers.append((f"intitle:{kws[-1]}", False))
    elif len(kws) == 1:
        tiers.append((f"intitle:{kws[0]}", True))
        tiers.append((clean, False))
    else:
        tiers.append((clean, False))
    return tiers


def resolve_for_queries(queries: list[str], cache: dict) -> list[str]:
    cache_key = "||".join(queries)
    if cache_key in cache and cache[cache_key]:
        return cache[cache_key]

    candidates = []
    seen = set()

    for raw_q in queries:
        for search_expr, req_kw in build_search_tiers(raw_q):
            hits = commons_search_candidates(search_expr, require_kw_in_title=req_kw)
            for u in hits:
                fn = base_filename(u)
                if fn not in seen:
                    seen.add(fn)
                    candidates.append(u)
            if len(candidates) >= 3:
                break
        if len(candidates) >= 3:
            break

    # If still empty, try un-gated top query
    if not candidates and queries:
        clean = queries[0].replace("intitle:", "").strip()
        hits = commons_search_candidates(clean, require_kw_in_title=False)
        for u in hits:
            fn = base_filename(u)
            if fn not in seen:
                seen.add(fn)
                candidates.append(u)

    if candidates:
        cache[cache_key] = candidates
    return candidates


def verify_http_url(url: str) -> bool:
    for attempt in range(3):
        for method in ("HEAD", "GET"):
            req = urllib.request.Request(url, headers=HEADERS, method=method)
            if method == "GET":
                req.add_header("Range", "bytes=0-63")
            try:
                with urllib.request.urlopen(req, timeout=8) as resp:
                    if resp.status in (200, 206):
                        ct = (resp.headers.get("Content-Type") or "").lower()
                        if "image" in ct or not ct:
                            return True
            except urllib.error.HTTPError as e:
                if e.code == 405 and method == "HEAD":
                    continue
                if e.code == 429 or e.code >= 500:
                    time.sleep(1.5 * (attempt + 1))
                    break
                return False
            except Exception:
                time.sleep(0.5)
                break
        else:
            return False
    return False


def main():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    cache = {}
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except Exception:
            cache = {}

    # Extract all decks
    decks = {}
    all_cards = []
    for dname in DECK_NAMES:
        m = re.search(rf"((?:var|let|const)\s+{dname}\s*=\s*)(\[.*?\])(;)", html)
        if not m:
            raise RuntimeError(f"Could not find deck {dname} in {INDEX_PATH}")
        arr = json.loads(m.group(2))
        decks[dname] = {"prefix": m.group(1), "suffix": m.group(3), "cards": arr}
        all_cards.extend(arr)

    print(f"Loaded {len(all_cards)} cards across {len(decks)} decks.", flush=True)

    # Step 1: Resolve Wikipedia batch titles for concrete VISUAL_QUERIES entries
    wiki_titles_needed = [
        spec[0] for num, spec in VISUAL_QUERIES.items() if spec[0]
    ]
    print(f"Batch-fetching {len(wiki_titles_needed)} Wikipedia PageImages...", flush=True)
    wiki_map = fetch_wiki_batch(wiki_titles_needed)
    print(f"Wikipedia returned {len(wiki_map)} clean JPGs.", flush=True)

    # Step 2: Assign KEPT existing verified photos first (enforcing strict uniqueness)
    used_urls = set()
    used_files = set()
    final_urls = {}  # num -> url
    candidates_by_num = {}  # num -> list[str]

    def claim_url(num: int, url: str) -> bool:
        cu = canonical_url(url)
        fn = base_filename(cu)
        if cu in used_urls or fn in used_files:
            return False
        used_urls.add(cu)
        used_files.add(fn)
        final_urls[num] = cu
        return True

    kept_count = 0
    for c in all_cards:
        num = c["num"]
        if num in KEEP_VERIFIED_EXISTING:
            cu = canonical_url(c.get("imageUrl", ""))
            if is_clean_photo_url(cu, card_num=num) and claim_url(num, cu):
                candidates_by_num[num] = [cu]
                kept_count += 1

    print(f"Kept {kept_count} clean unique existing photos.", flush=True)

    # Step 3: Pre-fetch uncached Commons queries with gentle 4-worker concurrency
    to_resolve = [c for c in all_cards if c["num"] not in final_urls]
    uncached_specs = []
    for c in to_resolve:
        num = c["num"]
        word = c.get("word", "")
        spec = VISUAL_QUERIES.get(num)
        if spec:
            wiki_t, queries = spec
        else:
            clean_w = re.sub(r"\s*\(.*?\)", "", word).split("/")[0].strip().lower()
            wiki_t, queries = None, [f"intitle:{clean_w}", clean_w]
        # Only skip Commons fetch if wiki_t already succeeded AND query is cached
        ck = "||".join(queries)
        if ck not in cache or not cache[ck]:
            uncached_specs.append((num, queries, ck))

    print(f"Fetching {len(uncached_specs)} uncached Commons searches (cached={len(to_resolve)-len(uncached_specs)})...", flush=True)

    if uncached_specs:
        def worker(item):
            _num, qs, ck = item
            local_cache = {}
            res = resolve_for_queries(qs, local_cache)
            return ck, res

        with ThreadPoolExecutor(max_workers=4) as pool:
            done_cnt = 0
            futs = [pool.submit(worker, item) for item in uncached_specs]
            for fut in as_completed(futs):
                ck, res = fut.result()
                if res:
                    cache[ck] = res
                done_cnt += 1
                if done_cnt % 50 == 0 or done_cnt == len(uncached_specs):
                    print(f"  Fetched [{done_cnt}/{len(uncached_specs)}]", flush=True)
                    with open(CACHE_PATH, "w", encoding="utf-8") as f:
                        json.dump(cache, f, indent=2)

    print(f"Assigning unique photographs for {len(to_resolve)} cards...", flush=True)
    for idx, c in enumerate(to_resolve, 1):
        num = c["num"]
        word = c.get("word", "")
        spec = VISUAL_QUERIES.get(num)
        if spec:
            wiki_t, queries = spec
        else:
            clean_w = re.sub(r"\s*\(.*?\)", "", word).split("/")[0].strip().lower()
            wiki_t, queries = None, [f"intitle:{clean_w}", clean_w]

        cands = []
        if wiki_t and wiki_t in wiki_map:
            cands.append(wiki_map[wiki_t])

        commons_cands = cache.get("||".join(queries), [])
        for u in commons_cands:
            if u not in cands:
                cands.append(u)

        chosen = False
        for u in cands:
            if claim_url(num, u):
                chosen = True
                break

        if not chosen:
            clean_alt = re.sub(r"\s*\(.*?\)", "", word).replace("/", " ").strip().lower()
            extra = resolve_for_queries([f"{clean_alt} photograph", queries[-1] + " photo"], cache)
            for u in extra:
                if u not in cands:
                    cands.append(u)
                if claim_url(num, u):
                    chosen = True
                    break

        candidates_by_num[num] = cands
        if not chosen:
            print(f"  WARN: #{num} {word} -> NO_UNIQUE ({len(cands)} cands)", flush=True)

    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

    missing = [c["num"] for c in all_cards if c["num"] not in final_urls]
    print(f"Resolution pass complete. Assigned: {len(final_urls)}/{len(all_cards)}, Missing: {missing}")

    # Step 4: Batch-verify all 1,446 assigned files via MediaWiki imageinfo API (50 per call)
    print("Batch-verifying 1,446 files via Wikimedia imageinfo API...", flush=True)

    def url_to_file_title(u: str) -> str:
        clean = u.split("?")[0].rstrip("/").split("/")[-1]
        clean = urllib.parse.unquote(clean)
        clean = re.sub(r"^\d+px-", "", clean).replace(" ", "_")
        return "File:" + clean

    def batch_check_imageinfo(api_host: str, file_titles: list[str]) -> dict[str, str]:
        valid = {}
        uniq = list(dict.fromkeys(file_titles))
        for i in range(0, len(uniq), 50):
            chunk = uniq[i:i + 50]
            params = urllib.parse.urlencode({
                "action": "query",
                "titles": "|".join(chunk),
                "prop": "imageinfo",
                "iiprop": "url|mime|size",
                "iiurlwidth": "960",
                "format": "json",
            })
            data = fetch_json(f"https://{api_host}/w/api.php?{params}")
            pages = data.get("query", {}).get("pages", {})
            # Also map normalized names back
            norm_map = {n.get("to", ""): n.get("from", "") for n in data.get("query", {}).get("normalized", [])}
            for _pid, pg in pages.items():
                if "missing" in pg:
                    continue
                ii = (pg.get("imageinfo") or [{}])[0]
                mime = ii.get("mime", "")
                if "jpeg" not in mime.lower() and "jpg" not in (ii.get("url", "").lower()):
                    continue
                t = pg.get("title", "")
                best_u = canonical_url(ii.get("thumburl") or ii.get("url") or "")
                if not best_u:
                    continue
                valid[t.lower()] = best_u
                if t in norm_map:
                    valid[norm_map[t].lower()] = best_u
            time.sleep(0.12)
        return valid

    title_by_num = {num: url_to_file_title(u) for num, u in final_urls.items()}
    commons_valid = batch_check_imageinfo("commons.wikimedia.org", list(title_by_num.values()))
    missing_titles = [t for n, t in title_by_num.items() if t.lower() not in commons_valid]
    enwiki_valid = batch_check_imageinfo("en.wikipedia.org", missing_titles) if missing_titles else {}

    verified_urls = {**enwiki_valid, **commons_valid}
    failed_nums = []
    for num, t in list(title_by_num.items()):
        live_u = verified_urls.get(t.lower())
        if live_u and is_clean_photo_url(live_u, card_num=num):
            final_urls[num] = live_u
        else:
            # Keep if exact URL has valid upload.wikimedia.org jpg structure and was just normalized
            if t.lower() in verified_urls:
                final_urls[num] = verified_urls[t.lower()]
            else:
                failed_nums.append(num)

    print(f"Batch imageinfo verification finished: {len(final_urls) - len(failed_nums)}/{len(final_urls)} verified, {len(failed_nums)} fallback replacements.", flush=True)
    for num in failed_nums:
        old_u = final_urls.pop(num, None)
        if old_u:
            used_urls.discard(old_u)
            used_files.discard(base_filename(old_u))
        cands = candidates_by_num.get(num, [])
        if len(cands) <= 1:
            spec = VISUAL_QUERIES.get(num)
            q_list = spec[1] if spec else [all_cards[num - 1]["word"].split("/")[0].strip().lower()]
            cands = commons_search_candidates(q_list[-1].replace("intitle:", ""), require_kw_in_title=False)
        fixed = False
        for u in cands:
            cu = canonical_url(u)
            fn = base_filename(cu)
            if cu == old_u or cu in used_urls or fn in used_files:
                continue
            ft = url_to_file_title(cu)
            chk = batch_check_imageinfo("commons.wikimedia.org", [ft])
            if ft.lower() in chk and claim_url(num, chk[ft.lower()]):
                fixed = True
                break
        if not fixed and old_u:
            claim_url(num, old_u)
            print(f"  WARN: kept existing {num} -> {old_u}", flush=True)

    # Step 5: Write updated decks back into index.html + JSON stores
    accurate_map = {}
    wiki_thumbs = {}

    for dname in DECK_NAMES:
        for c in decks[dname]["cards"]:
            num = c["num"]
            u = final_urls.get(num, canonical_url(c.get("imageUrl", "")))
            c["imageUrl"] = u
            c["gifUrl"] = u
            accurate_map[str(num)] = u
            if c.get("word"):
                accurate_map[str(c["word"]).strip().upper()] = u
            wiki_thumbs[str(num)] = u

    new_html = html
    for dname in DECK_NAMES:
        pattern = re.compile(rf"(?:var|let|const)\s+{dname}\s*=\s*\[.*?\];")
        serialized = json.dumps(decks[dname]["cards"], ensure_ascii=False)
        replacement = f"{decks[dname]['prefix']}{serialized}{decks[dname]['suffix']}"
        new_html, n_subs = pattern.subn(lambda _m: replacement, new_html, count=1)
        if n_subs != 1:
            raise RuntimeError(f"Failed replacing deck {dname} in {INDEX_PATH}")

    # Clear legacy cardPhotos Unsplash dictionary
    new_html = re.sub(r"var cardPhotos\s*=\s*\{.*?\};", "var cardPhotos = {};", new_html, count=1, flags=re.S)

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(new_html)

    with open(ACCURATE_PATH, "w", encoding="utf-8") as f:
        json.dump(accurate_map, f, indent=2, ensure_ascii=False)

    with open(WIKI_THUMBS_PATH, "w", encoding="utf-8") as f:
        json.dump(wiki_thumbs, f, indent=2, ensure_ascii=False)

    if os.path.exists(BACKUP_PATH):
        with open(BACKUP_PATH, "r", encoding="utf-8") as f:
            backup = json.load(f)
        if isinstance(backup, list):
            for c in backup:
                n = c.get("num")
                if n in final_urls:
                    c["imageUrl"] = final_urls[n]
                    c["gifUrl"] = final_urls[n]
        elif isinstance(backup, dict):
            for k, arr in backup.items():
                if isinstance(arr, list):
                    for c in arr:
                        if isinstance(c, dict) and c.get("num") in final_urls:
                            c["imageUrl"] = final_urls[c["num"]]
                            c["gifUrl"] = final_urls[c["num"]]
                elif isinstance(arr, dict) and arr.get("num") in final_urls:
                    arr["imageUrl"] = final_urls[arr["num"]]
                    arr["gifUrl"] = final_urls[arr["num"]]
        with open(BACKUP_PATH, "w", encoding="utf-8") as f:
            json.dump(backup, f, indent=2, ensure_ascii=False)

    print("ALL DONE! Updated index.html, accurate_images.json, wiki_thumbs.json, backup_original_cards.json.")


if __name__ == "__main__":
    main()
