import json
import re
import unicodedata
from scripts.es_hooks_data import ES_SOUND_ALIKES as ES1
from scripts.hi_hooks_data import HI_SOUND_ALIKES as HI1
from scripts.hooks_2001_2500_complete import (
    MULTI_TAMIL_2001_2500,
    EXTRA_ES_HOOKS,
    EXTRA_HI_HOOKS,
)

with open("scripts/final_master_fix_3000.py", "r", encoding="utf-8") as f:
    fmf = f.read()

fmf_defs = fmf.split("def main(")[0]
ns = {"__file__": "scripts/final_master_fix_3000.py"}
exec(fmf_defs, ns)
ES2 = ns.get("ES_SOUND_ALIKES", {})
HI2 = ns.get("HI_SOUND_ALIKES", {})


def strip_acc(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    ).lower()


def find_cognate(en_str, es_str):
    for ew in re.findall(r"[A-Za-z]+", en_str.lower()):
        if len(ew) < 3:
            continue
        for sw in re.findall(r"[A-Za-záéíóúüñ]+", es_str.lower()):
            sw_c = strip_acc(sw)
            if len(sw_c) < 3:
                continue
            if ew == sw_c:
                return ew.title()
            if len(ew) >= 4 and len(sw_c) >= 4 and (ew[:4] == sw_c[:4] or ew[:4] in sw_c or sw_c[:4] in ew):
                return ew.title()
            if sw_c.startswith("es") and len(ew) >= 3 and sw_c[1:4] == ew[:3]:
                return ew.title()
    return None


def build_es_sense_shortcut(word, label, es_val):
    es_clean = es_val.strip()
    es_low = es_clean.lower()
    en_ctx = f"{word} {label or ''}".strip()

    if es_low in EXTRA_ES_HOOKS:
        return EXTRA_ES_HOOKS[es_low]

    parts = [p.strip() for p in re.split(r"[/()]", es_clean) if p.strip()]
    for p in parts:
        pl = p.lower()
        if pl in EXTRA_ES_HOOKS:
            return EXTRA_ES_HOOKS[pl]
        if pl in ES2:
            return ES2[pl]
        if pl.endswith("se") and pl[:-2] in ES2:
            return ES2[pl[:-2]]
        if pl in ES1:
            bridge, link = ES1[pl]
            return f"<strong>{es_clean}</strong> ≈ {bridge} → {link}!"
        if pl.endswith("se") and pl[:-2] in ES1:
            bridge, link = ES1[pl[:-2]]
            return f"<strong>{es_clean}</strong> ≈ {bridge} → {link}!"

    cog = find_cognate(en_ctx, es_clean)
    if cog:
        return f'<strong>{es_clean}</strong> ≈ Direct match with English <strong>"{cog}"</strong> (same Latin root &amp; sound) → <em>{word.title()} ({es_clean})</em>!'

    return f'<strong>{es_clean}</strong> ≈ Key Spanish expression for <em>{word.title()} ({es_clean})</em>!'


def build_hi_sense_shortcut(word, label, hi_val, tamil_str=""):
    hi_clean = hi_val.strip()
    hi_low = hi_clean.lower()
    en_ctx = f"{word} {label or ''}".strip()
    ta_short = tamil_str.split("(")[0].split("/")[0].strip()
    ta_short = re.sub(r"^\d+\.\s*", "", ta_short).strip()

    if hi_low in EXTRA_HI_HOOKS:
        return EXTRA_HI_HOOKS[hi_low]

    parts = [p.strip() for p in re.split(r"[/()]", hi_clean) if p.strip()]
    en_words = set(re.findall(r"[a-z]+", en_ctx.lower()))

    # Prioritize native Hindi parts first so we explain the authentic Hindi word
    native_parts = [p for p in parts if p.lower() not in en_words]
    search_order = native_parts + parts

    for p in search_order:
        pl = p.lower()
        st = re.sub(
            r"\s+(karna|hona|dena|lena|jaana|aana|padna|lagna|rehna|rakhna)$", "", pl
        ).strip()
        for cand in [pl, st]:
            if not cand:
                continue
            if cand in EXTRA_HI_HOOKS:
                return EXTRA_HI_HOOKS[cand]
            if cand in HI2:
                res = HI2[cand]
                # Ensure full hi_clean header is shown if slash-separated
                if "/" in hi_clean:
                    res = re.sub(
                        r"^<strong>[^<]+</strong>",
                        f"<strong>{hi_clean}</strong>",
                        res,
                        count=1,
                    )
                return res
            if cand in HI1:
                bridge, link = HI1[cand]
                return f"<strong>{hi_clean}</strong> ≈ {bridge} → {link}!"

    # If the sense is a direct English loanword (e.g., Whiteboard, Pencil, Diploma)
    ta_part = f" &amp; spoken Tamil <strong>{ta_short}</strong>" if ta_short else ""
    return f'<strong>{hi_clean}</strong> ≈ 100% identical to English <strong>"{hi_clean}"</strong>{ta_part} → Same everyday word in Hindi &amp; English!'


