"""Web scraping, HTML text extraction, and SHA-256 source metadata service."""

from __future__ import annotations

import datetime
import hashlib
import html as html_lib
import re
import urllib.request
from dataclasses import dataclass

from ..schemas.common import SourceMetadata


@dataclass
class FetchedSourceDocument:
    """Container for fetched web page metadata and cleaned text content."""

    metadata: SourceMetadata
    extracted_text: str
    raw_html: str


def extract_text_from_html(raw_html: str) -> str:
    """Convert raw HTML into clean, readable plain text for LLM analysis."""
    # Remove script, style, noscript, svg, header, footer, nav blocks
    cleaned = re.sub(
        r"<(script|style|noscript|svg|nav|footer)[^>]*>.*?</\1>",
        " ",
        raw_html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    # Replace block-level tags with newlines
    cleaned = re.sub(
        r"</?(p|div|br|h[1-6]|li|tr|article|section|blockquote)[^>]*>",
        "\n",
        cleaned,
        flags=re.IGNORECASE,
    )
    # Strip remaining HTML tags
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    # Unescape HTML entities
    cleaned = html_lib.unescape(cleaned)
    # Collapse horizontal whitespace and multiple blank lines
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in cleaned.splitlines()]
    non_empty_lines = [line for line in lines if line]
    return "\n".join(non_empty_lines)


def _extract_meta_tag(raw_html: str, names: list[str]) -> str:
    """Extract content from a meta tag matching any of the given property/name attributes."""
    for name in names:
        escaped = re.escape(name)
        pattern = rf'<meta[^>]+(?:property|name)=["\']{escaped}["\'][^>]+content=["\']([^"\']+)["\']'
        match = re.search(pattern, raw_html, re.IGNORECASE)
        if not match:
            pattern_inv = rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']{escaped}["\']'
            match = re.search(pattern_inv, raw_html, re.IGNORECASE)
        if match and match.group(1).strip():
            return html_lib.unescape(match.group(1).strip())
    return "Not specified"


def fetch_url_content_and_metadata(url: str, timeout: int = 30) -> FetchedSourceDocument:
    """Download a URL, compute its SHA-256 hash, extract metadata and readable text."""
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
            )
        },
    )

    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_bytes = response.read()
        raw_html = content_bytes.decode("utf-8", errors="ignore")

    title_match = re.search(r"<title[^>]*>(.*?)</title>", raw_html, re.IGNORECASE | re.DOTALL)
    title = (
        html_lib.unescape(title_match.group(1).strip())
        if title_match and title_match.group(1).strip()
        else _extract_meta_tag(raw_html, ["og:title", "twitter:title"])
    )

    publisher = _extract_meta_tag(raw_html, ["og:site_name", "publisher", "application-name"])
    author = _extract_meta_tag(raw_html, ["author", "article:author", "dc.creator"])
    published_date = _extract_meta_tag(
        raw_html,
        ["article:published_time", "pubdate", "publishdate", "date", "dc.date"],
    )

    metadata = SourceMetadata(
        url=url,
        title=title,
        publisher=publisher,
        author=author,
        published_date=published_date,
        retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        sha256_hash=hashlib.sha256(content_bytes).hexdigest(),
    )
    extracted_text = extract_text_from_html(raw_html)

    return FetchedSourceDocument(
        metadata=metadata,
        extracted_text=extracted_text,
        raw_html=raw_html,
    )
