/** Shared URL helpers for site sync and link validation. */
export const SITE_ORIGIN = "https://shiva171289.github.io";
export const SITE_BASE = "/agentic-ai-architecture/";
export const GITHUB_REPO = "https://github.com/shiva171289/agentic-ai-architecture";

export function sitePath(path) {
  const p = path.startsWith("/") ? path.slice(1) : path;
  return `${SITE_BASE}${p}`;
}

export function githubBlob(path) {
  return `${GITHUB_REPO}/blob/main/${path.replace(/^\//, "")}`;
}

export function githubTree(path) {
  return `${GITHUB_REPO}/tree/main/${path.replace(/^\//, "")}`;
}
