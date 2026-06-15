import html
import re
import unicodedata
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Iterable
from urllib.parse import urljoin, urlparse

import httpx


DEFAULT_SOURCE_URLS = [
    "https://cocayhoala.vn/blogs/news-cocayhoala?view=en",
    "https://cocayhoala.vn/blogs/cham-soc-toc",
    "https://cocayhoala.vn/blogs/cham-soc-co-the",
    "https://cocayhoala.vn/blogs/cham-soc-da",
    "https://cocayhoala.vn/blogs/tin-tuc-co-cay-hoa-la",
    "https://cocayhoala.vn/blogs/cau-chuyen-thuong-hieu",
    "https://cocayhoala.vn/blogs/kien-thuc-chuyen-sau",
]
DEFAULT_TIMEOUT = 20
MAX_EXCERPT_CHARS = 700


@dataclass
class SourceArticle:
    title: str
    slug: str
    content: str
    seo_keyword: str
    source_url: str
    image_url: str | None = None


class BlogHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []
        self.images: list[str] = []
        self.meta: dict[str, str] = {}
        self.text_parts: list[str] = []
        self.title_parts: list[str] = []
        self._capture_tag: str | None = None
        self._tag_stack: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "a" and attrs_dict.get("href"):
            self.links.append(attrs_dict["href"])
            return
        if tag == "img":
            src = attrs_dict.get("src") or attrs_dict.get("data-src") or attrs_dict.get("data-original")
            if src:
                self.images.append(html.unescape(src).strip())
            return
        if tag == "meta":
            key = attrs_dict.get("property") or attrs_dict.get("name")
            value = attrs_dict.get("content")
            if key and value:
                self.meta[key.lower()] = html.unescape(value).strip()
            return
        if tag == "h1":
            self._capture_tag = "title"
        elif tag in {"p", "li", "h2", "h3"}:
            self._capture_tag = "body"
            self._tag_stack.append(tag)

    def handle_endtag(self, tag):
        if tag in {"p", "li", "h1", "h2", "h3"}:
            self._capture_tag = None
        if tag in {"p", "li", "h2", "h3"} and self._tag_stack:
            self._tag_stack.pop()

    def handle_data(self, data):
        text = normalize_space(data)
        if not text:
            return
        if self._capture_tag == "title":
            self.title_parts.append(text)
        elif self._capture_tag == "body":
            tag = self._tag_stack[-1] if self._tag_stack else "p"
            self.text_parts.append(f"{tag}\t{text}")


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def slugify(value: str) -> str:
    value = value.replace("\u0111", "d").replace("\u0110", "D")
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return value.strip("-")[:180] or "blog-post"


def clean_title(title: str) -> str:
    title = normalize_space(title)
    for suffix in ("- Co Cay Hoa La", "- C Cay Hoa L", "– Co Cay Hoa La"):
        title = title.replace(suffix, "")
    return title.strip(" -")


def parse_html(raw_html: str) -> BlogHTMLParser:
    parser = BlogHTMLParser()
    parser.feed(raw_html)
    return parser


def extract_article_html(raw_html: str) -> str:
    match = re.search(r"<article\b[^>]*>.*?</article>", raw_html, flags=re.IGNORECASE | re.DOTALL)
    return match.group(0) if match else raw_html


def meta_image_urls(parser: BlogHTMLParser) -> list[str]:
    urls: list[str] = []
    for key in ("og:image:secure_url", "og:image", "twitter:image"):
        value = parser.meta.get(key)
        if value and value not in urls:
            urls.append(value)
    return urls


def is_article_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.netloc and parsed.netloc != "cocayhoala.vn":
        return False
    parts = [part for part in parsed.path.split("/") if part]
    return len(parts) >= 3 and parts[0] == "blogs"


