from typing import Any


def _board_summary(board: Any) -> str:
    hypotheses = board.get_all()
    if not hypotheses:
        return "none"
    return "; ".join(hypothesis.text for hypothesis in hypotheses[:3])


def build_bug_prompt(context: dict[str, Any], board: Any) -> str:
    return (
        f"Task: {context.get('task', '')}\n"
        f"Input: {context.get('data', '')}\n"
        f"Board: {_board_summary(board)}\n"
        "Return exactly one short possible bug."
    )


def build_performance_prompt(context: dict[str, Any], board: Any) -> str:
    return (
        f"Task: {context.get('task', '')}\n"
        f"Input: {context.get('data', '')}\n"
        f"Board: {_board_summary(board)}\n"
        "Return exactly one short performance concern."
    )


def build_critic_prompt(context: dict[str, Any], board: Any) -> str:
    return (
        f"Task: {context.get('task', '')}\n"
        f"Input: {context.get('data', '')}\n"
        f"Board: {_board_summary(board)}\n"
        "Return exactly one short critique."
    )
