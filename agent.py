from retriever import search_catalog

CLARIFICATION = "Could you provide job role, skills, and experience level?"

OFF_TOPIC = ["weather", "cricket", "movie", "politics", "song"]

VAGUE = ["assessment", "test", "hire", "hiring"]

PERSONALITY = ["personality", "opq"]
COGNITIVE = ["cognitive", "aptitude"]
SKILLS = ["python", "java", "sql", "developer", "engineer", "analyst"]


def text(messages):
    return " ".join([m["content"] for m in messages]).lower()


def is_off_topic(q):
    return any(x in q for x in OFF_TOPIC)


def is_comparison(q):
    return any(x in q for x in ["difference", "compare", "vs", "versus"])


def needs_clarification(q):
    return any(x in q for x in VAGUE) and not any(x in q for x in PERSONALITY + COGNITIVE + SKILLS)


def compare_opq_gsa():
    return {
        "reply": (
            "OPQ (Occupational Personality Questionnaire) measures personality traits "
            "like behavior, motivation, and working style. "
            "GSA (Global Skills Assessment) measures job-related skills and behavioral performance. "
            "So OPQ focuses on personality, while GSA focuses on skills."
        ),
        "recommendations": [],
        "end_of_conversation": False
    }


def process(messages):

    q = text(messages)

    # 1. OFF TOPIC
    if is_off_topic(q):
        return {
            "reply": "I can only help with SHL assessments.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # 2. CLARIFICATION
    if needs_clarification(q):
        return {
            "reply": CLARIFICATION,
            "recommendations": [],
            "end_of_conversation": False
        }

    # 3. IMPORTANT FIX: STRICT COMPARISON HANDLING
    if is_comparison(q):

        # ONLY trigger comparison for OPQ vs GSA
        if "opq" in q and "gsa" in q:
            return compare_opq_gsa()

        return {
            "reply": "Please specify which assessments you want to compare (e.g., OPQ vs GSA).",
            "recommendations": [],
            "end_of_conversation": False
        }

    # 4. NORMAL SEARCH (ONLY WHEN NOT COMPARISON)
    results = search_catalog(q, top_k=5)

    recommendations = [
        {
            "name": r.get("name", ""),
            "url": r.get("link", ""),
            "reason": f"Matched based on: {q}"
        }
        for r in results
    ]

    return {
        "reply": "Here are the most relevant SHL assessments based on your requirement.",
        "recommendations": recommendations,
        "end_of_conversation": True
    }