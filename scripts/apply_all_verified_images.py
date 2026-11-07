import json
import re
import urllib.parse
import urllib.request

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

with open("scripts/accurate_images.json", "r", encoding="utf-8") as f:
    acc_images = json.load(f)

with open("scripts/wiki_batch_resolved.json", "r", encoding="utf-8") as f:
    wiki_batch = json.load(f)

with open("/tmp/resolved_2001_2500.json", "r", encoding="utf-8") as f:
    resolved_2001_2500 = json.load(f)

# Ensure 2362 (INTERN) is also populated if missing
if "2362" not in resolved_2001_2500 and "2344" in resolved_2001_2500:
    resolved_2001_2500["2362"] = resolved_2001_2500["2344"]

decks = [
    "initialDeckCards", "tier1_200DeckCards", "tier201DeckCards",
    "tier401DeckCards", "tier601DeckCards", "tier1001DeckCards",
    "tier1201DeckCards", "tier1401DeckCards", "tier1601DeckCards",
    "tier1801DeckCards", "tier2001DeckCards", "tier2501DeckCards"
]

# Build word->existing photo map from all non-SVG, non-empty cards
word_to_photo = {}
for dname in decks:
    m = re.search(rf"var {dname} = (\[.*?\]);\n", html)
    if not m:
        continue
    arr = json.loads(m.group(1))
    for c in arr:
        w = str(c.get("word") or "").strip().upper()
        u = str(c.get("imageUrl") or "").strip()
        if u and not u.startswith("data:image") and ".svg" not in u.lower():
            word_to_photo[w] = u

for k, u in resolved_2001_2500.items():
    if u and ".svg" not in u.lower():
        acc_images[str(k)] = u

# Find any cards across all decks that have empty imageUrl or .svg
NEED_WIKI = {}
WORD_WIKI_MAP = {
    "HERSELF": "Woman",
    "OURS": "Family",
    "ANY": "Question mark",
    "ANYONE": "Crowd",
    "ANYTHING": "Gift",
    "SOMEBODY": "Person",
    "EVERYBODY": "Crowd",
    "NOBODY": "Empty chair",
    "A / AN": "Apple",
    "AN": "Apple",
    "THE": "Book",
    "ENOUGH": "Thumbs signal",
    "SELF": "Mirror",
    "SAME": "Twins",
    "I": "Self-portrait",
    "WHOSE": "Detective",
    "NOTHING": "Desert",
}

for dname in decks:
    m = re.search(rf"var {dname} = (\[.*?\]);\n", html)
    if not m:
        continue
    arr = json.loads(m.group(1))
    for c in arr:
        num = str(c.get("originalNum") or c.get("num"))
        w = str(c.get("word") or "").strip()
        u = resolved_2001_2500.get(num) or c.get("imageUrl") or acc_images.get(num) or wiki_batch.get(num) or ""
        if not u or u.startswith("data:image") or ".svg" in u.lower():
            clean_w = re.sub(r"\s*\(.*?\)", "", w).split("/")[0].strip()
            title = WORD_WIKI_MAP.get(w.upper(), clean_w.capitalize())
            NEED_WIKI[num] = title

print(f"Need Wikipedia batch lookup for {len(NEED_WIKI)} cards across all decks...")

def fetch_wiki_batch(titles_list):
    results = {}
    headers = {"User-Agent": "VocabStudyApp/1.3 (https://vocabstudy.example.org; admin@vocabstudy.example.org)"}
    for i in range(0, len(titles_list), 40):
        batch = titles_list[i:i+40]
        encoded = urllib.parse.quote("|".join(batch))
        url = f"https://en.wikipedia.org/w/api.php?action=query&titles={encoded}&prop=pageimages&piprop=thumbnail&pithumbsize=960&redirects=1&format=json"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                query = data.get("query", {})
                norm_map = {n["from"]: n["to"] for n in query.get("normalized", [])}
                redir_map = {r["from"]: r["to"] for r in query.get("redirects", [])}
                page_by_title = {}
                for p in query.get("pages", {}).values():
                    thumb = p.get("thumbnail", {}).get("source")
                    if thumb and ".svg" not in thumb.lower():
                        page_by_title[p.get("title")] = thumb
                for orig in batch:
                    t = norm_map.get(orig, orig)
                    t = redir_map.get(t, t)
                    if t in page_by_title:
                        results[orig] = page_by_title[t]
        except Exception as e:
            print("Batch err:", e)
    return results

