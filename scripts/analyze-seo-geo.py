#!/usr/bin/env python3
"""
SEO & GEO analysis for WordPress post content.
Analyzes text for SEO metrics (keywords, headings, meta) and GEO relevance (location terms).
Usage: python analyze-seo-geo.py <content_file_or_text> [--keywords "kw1,kw2"] [--location "City, Region"]
"""

import argparse
import re
import sys
from pathlib import Path


def analyze_seo(content: str, focus_keywords: list[str] | None = None) -> dict:
    """Analyze content for SEO metrics."""
    content_lower = content.lower()
    words = re.findall(r"\b\w+\b", content)
    word_count = len(words)

    # Extract headings (H1-H6)
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL | re.IGNORECASE)
    h2 = re.findall(r"<h2[^>]*>(.*?)</h2>", content, re.DOTALL | re.IGNORECASE)
    h3 = re.findall(r"<h3[^>]*>(.*?)</h3>", content, re.DOTALL | re.IGNORECASE)

    # Strip HTML from content for keyword analysis
    text_only = re.sub(r"<[^>]+>", " ", content)
    text_words = re.findall(r"\b\w+\b", text_only.lower())

    result = {
        "word_count": word_count,
        "h1_count": len(h1),
        "h2_count": len(h2),
        "h3_count": len(h3),
        "h1_titles": [re.sub(r"<[^>]+>", "", h).strip()[:80] for h in h1[:5]],
        "h2_titles": [re.sub(r"<[^>]+>", "", h).strip()[:80] for h in h2[:10]],
        "keyword_analysis": {},
        "recommendations": [],
    }

    # Keyword density
    if focus_keywords:
        for kw in focus_keywords:
            kw_lower = kw.lower()
            count = sum(1 for w in text_words if w == kw_lower or kw_lower in w)
            density = (count / word_count * 100) if word_count else 0
            result["keyword_analysis"][kw] = {
                "occurrences": count,
                "density_percent": round(density, 2),
            }

    # SEO recommendations
    if word_count < 300:
        result["recommendations"].append("Content too short. Aim for 300+ words for better SEO.")
    elif word_count > 2000:
        result["recommendations"].append("Consider splitting long content for readability.")

    if len(h1) == 0:
        result["recommendations"].append("Add an H1 heading with primary keyword.")
    elif len(h1) > 1:
        result["recommendations"].append("Use only one H1 per page.")

    if len(h2) < 2 and word_count > 500:
        result["recommendations"].append("Add more H2 subheadings for structure.")

    for kw, data in result.get("keyword_analysis", {}).items():
        if data["density_percent"] < 0.5 and data["occurrences"] < 2:
            result["recommendations"].append(f"Consider using keyword '{kw}' more naturally.")
        elif data["density_percent"] > 3:
            result["recommendations"].append(f"Keyword '{kw}' may be overused (keyword stuffing).")

    return result


def analyze_geo(content: str, target_location: str | None = None) -> dict:
    """Analyze content for GEO/local SEO relevance."""
    content_lower = content.lower()
    result = {
        "location_mentions": [],
        "local_seo_score": 0,
        "recommendations": [],
    }

    # Common location patterns
    location_patterns = [
        r"\b(город|городе|города)\s+([А-Яа-яЁё\s\-]+)",
        r"\b(region|city|town|area)\s+([A-Za-z\s\-]+)",
        r"\b(Москв[аеуы]?|Санкт-Петербург[ае]?|Питер[ае]?)\b",
        r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*([A-Z]{2})\b",  # City, ST
        r"\b(\d{5,6})\b",  # Postal codes
    ]

    for pattern in location_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for m in matches:
            loc = (" ".join(m).strip() if isinstance(m, tuple) else str(m)).strip()
            if len(loc) > 2 and loc not in result["location_mentions"]:
                result["location_mentions"].append(loc)

    # Deduplicate
    result["location_mentions"] = list(dict.fromkeys(result["location_mentions"]))[:20]

    # Score based on location presence
    if target_location:
        target_lower = target_location.lower()
        if target_lower in content_lower:
            result["local_seo_score"] = 80
            result["recommendations"].append(f"Target location '{target_location}' is mentioned.")
        else:
            result["local_seo_score"] = 30
            result["recommendations"].append(f"Add mentions of target location: {target_location}")
    else:
        result["local_seo_score"] = 50 if result["location_mentions"] else 20
        if not result["location_mentions"]:
            result["recommendations"].append("Consider adding location-specific terms for local SEO.")

    return result


def format_report(seo: dict, geo: dict) -> str:
    """Format analysis as readable report."""
    lines = [
        "## SEO & GEO Analysis Report",
        "",
        "### SEO Metrics",
        f"- **Word count:** {seo['word_count']}",
        f"- **H1:** {seo['h1_count']} | **H2:** {seo['h2_count']} | **H3:** {seo['h3_count']}",
    ]
    if seo.get("h1_titles"):
        lines.append("- **H1 titles:** " + "; ".join(seo["h1_titles"][:3]))
    if seo.get("keyword_analysis"):
        lines.append("- **Keyword density:**")
        for kw, d in seo["keyword_analysis"].items():
            lines.append(f"  - {kw}: {d['occurrences']} occurrences ({d['density_percent']}%)")

    lines.extend(["", "### GEO / Local SEO", f"- **Local SEO score:** {}/100".format(geo["local_seo_score"])])
    if geo.get("location_mentions"):
        lines.append(f"- **Location mentions:** {', '.join(geo['location_mentions'][:10])}")

    lines.extend(["", "### Recommendations"])
    for r in seo.get("recommendations", []) + geo.get("recommendations", []):
        lines.append(f"- {r}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="SEO & GEO analysis for content")
    parser.add_argument("content", help="Content text or path to file")
    parser.add_argument("--keywords", help="Comma-separated focus keywords")
    parser.add_argument("--location", help="Target location for GEO analysis")
    args = parser.parse_args()

    content = args.content
    if content == "-":
        content = sys.stdin.read()
    elif Path(content).exists():
        content = Path(content).read_text(encoding="utf-8", errors="ignore")

    keywords = [k.strip() for k in args.keywords.split(",")] if args.keywords else None

    seo = analyze_seo(content, keywords)
    geo = analyze_geo(content, args.location)

    print(format_report(seo, geo))


if __name__ == "__main__":
    main()
