"""xAPI verb vocabulary and IRI-to-shortname mapping.

ADL verb registry: https://registry.tincanapi.com/
"""

VERB_IRI_MAP: dict[str, str] = {
    "http://adlnet.gov/expapi/verbs/registered": "registered",
    "http://adlnet.gov/expapi/verbs/initialized": "initialized",
    "http://adlnet.gov/expapi/verbs/attempted": "attempted",
    "http://adlnet.gov/expapi/verbs/experienced": "experienced",
    "http://adlnet.gov/expapi/verbs/completed": "completed",
    "http://adlnet.gov/expapi/verbs/passed": "passed",
    "http://adlnet.gov/expapi/verbs/failed": "failed",
    "http://adlnet.gov/expapi/verbs/scored": "scored",
}

# Reverse map for building statements
SHORTNAME_TO_IRI = {v: k for k, v in VERB_IRI_MAP.items()}

# Verbs that indicate a learner started/enrolled
ENROLLMENT_VERBS = {"registered", "initialized", "attempted"}

# Verbs indicating course completion
COMPLETION_VERBS = {"completed", "passed"}

SCORING_VERBS = {"scored", "passed", "failed", "completed"}


def resolve_verb(verb_data: dict | str) -> str | None:
    if isinstance(verb_data, str):
        iri = verb_data
    elif isinstance(verb_data, dict):
        iri = verb_data.get("id", "")
    else:
        return None

    return VERB_IRI_MAP.get(iri)


def verb_iri(shortname: str) -> str:
    return SHORTNAME_TO_IRI.get(shortname, "")