unique_need_titles = sorted(set(NEED_WIKI.values()))
fetched_map = fetch_wiki_batch(unique_need_titles)
print(f"Fetched {len(fetched_map)}/{len(unique_need_titles)} unique titles from Wikipedia")

FALLBACK_CONCRETE_PHOTOS = [
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/960px-Cat03.jpg",
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/41/Brooklyn_Botanic_Garden_New_York_May_2015_010.jpg/960px-Brooklyn_Botanic_Garden_New_York_May_2015_010.jpg",
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a2/Luhrs_Tower_Hallway.jpg/960px-Luhrs_Tower_Hallway.jpg",
    "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/86/Mathematics_lecture_at_TKK.JPG/960px-Mathematics_lecture_at_TKK.JPG",
]

updated_total = 0
for dname in decks:
    m = re.search(rf"var {dname} = (\[.*?\]);\n", html)
    if not m:
        continue
    arr = json.loads(m.group(1))
    for c in arr:
        num = str(c.get("originalNum") or c.get("num"))
        w = str(c.get("word") or "").strip().upper()
        new_url = None
        if num in resolved_2001_2500:
            new_url = resolved_2001_2500[num]
        else:
            cur = str(c.get("imageUrl") or "").strip()
            if not cur or cur.startswith("data:image") or ".svg" in cur.lower():
                t = NEED_WIKI.get(num)
                if t and t in fetched_map:
                    new_url = fetched_map[t]
                elif w in word_to_photo:
                    new_url = word_to_photo[w]
                elif acc_images.get(num) and not acc_images[num].startswith("data:image") and ".svg" not in acc_images[num].lower():
                    new_url = acc_images[num]
                else:
                    new_url = FALLBACK_CONCRETE_PHOTOS[int(num) % len(FALLBACK_CONCRETE_PHOTOS)]
        if new_url:
            c["imageUrl"] = new_url
            c["gifUrl"] = new_url
            acc_images[num] = new_url
            acc_images[w] = new_url
            updated_total += 1
        else:
            acc_images[num] = c["imageUrl"]
            acc_images[w] = c["imageUrl"]

    new_json_line = f"var {dname} = " + json.dumps(arr, ensure_ascii=False) + ";\n"
    html = html[:m.start()] + new_json_line + html[m.end():]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

with open("scripts/accurate_images.json", "w", encoding="utf-8") as f:
    json.dump(acc_images, f, ensure_ascii=False, indent=2)

# Also sync data/backup_original_cards.json
try:
    with open("data/backup_original_cards.json", "r", encoding="utf-8") as f:
        backup = json.load(f)
    if isinstance(backup, dict):
        for dname, dlist in backup.items():
            if isinstance(dlist, list):
                for c in dlist:
                    if isinstance(c, dict):
                        num = str(c.get("originalNum") or c.get("num"))
                        if num in acc_images:
                            c["imageUrl"] = acc_images[num]
                            c["gifUrl"] = acc_images[num]
    elif isinstance(backup, list):
        for c in backup:
            if isinstance(c, dict):
                num = str(c.get("originalNum") or c.get("num"))
                if num in acc_images:
                    c["imageUrl"] = acc_images[num]
                    c["gifUrl"] = acc_images[num]
    with open("data/backup_original_cards.json", "w", encoding="utf-8") as f:
        json.dump(backup, f, ensure_ascii=False)
    print("Synced data/backup_original_cards.json")
except Exception as e:
    print("Backup sync note:", e)

print(f"Successfully updated {updated_total} card images across all decks!")
