/** Set your Buttondown username after Week 0 signup. See docs/setup/week0-accounts-checklist.md */
export const buttondownUsername = "YOUR_BUTTONDOWN_USERNAME";

export const siteTitle = "Agentic AI Architecture";
export const siteTagline =
  "Learn enterprise agentic AI week by week—one fictional support platform, runnable code on GitHub.";

export const githubRepo = "https://github.com/shiva171289/agentic-ai-architecture";

/** GitHub blob link for repo paths (no leading slash required). */
export function githubBlob(path: string) {
  return `${githubRepo}/blob/main/${path.replace(/^\//, "")}`;
}
