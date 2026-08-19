"""
normalization.py
Prevents formatting differences ("Python" vs "python" vs "PYTHON",
"React.js" vs "React JS" vs "React") from being treated as different
skills. See PRD Section 53.

This is a simple alias-map approach. Extend SKILL_ALIASES as your
platform's controlled skill vocabulary grows.
"""

import re

SKILL_ALIASES = {
    "react.js": "react",
    "reactjs": "react",
    "react js": "react",
    "node.js": "nodejs",
    "node js": "nodejs",
    "vue.js": "vue",
    "vuejs": "vue",
    "c++": "cpp",
    "c#": "csharp",
    "next.js": "nextjs",
}


def normalize_skill(raw: str) -> str:
    """Lowercase, trim, collapse whitespace, then apply alias map."""
    if not raw:
        return ""
    text = raw.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return SKILL_ALIASES.get(text, text)


def normalize_level(raw: str) -> str:
    if not raw:
        return ""
    return raw.strip().lower()


LEVEL_RANK = {
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3,
}


def level_rank(level: str) -> int:
    return LEVEL_RANK.get(normalize_level(level), 0)