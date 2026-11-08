import json
import re

def main():
    print("Reading index.html...")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Fix reindexAndBuildCards so it preserves c.originalNum || c.num
    old_block = """            return {
              ...c,
              id: c.id || `${deckInfo.id}_${c.originalNum || c.num}`,
              originalNum: c.originalNum || c.num,
              num: startNum + idx,
              displayNum: startNum + idx,"""
    
    new_block = """            const cardNum = c.originalNum || c.num || (startNum + idx);
            return {
              ...c,
              id: c.id || `${deckInfo.id}_${cardNum}`,
              originalNum: cardNum,
              num: cardNum,
              displayNum: cardNum,"""

    if old_block in html:
        html = html.replace(old_block, new_block, 1)
        print("✓ Successfully patched reindexAndBuildCards to preserve originalNum & num!")
    else:
        print("Warning: old_block not found in html verbatim, searching via regex...")
        pattern = r"return\s*\{\s*\.\.\.c,\s*id:\s*c\.id\s*\|\|\s*`\$\{deckInfo\.id\}_\$\{c\.originalNum\s*\|\|\s*c\.num\}`,\s*originalNum:\s*c\.originalNum\s*\|\|\s*c\.num,\s*num:\s*startNum\s*\+\s*idx,\s*displayNum:\s*startNum\s*\+\s*idx,"
        m = re.search(pattern, html)
        if m:
            html = html[:m.start()] + new_block + html[m.end():]
            print("✓ Successfully patched reindexAndBuildCards via regex!")
        else:
            print("ERROR: Could not locate reindexAndBuildCards return block!")

    # 2. Add referrerpolicy='no-referrer' to front-visual-img
    old_img = '<img\n                    id="front-visual-img"\n                    class="visual-img"\n                    alt="Target vocabulary visual"\n                  />'
    new_img = '<img\n                    id="front-visual-img"\n                    class="visual-img"\n                    alt="Target vocabulary visual"\n                    referrerpolicy="no-referrer"\n                    crossorigin="anonymous"\n                    loading="eager"\n                  />'
    if old_img in html:
        html = html.replace(old_img, new_img, 1)
        print("✓ Successfully patched front-visual-img tag with referrerpolicy and crossorigin!")
    else:
        # try regex for front-visual-img
        m_img = re.search(r'<img\s+id="front-visual-img"[^>]*>', html)
        if m_img:
            html = html[:m_img.start()] + '<img id="front-visual-img" class="visual-img" alt="Target vocabulary visual" referrerpolicy="no-referrer" crossorigin="anonymous" loading="eager" />' + html[m_img.end():]
            print("✓ Successfully patched front-visual-img via regex!")

    # 3. Patch tempImg loading and fallback in renderCardImage
    old_loader = """          const tempImg = new Image();
          tempImg.onload = () => {
            if (renderToken !== activeCardImageToken || currentIndex !== expectedIndex) return;
            frontVisualImgEl.src = tempImg.src;
            frontVisualImgEl.classList.add("loaded");
            if (visualSkeletonEl) {
              visualSkeletonEl.style.opacity = "0";
              setTimeout(() => {
                if (renderToken === activeCardImageToken && visualSkeletonEl) {
                  visualSkeletonEl.style.display = "none";
                }
              }, 160);
            }
          };
          tempImg.onerror = () => {
            if (renderToken !== activeCardImageToken || currentIndex !== expectedIndex) return;
            if (!tempImg.dataset.retriedApi) {
              tempImg.dataset.retriedApi = "true";
              tempImg.src = `/api/image?num=${lookupId}&q=${encodeURIComponent(card.word)}&fallback=1`;
              return;
            }
            if (!tempImg.dataset.retried) {
              tempImg.dataset.retried = "true";
              tempImg.src = buildDynamicCardSvgUri(card);
              return;
            }
            if (visualSkeletonEl) visualSkeletonEl.style.display = "none";
            frontVisualImgEl.style.display = "none";
            if (frontVisualFallbackEl) frontVisualFallbackEl.style.display = "flex";
          };
          tempImg.src = primaryImgUrl;"""

    new_loader = """          const tempImg = new Image();
          tempImg.referrerPolicy = "no-referrer";
          tempImg.crossOrigin = "anonymous";
          tempImg.onload = () => {
            if (renderToken !== activeCardImageToken || currentIndex !== expectedIndex) return;
            frontVisualImgEl.src = tempImg.src;
            frontVisualImgEl.classList.add("loaded");
            if (visualSkeletonEl) {
              visualSkeletonEl.style.opacity = "0";
              setTimeout(() => {
                if (renderToken === activeCardImageToken && visualSkeletonEl) {
                  visualSkeletonEl.style.display = "none";
                }
              }, 160);
            }
          };
          tempImg.onerror = () => {
            if (renderToken !== activeCardImageToken || currentIndex !== expectedIndex) return;
            // 1. Direct proxy retry through server with full buffer streaming
            if (!tempImg.dataset.retriedProxy) {
              tempImg.dataset.retriedProxy = "true";
              tempImg.src = `/api/proxy-image?url=${encodeURIComponent(primaryImgUrl)}&num=${lookupId}&q=${encodeURIComponent(card.word)}`;
              return;
            }
            // 2. Verified real-world image resolver by word/num
            if (!tempImg.dataset.retriedApi) {
              tempImg.dataset.retriedApi = "true";
              tempImg.src = `/api/image?num=${lookupId}&q=${encodeURIComponent(card.word)}`;
              return;
            }
            // 3. Fallback illustration only if network fails completely
            if (!tempImg.dataset.retriedSvg) {
              tempImg.dataset.retriedSvg = "true";
              tempImg.src = buildDynamicCardSvgUri(card);
              return;
            }
            if (visualSkeletonEl) visualSkeletonEl.style.display = "none";
            frontVisualImgEl.style.display = "none";
            if (frontVisualFallbackEl) frontVisualFallbackEl.style.display = "flex";
          };
          tempImg.src = primaryImgUrl;"""

    if old_loader in html:
        html = html.replace(old_loader, new_loader, 1)
        print("✓ Successfully patched tempImg loading and fallback pipeline!")
    else:
        print("Warning: old_loader not found verbatim in html!")

    # 4. Normalize all thumb.wikimedia.org to upload.wikimedia.org without tracking query params
    sub_count = 0
    def repl_wiki(m):
        nonlocal sub_count
        sub_count += 1
        url = m.group(0)
        url = url.replace("https://thumb.wikimedia.org", "https://upload.wikimedia.org")
        url = re.sub(r'\?utm_source=[^"\'\s&]+(?:&utm_campaign=[^"\'\s&]+)?(?:&utm_content=[^"\'\s&]+)?', '', url)
        return url

    html = re.sub(r'https://thumb\.wikimedia\.org/wikipedia/commons/thumb/[^"\'\s]+', repl_wiki, html)
    print(f"✓ Replaced {sub_count} thumb.wikimedia.org URLs in index.html with canonical upload.wikimedia.org!")

    # 5. Save updated index.html
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved index.html successfully.")

if __name__ == "__main__":
    main()
