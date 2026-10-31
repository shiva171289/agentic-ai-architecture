/**
 * Prefix root-relative markdown links with the GitHub Pages base path.
 * @param {string} base e.g. "/agentic-ai-architecture/"
 */
export function rehypeBaseUrl(base) {
  const prefix = base.endsWith("/") ? base.slice(0, -1) : base;

  return (tree) => {
    walk(tree, (node) => {
      if (node.type !== "element" || node.tagName !== "a") return;
      const href = node.properties?.href;
      if (typeof href !== "string") return;
      if (!href.startsWith("/") || href.startsWith("//")) return;
      node.properties.href = `${prefix}${href}`;
    });
  };
}

function walk(node, fn) {
  fn(node);
  if (node.children) {
    for (const child of node.children) walk(child, fn);
  }
}
