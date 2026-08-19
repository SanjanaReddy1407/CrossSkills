from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import User, Skill

recommendations_bp = Blueprint("recommendations", __name__, url_prefix="/api/recommendations")

# --- ASSUMPTION (PRD open decision #2): ordinal skill-level scale ---
LEVEL_RANK = {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}

# --- ASSUMPTION (PRD open decision #1): match-score weights ---
WEIGHT_DIRECT_MATCH = 40     # candidate offers what I want
WEIGHT_MUTUAL_MATCH = 30     # I also offer what candidate wants (skill-swap bonus)
WEIGHT_LEVEL_FIT = 15        # candidate's proficiency vs. my desired level
WEIGHT_CATEGORY = 10         # shared category between matched skills
WEIGHT_RATING = 5            # candidate's average rating


def _norm(text):
    return (text or "").strip().lower()


def _level_fit_score(desired_level, offered_level):
    """1.0 if offered level meets/exceeds desired level, tapering off otherwise."""
    d_rank = LEVEL_RANK.get(_norm(desired_level))
    o_rank = LEVEL_RANK.get(_norm(offered_level))
    if d_rank is None or o_rank is None:
        return 0.5  # unknown/unspecified level — neutral score
    if o_rank >= d_rank:
        return 1.0
    diff = d_rank - o_rank
    return max(0.0, 1.0 - diff * 0.34)


def _best_skill_match(wanted_list, offered_list):
    """
    wanted_list: [(skill_name, desired_level, category_id), ...]
    offered_list: [(skill_name, skill_level, category_id), ...]
    Returns the best-matching (level_fit_score, category_match) pair, or None.
    """
    best = None
    for w_skill, w_level, w_cat in wanted_list:
        for o_skill, o_level, o_cat in offered_list:
            if _norm(w_skill) == _norm(o_skill) and _norm(w_skill) != "":
                level_fit = _level_fit_score(w_level, o_level)
                category_match = 1.0 if w_cat == o_cat else 0.0
                candidate = (level_fit, category_match)
                if best is None or candidate[0] > best[0]:
                    best = candidate
    return best


@recommendations_bp.route("", methods=["GET"])
@jwt_required()
def get_recommendations():
    current_user_id = get_jwt_identity()

    my_skills = Skill.query.filter_by(user_id=current_user_id).all()
    if not my_skills:
        return jsonify({
            "message": "Add your skills to receive recommendations.",
            "results": [],
        }), 200

    my_offered = [(s.skill, s.skill_level, s.category_id) for s in my_skills if s.skill]
    my_desired = [(s.desired_skill, s.desired_level, s.category_id) for s in my_skills if s.desired_skill]

    if not my_desired:
        return jsonify({
            "message": "Add a skill you want to learn to receive recommendations.",
            "results": [],
        }), 200

    candidates = User.query.filter(User.user_id != current_user_id).all()

    scored = []
    for candidate in candidates:
        candidate_skills = Skill.query.filter_by(user_id=candidate.user_id).all()
        if not candidate_skills:
            continue

        candidate_offered = [(s.skill, s.skill_level, s.category_id) for s in candidate_skills if s.skill]
        candidate_desired = [(s.desired_skill, s.desired_level, s.category_id) for s in candidate_skills if s.desired_skill]

        # Do they offer what I want?
        direct = _best_skill_match(my_desired, candidate_offered)
        if direct is None:
            continue  # no relevant skill overlap at all — not a candidate

        level_fit, category_match = direct

        # Do I offer what they want? (mutual skill-swap bonus)
        reverse = _best_skill_match(candidate_desired, my_offered)
        mutual_match = 1.0 if reverse is not None else 0.0

        rating_score = float(candidate.avg_rating or 0) / 5.0

        score = (
            WEIGHT_DIRECT_MATCH * 1.0
            + WEIGHT_MUTUAL_MATCH * mutual_match
            + WEIGHT_LEVEL_FIT * level_fit
            + WEIGHT_CATEGORY * category_match
            + WEIGHT_RATING * rating_score
        )

        scored.append({
            "user": candidate.to_public_dict(),
            "match_score": round(score, 1),
            "mutual_skill_swap": bool(reverse is not None),
        })

    scored.sort(key=lambda x: x["match_score"], reverse=True)

    if not scored:
        return jsonify({
            "message": "No suitable skill-swap partners found at the moment.",
            "results": [],
        }), 200

    return jsonify({"results": scored[:20]}), 200