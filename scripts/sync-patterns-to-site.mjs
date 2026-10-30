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

if (fs.existsSync(checklistSrc)) {
  const body = fs.readFileSync(checklistSrc, "utf8");
  const withFm = `---
title: "Agentic AI Production Readiness Checklist"
description: "Pre-production checklist for enterprise agent workflows"
---

${body.replace(/^# .+\n/, "")}`;
  fs.writeFileSync(checklistOut, withFm);
  console.log("synced checklist");
}
