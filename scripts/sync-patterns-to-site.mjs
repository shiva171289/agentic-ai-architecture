import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const patternsDir = path.join(root, "patterns");
const blogOut = path.join(root, "site", "src", "content", "blog");
const checklistSrc = path.join(root, "framework", "production-readiness-checklist.md");
const checklistOut = path.join(root, "site", "src", "content", "pages", "production-readiness-checklist.md");

fs.mkdirSync(blogOut, { recursive: true });
fs.mkdirSync(path.dirname(checklistOut), { recursive: true });

for (const dir of fs.readdirSync(patternsDir, { withFileTypes: true })) {
  if (!dir.isDirectory()) continue;
  const blogPath = path.join(patternsDir, dir.name, "blog.md");
  if (!fs.existsSync(blogPath)) continue;
  const dest = path.join(blogOut, `${dir.name}.md`);
  fs.copyFileSync(blogPath, dest);
  console.log("synced", dest);
}

function syncPageFromMarkdown(src, dest, { title, description }) {
  if (!fs.existsSync(src)) {
    console.warn("skip missing page source:", src);
    return;
  }
  const body = fs.readFileSync(src, "utf8");
  const withFm = `---
title: "${title}"
description: "${description}"
---

${body.replace(/^# .+\n+/, "")}`;
  fs.writeFileSync(dest, withFm);
  console.log("synced", dest);
}

const pagesOut = path.join(root, "site", "src", "content", "pages");

syncPageFromMarkdown(checklistSrc, checklistOut, {
  title: "Agentic AI Production Readiness Checklist",
  description: "Pre-production checklist for enterprise agent workflows",
});

syncPageFromMarkdown(
  path.join(root, "content", "ai-architect-skills-map.md"),
  path.join(pagesOut, "ai-architect-skills-map.md"),
  {
    title: "AI Architect skills map",
    description:
      "Competency matrix mapping calendar weeks to enterprise agentic AI architecture skills.",
  },
);

syncPageFromMarkdown(
  path.join(root, "content", "start-here.md"),
  path.join(pagesOut, "start-here.md"),
  {
    title: "Start Here",
    description:
      "Primer, Acme Support Platform storyline, and level ladder for new readers.",
  },
);
