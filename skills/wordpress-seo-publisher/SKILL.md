---
name: wordpress-seo-publisher
description: Create, publish, and optimize WordPress posts with SEO and GEO analysis. Use when the user wants to create blog posts, publish to WordPress, analyze content for SEO (keywords, headings, meta), or optimize for local/geographic search (GEO).
---

# WordPress SEO Publisher

Workflow for creating posts, publishing to WordPress, and analyzing SEO & GEO.

## Prerequisites

1. **WordPress MCP**: Install [mcp-adapter](https://github.com/WordPress/mcp-adapter) plugin on your WordPress site (or use Application Passwords with REST API).
2. **Environment**: Set `WP_API_URL` to your WordPress site URL (e.g. `https://yoursite.com`).
3. **Auth**: Use OAuth (default), or set `WP_API_USERNAME` + `WP_API_PASSWORD` (Application Password) with `OAUTH_ENABLED=false`.

## Workflow

### 1. Create Post Content

- Generate or edit post content in markdown/HTML.
- Include: title, content, optional meta description, focus keywords.
- For GEO: include location terms (city, region) naturally in text.

### 2. Publish to WordPress

Use WordPress MCP tools (when available) or REST API:

```
POST {WP_API_URL}/wp-json/wp/v2/posts
Authorization: Basic base64(username:application_password)
Content-Type: application/json

{
  "title": "Post Title",
  "content": "<p>Post content...</p>",
  "status": "draft" | "publish"
}
```

Create Application Password: WordPress Admin → Users → Profile → Application Passwords.

### 3. SEO & GEO Analysis

Run the analysis script on content before or after publishing:

```bash
# From file
python scripts/analyze-seo-geo.py post.md --keywords "keyword1,keyword2" --location "Moscow"

# From stdin
echo "<h1>Title</h1><p>Content...</p>" | python scripts/analyze-seo-geo.py - --keywords "seo"
```

**SEO checks**: word count, H1/H2/H3 structure, keyword density (0.5–3% ideal).

**GEO checks**: location mentions, local SEO score.

### 4. Iterate

Based on analysis recommendations:
- Add/move keywords naturally
- Fix heading structure (one H1, logical H2/H3)
- Add location terms for local SEO

## Quick Reference

| Task | Action |
|------|--------|
| Create post | Write content, use MCP or REST API to create |
| Publish | Set `status: "publish"` in API request |
| SEO analysis | `python scripts/analyze-seo-geo.py <file> --keywords "kw1,kw2"` |
| GEO analysis | `python scripts/analyze-seo-geo.py <file> --location "City"` |

## References

- [WordPress REST API Posts](https://developer.wordpress.org/rest-api/reference/posts/)
- [Application Passwords](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/#application-passwords)
