SKILLS = {
    "analyze": "Inspect the input and identify notable issues or patterns.",
    "summarize": "Compress the situation into a concise takeaway.",
    "rewrite": "Suggest a clearer or safer revision.",
    "evaluate_risk": "Point out likely failure modes or impact.",
    "suggest_strategy": "Recommend a practical next step or plan.",
    "identify_tradeoffs": "Highlight benefits, costs, or tensions.",
}


def get_skill_description(name: str) -> str:
    try:
        return SKILLS[name]
    except KeyError as exc:
        raise ValueError(f"Unknown skill: {name}") from exc


def get_skill_descriptions(names: list[str]) -> list[str]:
    return [get_skill_description(name) for name in names]
