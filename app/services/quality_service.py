import re


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def _normalize_text(text):
    """
    Convert text into a normalized lowercase word string.
    """

    if not text:
        return ""

    return re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        text.lower()
    )


def _get_words(text):
    """
    Return normalized words from text.
    """

    normalized = _normalize_text(text)

    return set(
        word
        for word in normalized.split()
        if len(word) > 2
    )


# ============================================================
# OUTPUT VALIDATION
# ============================================================

def validate_output(output, source_text):

    result = {
        "valid": True,
        "status": "PASS",
        "message": "Output passed validation checks.",
        "checks": []
    }

    # --------------------------------------------------------
    # CHECK 1 — EMPTY OUTPUT
    # --------------------------------------------------------

    if not output or not output.strip():

        result["valid"] = False
        result["status"] = "FAIL"
        result["message"] = "AI returned an empty response."

        result["checks"].append(
            "❌ Non-empty output: Failed"
        )

        return result

    result["checks"].append(
        "✅ Non-empty output: Passed"
    )

    # --------------------------------------------------------
    # CHECK 2 — SOURCE DOCUMENT
    # --------------------------------------------------------

    if not source_text or not source_text.strip():

        result["valid"] = False
        result["status"] = "FAIL"
        result["message"] = (
            "Source document is unavailable."
        )

        result["checks"].append(
            "❌ Source document available: Failed"
        )

        return result

    result["checks"].append(
        "✅ Source document available: Passed"
    )

    # --------------------------------------------------------
    # CHECK 3 — MINIMUM RESPONSE LENGTH
    # --------------------------------------------------------

    output_word_count = len(
        output.split()
    )

    if output_word_count < 20:

        result["status"] = "WARNING"

        result["checks"].append(
            "⚠️ Response length: Limited"
        )

    else:

        result["checks"].append(
            "✅ Response length: Passed"
        )

    # --------------------------------------------------------
    # CHECK 4 — SOURCE GROUNDING
    # --------------------------------------------------------

    source_words = _get_words(
        source_text
    )

    output_words = _get_words(
        output
    )

    if source_words and output_words:

        overlap = (
            source_words.intersection(
                output_words
            )
        )

        overlap_ratio = (
            len(overlap) /
            max(len(output_words), 1)
        )

        if overlap_ratio >= 0.20:

            result["checks"].append(
                "✅ Document grounding: Strong"
            )

        elif overlap_ratio >= 0.10:

            result["status"] = "WARNING"

            result["checks"].append(
                "⚠️ Document grounding: Moderate"
            )

        else:

            result["status"] = "WARNING"

            result["checks"].append(
                "⚠️ Document grounding: Low"
            )

    # --------------------------------------------------------
    # CHECK 5 — STRUCTURED RESPONSE
    # --------------------------------------------------------

    heading_pattern = r"(^|\n)\s*(#+|\*\*)"

    if re.search(
        heading_pattern,
        output
    ):

        result["checks"].append(
            "✅ Structured response: Passed"
        )

    else:

        result["checks"].append(
            "⚠️ Structured response: No headings detected"
        )

    # --------------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------------

    if result["status"] == "PASS":

        result["message"] = (
            "Output passed the automated validation checks."
        )

    elif result["status"] == "WARNING":

        result["message"] = (
            "Output was generated successfully, "
            "but one or more heuristic checks "
            "returned a warning."
        )

    return result


# ============================================================
# HEURISTIC QUALITY EVALUATION
# ============================================================

def evaluate_output(output, source_text):

    if not output or not output.strip():

        return {
            "relevance": 0,
            "consistency": 0,
            "factuality": 0,
            "overall": 0
        }

    if not source_text or not source_text.strip():

        return {
            "relevance": 0,
            "consistency": 0,
            "factuality": 0,
            "overall": 0
        }

    source_words = _get_words(
        source_text
    )

    output_words = _get_words(
        output
    )

    # --------------------------------------------------------
    # WORD OVERLAP
    # --------------------------------------------------------

    if output_words:

        common_words = (
            source_words.intersection(
                output_words
            )
        )

        overlap_ratio = (
            len(common_words) /
            len(output_words)
        )

    else:

        overlap_ratio = 0

    # --------------------------------------------------------
    # RELEVANCE
    #
    # Based on overlap between important words
    # in the source and generated output.
    # --------------------------------------------------------

    relevance = round(
        min(
            100,
            overlap_ratio * 150
        )
    )

    # Minimum useful-response adjustment

    output_length = len(
        output.split()
    )

    if output_length < 20:

        relevance = min(
            relevance,
            60
        )

    # --------------------------------------------------------
    # CONSISTENCY
    #
    # Checks whether the generated output maintains
    # reasonable overlap with the source document.
    # --------------------------------------------------------

    if overlap_ratio >= 0.30:

        consistency = 95

    elif overlap_ratio >= 0.20:

        consistency = 85

    elif overlap_ratio >= 0.10:

        consistency = 70

    elif overlap_ratio > 0:

        consistency = 55

    else:

        consistency = 30

    # --------------------------------------------------------
    # FACTUALITY / GROUNDING INDICATOR
    #
    # This is a heuristic grounding indicator.
    # It is NOT a verified factual accuracy score.
    # --------------------------------------------------------

    if overlap_ratio >= 0.30:

        factuality = 90

    elif overlap_ratio >= 0.20:

        factuality = 80

    elif overlap_ratio >= 0.10:

        factuality = 65

    elif overlap_ratio > 0:

        factuality = 50

    else:

        factuality = 25

    # --------------------------------------------------------
    # STRUCTURE BONUS
    # --------------------------------------------------------

    has_structure = bool(
        re.search(
            r"(^|\n)\s*(#+|\*\*)",
            output
        )
    )

    if has_structure:

        consistency = min(
            100,
            consistency + 5
        )

    # --------------------------------------------------------
    # OVERALL SCORE
    # --------------------------------------------------------

    overall = round(
        (
            relevance
            + consistency
            + factuality
        ) / 3
    )

    return {
        "relevance": relevance,
        "consistency": consistency,
        "factuality": factuality,
        "overall": overall
    }