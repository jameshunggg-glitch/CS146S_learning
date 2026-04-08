from dataclasses import dataclass, field


@dataclass
class ArticleCandidate:
    title: str
    url: str
    source: str
    published_date: str
    note: str = ""


@dataclass
class ArticleDigest:
    title: str
    url: str
    source: str
    published_date: str
    extraction_status: str
    summary: str
    key_points: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)