def unique_article_urls(source_url: str, links: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    article_urls: list[str] = []
    for href in links:
        absolute = urljoin(source_url, href).split("#", 1)[0]
        if is_article_url(absolute) and absolute not in seen:
            seen.add(absolute)
            article_urls.append(absolute)
    return article_urls


def fetch(client: httpx.Client, url: str) -> str:
    response = client.get(url)
    response.raise_for_status()
    return response.text


def split_tagged_text(tagged_text: str) -> tuple[str, str]:
    if "\t" not in tagged_text:
        return "p", tagged_text
    tag, text = tagged_text.split("\t", 1)
    return tag, text


def trim_article_parts(title: str, tagged_parts: list[str]) -> list[tuple[str, str]]:
    parts = [split_tagged_text(part) for part in tagged_parts]
    title_lower = title.lower()
    start = 0
    for idx, (_, text) in enumerate(parts):
        text_lower = text.lower()
        if text_lower == title_lower or title_lower in text_lower or text_lower in title_lower:
            start = idx + 1
            break

    stop_markers = {
        "featured products",
        "related articles",
        "news categories",
        "sign up to receive news from us",
        "customer support",
        "store system",
        "product name",
    }
    noise = {"home", "products", "menu", "shopping cart", "cart is empty", "see more", "close"}
    cleaned: list[tuple[str, str]] = []
    for tag, text in parts[start:]:
        text_lower = text.lower()
        if text_lower in stop_markers or text.startswith("Copyrights"):
            break
        if text_lower in noise:
            continue
        cleaned.append((tag, text))
    return cleaned


def is_noise_image(url: str) -> bool:
    lowered = url.lower()
    tokens = [
        "loading",
        "logo",
        "icon",
        "favicon",
        "bocongthuong",
        "cart",
        "facebook.com/tr",
        "pixel",
        "analytics",
        "tracking",
        "sprite",
    ]
    return any(token in lowered for token in tokens)


def absolute_image_urls(article_url: str, images: Iterable[str]) -> list[str]:
    result: list[str] = []
    for image in images:
        absolute = urljoin(article_url, image)
        if absolute.startswith("data:") or is_noise_image(absolute):
            continue
        if absolute not in result:
            result.append(absolute)
    return result


def build_html_content(parts: list[tuple[str, str]], image_urls: list[str], source_url: str, full: bool) -> str:
    html_parts: list[str] = []
    if image_urls:
        image = html.escape(image_urls[0], quote=True)
        html_parts.append(f'<figure><img src="{image}" alt="" /></figure>')

    body_parts = parts if full else parts[:3]
    for tag, text in body_parts:
        safe_text = html.escape(text)
        if tag in {"h2", "h3"}:
            html_parts.append(f"<{tag}>{safe_text}</{tag}>")
        else:
            html_parts.append(f"<p>{safe_text}</p>")

    source = html.escape(source_url, quote=True)
    html_parts.append(
        f'<p><em>Nguon tham khao: <a href="{source}" target="_blank" rel="noopener noreferrer">{source}</a></em></p>'
    )
    return "\n".join(html_parts)


def collect_article_urls(source_urls: list[str], limit: int = 10) -> tuple[list[str], list[str]]:
    headers = {"User-Agent": "HoaDongDuongContentFactory/1.0"}
    urls: list[str] = []
    warnings: list[str] = []
    with httpx.Client(headers=headers, timeout=DEFAULT_TIMEOUT, follow_redirects=True) as client:
        for source_url in source_urls or DEFAULT_SOURCE_URLS:
            if is_article_url(source_url):
                if source_url not in urls:
                    urls.append(source_url)
                if limit and len(urls) >= limit:
                    return urls, warnings
                continue

            try:
                listing_parser = parse_html(fetch(client, source_url))
            except httpx.HTTPStatusError as exc:
                warnings.append(f"Skipped {source_url}: HTTP {exc.response.status_code}")
                continue
            except httpx.HTTPError as exc:
                warnings.append(f"Skipped {source_url}: {exc.__class__.__name__}")
                continue
            for url in unique_article_urls(source_url, listing_parser.links):
                if url not in urls:
                    urls.append(url)
                if limit and len(urls) >= limit:
                    return urls, warnings
    return urls, warnings


def extract_article(url: str, import_full_content: bool = False) -> SourceArticle:
    headers = {"User-Agent": "HoaDongDuongContentFactory/1.0"}
    with httpx.Client(headers=headers, timeout=DEFAULT_TIMEOUT, follow_redirects=True) as client:
        raw_html = fetch(client, url)

    page_parser = parse_html(raw_html)
    article_parser = parse_html(extract_article_html(raw_html))
    title = clean_title(
        page_parser.meta.get("og:title")
        or page_parser.meta.get("twitter:title")
        or " ".join(article_parser.title_parts)
        or url.rstrip("/").rsplit("/", 1)[-1].replace("-", " ").title()
    )
    article_parts = trim_article_parts(title, article_parser.text_parts)
    image_urls = absolute_image_urls(url, meta_image_urls(page_parser) + article_parser.images)
    body_text = "\n\n".join(text for _, text in article_parts)
    description = page_parser.meta.get("description") or page_parser.meta.get("og:description") or ""
    excerpt = normalize_space(description or body_text)
    if len(excerpt) > MAX_EXCERPT_CHARS:
        excerpt = excerpt[:MAX_EXCERPT_CHARS].rsplit(" ", 1)[0] + "..."

    content = build_html_content(article_parts or [("p", excerpt)], image_urls, url, import_full_content)
    return SourceArticle(
        title=title,
        slug=slugify(title),
        content=content,
        seo_keyword=title[:255],
        source_url=url,
        image_url=image_urls[0] if image_urls else None,
    )


def build_original_draft(topic: str, keyword: str | None = None, audience: str | None = None) -> SourceArticle:
    clean_topic = normalize_space(topic)
    clean_keyword = normalize_space(keyword or topic)
    clean_audience = normalize_space(audience or "nguoi quan tam den cham soc toc va co the tu thien nhien")
    title = f"{clean_topic}: huong dan cham soc tu thien nhien"
    content = (
        f"<p><strong>{html.escape(clean_topic)}</strong> la chu de phu hop voi {html.escape(clean_audience)}. "
        "Bai viet nay duoc tao nhu mot ban nhap SEO de bien tap truoc khi xuat ban.</p>"
        f"<h2>Vi sao {html.escape(clean_keyword)} dang duoc quan tam?</h2>"
        "<p>Nguoi dung ngay cang uu tien san pham lanh tinh, thanh phan ro rang va trai nghiem cham soc co tinh ben vung. "
        "Noi dung nen giai thich nhu cau that, tranh tuyen bo qua muc va gan voi loi ich co the kiem chung.</p>"
        "<h2>Cach lua chon san pham phu hop</h2>"
        "<ul>"
        "<li>Doc ky bang thanh phan va huong dan su dung.</li>"
        "<li>Uu tien cong thuc phu hop tinh trang da dau, toc hoac lan da.</li>"
        "<li>Thu tren vung nho truoc khi su dung thuong xuyen neu co co dia nhay cam.</li>"
        "</ul>"
        "<h2>Goi y bien tap truoc khi dang</h2>"
        "<p>Bo sung hinh anh san pham, lien ket noi bo, cau hoi thuong gap va thong tin chuyen mon da duoc kiem chung. "
        "Editor can ra soat lai giong van, tinh chinh xac va yeu cau phap ly truoc khi publish.</p>"
    )
    return SourceArticle(
        title=title,
        slug=slugify(title),
        content=content,
        seo_keyword=clean_keyword[:255],
        source_url="original-draft",
    )
