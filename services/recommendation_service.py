"""
recommendation_service.py
System-driven recommendation engine (PRD Sections 13-18, 52-56).
Uses Flask-SQLAlchemy ORM - fetch functions pull rows via the ORM and
convert them to plain dicts, then the scoring logic works on those
dicts (keeps the scoring code simple and DB-library-agnostic).

Pipeline (PRD Section 55):
    Read current user's skill rows
        -> Retrieve candidate users (global, excluding self)
        -> Remove ineligible candidates
        -> Compare Desired <-> Offered skills (both directions)
        -> Compare skill levels
        -> Compare categories
        -> Factor in avg_rating
        -> Calculate match score
        -> Sort + return top N

NOTE (PRD Section 17, 83): exact score weighting is an open decision.
The weights below are configurable constants - tune freely without
touching the scoring logic itself.
"""

from backend.extensions import db
from backend.models import User, Skill
from backend.utils.normalization import normalize_skill, level_rank

# ---- Configurable weights (PRD Section 17) --------------------------
WEIGHTS = {
    "skill_match": 35,        # desired -> their offered skill
    "mutual_swap_bonus": 25,  # both directions match (two-way swap)
    "level_match": 20,        # skill-level compatibility
    "category_match": 10,     # same category
    "rating_factor": 10,      # avg_rating contribution
}
MAX_POSSIBLE_SCORE = sum(WEIGHTS.values())  # 100


def _skill_to_dict(s: Skill) -> dict:
    return {
        "skill_id": str(s.skill_id),
        "user_id": str(s.user_id),
        "category_id": s.category_id,
        "skill": s.skill,
        "skill_level": s.skill_level,
        "desired_skill": s.desired_skill,
        "desired_level": s.desired_level,
    }


def _fetch_user_skills(user_id: str):
    rows = Skill.query.filter_by(user_id=user_id).all()
    return [_skill_to_dict(s) for s in rows]


def _fetch_candidate_skills(exclude_user_id: str):
    """
    Retrieves skill rows for every OTHER user, plus that user's name
    and avg_rating (PRD Section 13 - Global Matching).
    """
    rows = (
        db.session.query(Skill, User)
        .join(User, User.user_id == Skill.user_id)
        .filter(Skill.user_id != exclude_user_id)
        .all()
    )
    candidates = []
    for s, u in rows:
        d = _skill_to_dict(s)
        d["name"] = u.name
        d["avg_rating"] = float(u.avg_rating or 0)
        candidates.append(d)
    return candidates


def _level_score(desired_level: str, offered_level: str) -> float:
    """
    Returns 0.0-1.0. Full score if the candidate's proficiency meets or
    exceeds what the requester wants to reach; partial credit otherwise.
    """
    want = level_rank(desired_level)
    have = level_rank(offered_level)
    if want == 0 or have == 0:
        return 0.0
    if have >= want:
        return 1.0
    return max(0.0, 1 - (want - have) / 3)


def _rating_score(avg_rating) -> float:
    """Normalizes a 0-5 rating to 0.0-1.0. Missing rating -> neutral 0.5."""
    if avg_rating is None:
        return 0.5
    return max(0.0, min(1.0, float(avg_rating) / 5))


def _score_pair(my_row: dict, their_row: dict) -> dict:
    """
    Scores one (my desired/offered pair) against one candidate skill row.
    Returns a breakdown dict with a 'total' score 0-100, or None if the
    core requirement (they offer what I want) isn't met.
    """
    my_desired = normalize_skill(my_row["desired_skill"])
    their_offered = normalize_skill(their_row["skill"])
    their_desired = normalize_skill(their_row["desired_skill"])
    my_offered = normalize_skill(my_row["skill"])

    if not my_desired or my_desired != their_offered:
        return None  # core requirement: they must offer what I want

    breakdown = {"skill_match": WEIGHTS["skill_match"]}

    is_mutual = bool(their_desired) and their_desired == my_offered
    breakdown["mutual_swap_bonus"] = WEIGHTS["mutual_swap_bonus"] if is_mutual else 0

    level_fit = _level_score(my_row["desired_level"], their_row["skill_level"])
    breakdown["level_match"] = round(WEIGHTS["level_match"] * level_fit, 2)

    same_category = (
        my_row["category_id"] is not None
        and my_row["category_id"] == their_row["category_id"]
    )
    breakdown["category_match"] = WEIGHTS["category_match"] if same_category else 0

    rating_fit = _rating_score(their_row["avg_rating"])
    breakdown["rating_factor"] = round(WEIGHTS["rating_factor"] * rating_fit, 2)

    breakdown["total"] = round(sum(v for v in breakdown.values()), 2)
    breakdown["is_mutual_swap"] = is_mutual
    return breakdown


def get_recommendations(user_id: str, limit: int = 10):
    """
    Main entry point. Returns a ranked list of recommended users:
    [
      {
        "user_id": ..., "name": ..., "avg_rating": ...,
        "offered_skill": ..., "offered_level": ...,
        "matched_desired_skill": ..., "category_id": ...,
        "match_score": 92.0, "is_mutual_swap": true,
        "score_breakdown": {...}
      },
      ...
    ]
    """
    my_skills = _fetch_user_skills(user_id)
    if not my_skills:
        return []  # PRD Section 64 - empty state: "no skills yet"

    candidates = _fetch_candidate_skills(user_id)
    if not candidates:
        return []  # PRD Section 63 - "no suitable partners found"

    best_by_user = {}

    for my_row in my_skills:
        for their_row in candidates:
            result = _score_pair(my_row, their_row)
            if result is None:
                continue

            candidate_user_id = their_row["user_id"]
            existing = best_by_user.get(candidate_user_id)
            if existing is None or result["total"] > existing["match_score"]:
                best_by_user[candidate_user_id] = {
                    "user_id": candidate_user_id,
                    "name": their_row["name"],
                    "avg_rating": their_row["avg_rating"],
                    "offered_skill": their_row["skill"],
                    "offered_level": their_row["skill_level"],
                    "matched_desired_skill": my_row["desired_skill"],
                    "category_id": their_row["category_id"],
                    "match_score": result["total"],
                    "is_mutual_swap": result["is_mutual_swap"],
                    "score_breakdown": result,
                }

    ranked = sorted(best_by_user.values(), key=lambda r: r["match_score"], reverse=True)
    return ranked[:limit]