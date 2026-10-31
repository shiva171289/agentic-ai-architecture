#!/usr/bin/env node
/**
 * Scan built site HTML for broken links (internal + HTTP HEAD for external).
 * Run after: cd site && npm run build
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SITE_ORIGIN, SITE_BASE } from "./site-urls.mjs";

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const distDir = path.join(root, "site", "dist");

function collectHtmlFiles(dir, out = []) {
  for (const name of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, name.name);
    if (name.isDirectory()) collectHtmlFiles(full, out);
    else if (name.name.endsWith(".html")) out.push(full);
  }
  return out;
}

function extractHrefs(html) {
  const hrefs = [];
  const re = /href="([^"]+)"/g;
  let m;
  while ((m = re.exec(html))) hrefs.push(m[1]);
  return hrefs;
}

function resolveInternal(href) {
  if (href.startsWith("mailto:") || href.startsWith("#")) return null;
  if (href.startsWith("http://") || href.startsWith("https://")) return null;
  if (href.startsWith("//")) return null;

  let pathname = href;
  if (pathname.startsWith(SITE_BASE)) {
    pathname = pathname.slice(SITE_BASE.length - 1);
  } else if (pathname.startsWith("/")) {
    // Root-relative without base — still broken on GitHub Pages project sites
    return { kind: "missing-base", href };
  }

  if (pathname.startsWith("/")) pathname = pathname.slice(1);
  const filePath = path.join(distDir, pathname);
  if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
    const index = path.join(filePath, "index.html");
    if (fs.existsSync(index)) return { kind: "ok", href };
    return { kind: "missing", href, filePath: index };
  }
  if (fs.existsSync(filePath)) return { kind: "ok", href };
  const withIndex = path.join(filePath, "index.html");
  if (fs.existsSync(withIndex)) return { kind: "ok", href };
  return { kind: "missing", href, filePath: withIndex };
}

async function checkExternal(url) {
  try {
    const res = await fetch(url, { method: "HEAD", redirect: "follow" });
    if (res.status >= 400) {
      const get = await fetch(url, { method: "GET", redirect: "follow" });
      return get.status < 400 ? "ok" : `HTTP ${get.status}`;
    }
    return "ok";
  } catch (e) {
    return e.message;
  }
}

if (!fs.existsSync(distDir)) {
  console.error("Missing site/dist — run: cd site && npm run build");
  process.exit(1);
}

const hrefSet = new Set();
for (const file of collectHtmlFiles(distDir)) {
  for (const href of extractHrefs(fs.readFileSync(file, "utf8"))) hrefSet.add(href);
}

const internalProblems = [];
const externalProblems = [];
const externalOk = [];

for (const href of hrefSet) {
  const internal = resolveInternal(href);
  if (internal?.kind === "missing-base") {
    internalProblems.push(`${href} (missing ${SITE_BASE} prefix)`);
    continue;
  }
  if (internal?.kind === "missing") {
    internalProblems.push(`${href} → not found: ${path.relative(root, internal.filePath)}`);
    continue;
  }
  if (internal?.kind === "ok") continue;

  if (href.startsWith("http://") || href.startsWith("https://")) {
    const status = await checkExternal(href);
    if (status === "ok") externalOk.push(href);
    else externalProblems.push(`${href} → ${status}`);
  }
}

console.log(`Checked ${hrefSet.size} unique hrefs in site/dist`);
console.log(`External OK: ${externalOk.length}`);

if (internalProblems.length) {
  console.error("\nBroken internal links:");
  for (const p of internalProblems.sort()) console.error("  ", p);
}

if (externalProblems.length) {
  console.error("\nBroken external links:");
  for (const p of externalProblems.sort()) console.error("  ", p);
}

if (internalProblems.length || externalProblems.length) {
  process.exit(1);
}

console.log("All links passed validation.");
