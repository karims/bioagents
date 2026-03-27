from typing import Any

from bioagents.core.task import Task


def _board_summary(board: Any) -> str:
    hypotheses = board.get_all()
    if not hypotheses:
        return "none"
    return "; ".join(hypothesis.text for hypothesis in hypotheses[:3])


def build_bug_prompt(task: Task, board: Any) -> str:
    return (
        f"Task type: {task.task_type}\n"
        f"Title: {task.title or ''}\n"
        f"Input: {task.data}\n"
        f"Board: {_board_summary(board)}\n"
        "Return exactly one short plain sentence about a possible bug. No markdown, bullets, code, explanation, or quotes."
    )


def build_performance_prompt(task: Task, board: Any) -> str:
    return (
        f"Task type: {task.task_type}\n"
        f"Title: {task.title or ''}\n"
        f"Input: {task.data}\n"
        f"Board: {_board_summary(board)}\n"
        "Return exactly one short plain sentence about a performance concern. No markdown, bullets, code, explanation, or quotes."
    )


def build_critic_prompt(task: Task, board: Any) -> str:
    return (
        f"Task type: {task.task_type}\n"
        f"Title: {task.title or ''}\n"
        f"Input: {task.data}\n"
        f"Board: {_board_summary(board)}\n"
        "Return exactly one short plain sentence critique. No markdown, bullets, code, explanation, or quotes."
    )
