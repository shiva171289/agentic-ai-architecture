import rss from "@astrojs/rss";
import { getCollection } from "astro:content";

export async function GET(context) {
  const posts = (await getCollection("blog")).sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf(),
  );
  return rss({
    title: "Agentic AI Architecture",
    description: "Weekly enterprise agentic patterns — AWS and Azure",
    site: context.site,
    items: posts.map((post) => ({
      link: `/blog/${post.id}/`,
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
    })),
  });
}