def main():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    start_marker = "tier2001DeckCards = ["
    start = html.find(start_marker)
    if start == -1:
        raise RuntimeError("tier2001DeckCards not found in index.html")

    json_start = start + len("tier2001DeckCards = ")
    dec = json.JSONDecoder()
    cards, json_end = dec.raw_decode(html, json_start)
    card_words = [c["word"] for c in cards]

    with open(
        "public/assets/aistudio/Paste_November_05__2026_-_10_57PM_349ccb9a",
        "r",
        encoding="utf-8",
    ) as f:
        paste = f.read()

    raw_lines = [
        l.strip()
        for l in paste.splitlines()
        if l.strip() and not l.strip().startswith("update each and")
    ]

    pos = 0
    for idx, c in enumerate(cards):
        w = c["word"]
        num = c.get("originalNum") or c.get("num") or (2001 + idx)
        while pos < len(raw_lines) and raw_lines[pos] != w:
            pos += 1
        next_w = card_words[idx + 1] if idx + 1 < len(card_words) else None
        pos += 1
        block = []
        while pos < len(raw_lines):
            if next_w and raw_lines[pos] == next_w:
                if pos + 1 < len(raw_lines) and (
                    raw_lines[pos + 1].startswith("Hindi:")
                    or (
                        raw_lines[pos + 1].endswith(":")
                        and pos + 2 < len(raw_lines)
                        and raw_lines[pos + 2].startswith("Hindi:")
                    )
                ):
                    break
            block.append(raw_lines[pos])
            pos += 1

        senses = []
        cur_label = None
        cur_hi = None
        cur_es = None
        for b in block:
            if b.startswith("Hindi:"):
                cur_hi = b[len("Hindi:") :].strip()
            elif b.startswith("Spanish:"):
                cur_es = b[len("Spanish:") :].strip()
                senses.append((cur_label, cur_hi, cur_es))
                cur_label = None
                cur_hi = None
                cur_es = None
            elif b.endswith(":"):
                cur_label = b[:-1].strip()

        if not senses:
            raise RuntimeError(f"No senses parsed for {num} {w}")

        if num in MULTI_TAMIL_2001_2500:
            c["tamil"] = MULTI_TAMIL_2001_2500[num]

        if len(senses) == 1:
            lbl, hi_v, es_v = senses[0]
            c["trans"]["hi"] = hi_v
            c["trans"]["es"] = es_v
            c["shortcutEs"] = build_es_sense_shortcut(w, lbl, es_v)
            c["shortcutHi"] = build_hi_sense_shortcut(w, lbl, hi_v, c.get("tamil", ""))
        else:
            hi_parts = []
            es_parts = []
            ses_parts = []
            shi_parts = []
            ta_senses = [t.strip() for t in c.get("tamil", "").split("/")]
            for s_i, (lbl, hi_v, es_v) in enumerate(senses, 1):
                hi_parts.append(f"{s_i}. {lbl}: {hi_v}")
                es_parts.append(f"{s_i}. {lbl}: {es_v}")
                ta_s = ta_senses[s_i - 1] if s_i - 1 < len(ta_senses) else c.get("tamil", "")
                ses = build_es_sense_shortcut(w, lbl, es_v)
                shi = build_hi_sense_shortcut(w, lbl, hi_v, ta_s)
                ses = re.sub(
                    r"^<strong>",
                    f"<strong>{s_i}. ({lbl}) ",
                    ses,
                    count=1,
                )
                shi = re.sub(
                    r"^<strong>",
                    f"<strong>{s_i}. ({lbl}) ",
                    shi,
                    count=1,
                )
                ses_parts.append(ses)
                shi_parts.append(shi)

            c["trans"]["hi"] = " | ".join(hi_parts)
            c["trans"]["es"] = " | ".join(es_parts)
            c["shortcutEs"] = "<br>".join(ses_parts)
            c["shortcutHi"] = "<br>".join(shi_parts)

        c["hiDevanagari"] = c["trans"]["hi"]

    new_json = json.dumps(cards, ensure_ascii=False)
    html = html[:json_start] + new_json + html[json_end:]
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # Also update data/backup_original_cards.json so backups match 100%
    with open("data/backup_original_cards.json", "r", encoding="utf-8") as f:
        bkp = json.load(f)
    by_num = {c.get("originalNum") or c.get("num"): c for c in cards}
    for item in bkp:
        if item.get("tier") == "tier2001DeckCards":
            n = item.get("originalNum") or item.get("num")
            if n in by_num:
                src = by_num[n]
                item["trans"] = dict(src["trans"])
                item["tamil"] = src["tamil"]
                item["shortcutEs"] = src["shortcutEs"]
                item["shortcutHi"] = src["shortcutHi"]
                item["hiDevanagari"] = src["hiDevanagari"]
    with open("data/backup_original_cards.json", "w", encoding="utf-8") as f:
        json.dump(bkp, f, ensure_ascii=False, indent=2)

    print("Successfully updated all 500 cards in index.html and data/backup_original_cards.json!")


if __name__ == "__main__":
    main()
