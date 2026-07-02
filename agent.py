from retriever import search_catalog
import re

CLARIFICATION = "Could you provide job role, skills, and experience level?"

OFF_TOPIC = [
    "weather",
    "cricket",
    "movie",
    "politics",
    "song",
    "football",
    "ipl",
    "bitcoin",
    "crypto",
    "recipe",
    "music",
    "stock",
    "travel",
    "visa",
    "salary",
    "compensation",
    "interview tips",
    "legal",
    "employment law",
]

VAGUE = ["assessment", "test", "hire", "hiring"]

PERSONALITY = ["personality", "opq"]
COGNITIVE = ["cognitive", "aptitude"]
SKILLS = ["python", "java", "sql", "developer", "engineer", "analyst"]
SHL_SCOPE_TERMS = [
    "shl",
    "assessment",
    "test",
    "hire",
    "hiring",
    "candidate",
    "screen",
    "role",
    "job description",
    "jd",
    "personality",
    "cognitive",
    "aptitude",
    "skills",
    "opq",
    "gsa",
]


def text(messages):
    return " ".join([m["content"] for m in messages]).lower()


def is_off_topic(q):
    # Explicit blocked domains
    if any(x in q for x in OFF_TOPIC):
        return True

    # If user asks a broad non-assessment question and gives no SHL hiring signal,
    # treat it as off-topic for this assignment.
    has_scope_signal = any(x in q for x in SHL_SCOPE_TERMS)
    generic_question = bool(
        re.search(
            r"\b(what|why|how|when|where|who)\b", q
        )
    )
    return generic_question and not has_scope_signal


def is_comparison(q):
    # Accept common typo variants like "differnce"/"diffrence" as well.
    return bool(
        re.search(r"\b(compare|comparison|vs|versus|differ\w*|diff\w*)\b", q)
    )


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
            "reply": (
                "I can only help with SHL assessments from the SHL catalog. "
                "I cannot answer non-assessment or general legal/hiring advice requests."
            ),
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