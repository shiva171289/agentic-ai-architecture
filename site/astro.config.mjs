// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import { rehypeBaseUrl } from "./src/rehype-base-url.mjs";

const base = "/agentic-ai-architecture/";

// GitHub Pages project site
export default defineConfig({
  site: "https://shiva171289.github.io",
  base: "/agentic-ai-architecture",
  trailingSlash: "always",
  integrations: [sitemap()],
  markdown: {
    rehypePlugins: [[rehypeBaseUrl, base]],
  },
});
