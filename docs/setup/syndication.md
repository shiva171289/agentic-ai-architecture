# Syndication setup (GitHub Pages canonical)

GitHub Pages is the **canonical** blog. Other platforms get excerpts or cross-posts with a canonical link back to the site.

**Site base:** `https://shiva171289.github.io/agentic-ai-architecture/`  
**Blog URL pattern:** `https://shiva171289.github.io/agentic-ai-architecture/blog/wNN-slug/`

**Policy:** [02-content-strategy.md](../roadmap/02-content-strategy.md) (Medium timing and length).

---

## 1. GitHub Pages (primary)

1. Open the hub repo on GitHub.
2. Go to **Settings → Pages**.
3. Set **Source** to **GitHub Actions**.
4. Merge to `main`. Confirm workflow **Deploy site to GitHub Pages** succeeds.
5. Open the live blog URL for the pattern week.

Telegram-gated publish: see [04-agent-operations.md](../roadmap/04-agent-operations.md) (`approve publish wNN`).

---

## 2. Medium (manual Week 1)

1. Create a Medium account (or use an existing one).
2. Open **Settings → Security and apps → Integration tokens**.
3. Generate a token. Store it in your password manager (not in this repo).
4. Wait **7–14 days** after the GitHub Pages post is live.
5. Publish an **800–1200 word** excerpt (Post A depth).
6. In Medium story settings, set **Canonical link** to the GitHub Pages blog URL.
7. Add CTA to full pattern, code, and cloud mapping on the site.
8. Record `mediumRepublishDate` in pattern `blog.md` front matter when done.

**Future automation:** GitHub Action with repo secret `MEDIUM_INTEGRATION_TOKEN` (not implemented in v1).

---

## 3. Dev.to (optional cross-post)

1. Create a dev.to account.
2. Open **Settings → Extensions → Generate API Key**.
3. Store the key in your password manager.
4. Publish with **canonical_url** pointing to the GitHub Pages post.
5. Use the same excerpt as Medium or a shorter teaser.

**Future automation:** script under `scripts/` calling Dev.to API (not implemented in v1).

---

## 4. Hashnode (optional cross-post)

1. Create a Hashnode blog / publication.
2. Open **Dashboard → Settings → Developer** (API key).
3. Store the key in your password manager.
4. Cross-post with canonical URL to GitHub Pages.

---

## 5. Substack / newsletter mirror

1. Use Buttondown (Week 0) or Substack for email.
2. Option A: paste the blog intro + link to GitHub Pages.
3. Option B: import site RSS (`/agentic-ai-architecture/rss.xml` after deploy) as a source—verify formatting manually.

---

## Checklist after each weekly merge

1. GitHub Pages live and linked from repo README if needed.
2. LinkedIn Post A (Tue) and Post B (Thu)—manual paste.
3. Update LinkedIn Featured: [linkedin-featured-checklist.md](linkedin-featured-checklist.md).
4. Medium excerpt (optional, delayed 7–14 days).
5. Log reach metrics in private `metrics.md`.

---

## Related

- [week1-operating-guide.md](week1-operating-guide.md)
- [hermes/templates/blog.md](../../hermes/templates/blog.md)
