from __future__ import annotations

import requests
from bs4 import BeautifulSoup

from app.models import ArticleCandidate, ArticleDigest
import re
from googlenewsdecoder import new_decoderv1
import urllib.parse

REQUEST_TIMEOUT_SECONDS = 10
DEFAULT_USER_AGENT = "Mozilla/5.0 (week4 learning project)"
DEFAULT_WARNING_FETCH_FAILED = "Failed to fetch original article."
DEFAULT_WARNING_STUB_SUMMARY = "Summary is still a simple extraction-based summary."
DEFAULT_WARNING_TEXT_EXTRACTION_FAILED = "Failed to extract usable article text."
DEFAULT_EXTRACTION_SUCCESS = "Success"
DEFAULT_EXTRACTION_FAILED = "Failed"
TEXT_PREVIEW_LENGTH = 500


DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
REQUEST_TIMEOUT_SECONDS = 10

def _resolve_final_url(url: str) -> tuple[str, bool]:
    # --- 1. 第一道防線：套件解碼 ---
    if "news.google.com" in url:
        try:
            decoded = new_decoderv1(url)
            if decoded and decoded.get("status"):
                return decoded.get("decoded_url"), True
        except Exception:
            pass 

    # --- 2. 第二道防線：發送請求並用 Regex 暴力破解 ---
    headers = {
        "User-Agent": DEFAULT_USER_AGENT,
        # 加上 Cookie 繞過 Google 可能的隱私權同意畫面 (Consent Page)
        "Cookie": "CONSENT=YES+cb;",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS, allow_redirects=True)
        response.raise_for_status()
        
        final_url = response.url

        if "news.google.com" in final_url:
            html_text = response.text
            
            # 策略 A: 尋找 Google 藏在自訂標籤裡的 data-n-au 屬性
            match = re.search(r'data-n-au=["\'](https?://[^"\']+)["\']', html_text)
            if match:
                return match.group(1), True
                
            # 策略 B: 尋找 JavaScript 的 window.location 跳轉
            match = re.search(r'window\.location\.replace\([\'"](https?://[^\'"]+)[\'"]\)', html_text)
            if match:
                return match.group(1), True
            
            # 策略 C: 尋找可能被 URL Encode 過的隱藏變數
            match = re.search(r'(?:url|href)\s*=\s*[\'"](https?://[^\'"]+)[\'"]', html_text)
            if match:
                decoded_url = urllib.parse.unquote(match.group(1))
                # 確保解碼出來的不是 google 自己
                if "google.com" not in decoded_url:
                    return decoded_url, True

            # 策略 D: 保留原本的 BeautifulSoup 作為最後防線
            soup = BeautifulSoup(html_text, "html.parser")
            meta_refresh = soup.find("meta", attrs={"http-equiv": re.compile("refresh", re.IGNORECASE)})
            if meta_refresh:
                content = meta_refresh.get("content", "")
                match = re.search(r'url=(.*)', content, re.IGNORECASE)
                if match:
                    return match.group(1).strip("'\" "), True

        return final_url, True

    except requests.RequestException:
        return url, False

def _fetch_article_page(url: str) -> tuple[bool, str]:
    headers = {
        "User-Agent": DEFAULT_USER_AGENT,
    }

    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        return True, response.text
    except requests.RequestException:
        return False, ""


def _extract_text_from_html(page_html: str) -> str:
    soup = BeautifulSoup(page_html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    cleaned_text = " ".join(text.split())
    return cleaned_text

def _split_into_sentences(text: str) -> list[str]:
    parts = re.split(r'(?<=[.!?])\s+', text)
    sentences = [part.strip() for part in parts if part.strip()]
    return sentences


def _build_simple_summary(article_text: str, max_sentences: int = 3) -> tuple[str, list[str]]:
    sentences = _split_into_sentences(article_text)

    usable_sentences = []
    for sentence in sentences:
        if len(sentence) >= 40:
            usable_sentences.append(sentence)

    if not usable_sentences:
        fallback = article_text[:TEXT_PREVIEW_LENGTH]
        return fallback, [fallback] if fallback else []

    summary_sentences = usable_sentences[:max_sentences]
    summary = " ".join(summary_sentences)
    key_points = summary_sentences

    return summary, key_points


def summarize_article(candidate: ArticleCandidate) -> ArticleDigest:
    resolved_url, resolve_ok = _resolve_final_url(candidate.url)

    fetch_ok, page_html = _fetch_article_page(resolved_url)

    if not fetch_ok:
        return ArticleDigest(
            title=candidate.title,
            url=resolved_url,
            source=candidate.source,
            published_date=candidate.published_date,
            extraction_status=DEFAULT_EXTRACTION_FAILED,
            summary=(
                f"Could not fetch the article page for '{candidate.title}'. "
                "Returning metadata-only stub summary."
            ),
            key_points=[
                f"Article source: {candidate.source}",
                f"Resolved URL success: {resolve_ok}",
                "Fetched HTML length: 0 characters",
            ],
            warnings=[
                DEFAULT_WARNING_FETCH_FAILED,
                DEFAULT_WARNING_STUB_SUMMARY,
            ],
        )

    article_text = _extract_text_from_html(page_html)

    if not article_text:
        return ArticleDigest(
            title=candidate.title,
            url=resolved_url,
            source=candidate.source,
            published_date=candidate.published_date,
            extraction_status=DEFAULT_EXTRACTION_FAILED,
            summary=(
                f"Fetched the article page for '{candidate.title}', "
                "but failed to extract usable article text."
            ),
            key_points=[
                f"Article source: {candidate.source}",
                f"Resolved URL success: {resolve_ok}",
                f"Fetched HTML length: {len(page_html)} characters",
            ],
            warnings=[
                DEFAULT_WARNING_TEXT_EXTRACTION_FAILED,
                DEFAULT_WARNING_STUB_SUMMARY,
            ],
        )

    summary_text, summary_points = _build_simple_summary(article_text)

    return ArticleDigest(
        title=candidate.title,
        url=resolved_url,
        source=candidate.source,
        published_date=candidate.published_date,
        extraction_status=DEFAULT_EXTRACTION_SUCCESS,
        summary=summary_text,
        key_points=summary_points,
        warnings=[DEFAULT_WARNING_STUB_SUMMARY],
    )