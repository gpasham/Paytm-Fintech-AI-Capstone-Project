import os
import re


def extract_signals(snippet: str) -> dict:
    """Extract disclosure signals using deterministic mock keyword/regex rules."""
    text = snippet.lower()

    risk_flags = []

    if "litigation" in text:
        risk_flags.append("litigation")

    if "regulatory" in text:
        risk_flags.append("regulatory")

    if (
        "customer concentration" in text
        or "top three customers" in text
        or re.search(r"\b\d+\s*percent of (?:total )?revenue\b", text)
    ):
        risk_flags.append("customer concentration")

    hedging_detected = any(
        phrase in text for phrase in ("assuming", "cautiously", "visibility")
    )

    if "confident" in text or "approved" in text:
        sentiment = "confident"
    elif hedging_detected:
        sentiment = "cautious"
    else:
        sentiment = "neutral"

    return {
        "risk_flags": risk_flags,
        "hedging_detected": hedging_detected,
        "sentiment": sentiment,
    }


def _validate_output(value):
    """Validate optional LLM JSON against the required schema."""
    if not isinstance(value, dict):
        raise ValueError("Output must be a JSON object.")

    if set(value.keys()) != {"risk_flags", "hedging_detected", "sentiment"}:
        raise ValueError("Output schema mismatch.")

    if (
        not isinstance(value["risk_flags"], list)
        or not all(isinstance(item, str) for item in value["risk_flags"])
    ):
        raise ValueError("risk_flags must be a list of strings.")

    if not isinstance(value["hedging_detected"], bool):
        raise ValueError("hedging_detected must be boolean.")

    if value["sentiment"] not in {"confident", "cautious", "neutral"}:
        raise ValueError("Invalid sentiment.")

    return value


def extract_signals_optional_llm(snippet: str) -> dict:
    """
    Optional MOCK_LLM=0 extension.

    An LLM integration can be inserted here. Its JSON output must be
    validated with _validate_output(), retried once on validation failure,
    and then fall back to extract_signals(snippet).
    """
    mock_result = extract_signals(snippet)

    if os.getenv("MOCK_LLM", "1") != "0":
        return mock_result

    # Baseline has no external LLM dependency, so safely fall back.
    return mock_result


if __name__ == "__main__":
    from disclosure_snippets import DISCLOSURE_SNIPPETS

    for snippet in DISCLOSURE_SNIPPETS:
        print(snippet)
        print(extract_signals(snippet))
        print()
