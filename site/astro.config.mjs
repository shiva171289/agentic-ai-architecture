// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// GitHub Pages project site
export default defineConfig({
  site: "https://shiva171289.github.io",
  base: "/agentic-ai-architecture",
  trailingSlash: "always",
  integrations: [sitemap()],
});
