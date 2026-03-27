from typing import Any

from bioagents.core.task import Task


def _board_summary(board: Any) -> str:
    hypotheses = board.get_all()
    if not hypotheses:
        return "none"
    return "; ".join(hypothesis.text for hypothesis in hypotheses[:3])


def _objective_line(task: Task) -> str:
    return f"Objective: {task.objective}\n" if task.objective else ""


def _skills_line(skills: list[str], descriptions: list[str]) -> str:
    if not skills:
        return "Skills: none\n"
    skill_items = ", ".join(f"{name} ({description})" for name, description in zip(skills, descriptions))
    return f"Skills: {skill_items}\n"


def _instruction(text: str) -> str:
    return (
        f"{text} Focus on the objective if provided. "
        "Return exactly one short plain sentence. No markdown, bullets, code, explanation, or quotes."
    )


def build_bug_prompt(
    task: Task,
    board: Any,
    skills: list[str],
    descriptions: list[str],
) -> str:
    return (
        f"Task type: {task.task_type}\n"
        f"Title: {task.title or ''}\n"
        f"{_objective_line(task)}"
        f"Input: {task.data}\n"
        f"Board: {_board_summary(board)}\n"
        f"{_skills_line(skills, descriptions)}"
        f"{_instruction('Identify one likely bug or failure mode.')}"
    )


def build_performance_prompt(
    task: Task,
    board: Any,
    skills: list[str],
    descriptions: list[str],
) -> str:
    return (
        f"Task type: {task.task_type}\n"
        f"Title: {task.title or ''}\n"
        f"{_objective_line(task)}"
        f"Input: {task.data}\n"
        f"Board: {_board_summary(board)}\n"
        f"{_skills_line(skills, descriptions)}"
        f"{_instruction('Identify one likely performance concern.')}"
    )


def build_solution_prompt(
    task: Task,
    board: Any,
    skills: list[str],
    descriptions: list[str],
) -> str:
    return (
        f"Task type: {task.task_type}\n"
        f"Title: {task.title or ''}\n"
        f"{_objective_line(task)}"
        f"Input: {task.data}\n"
        f"Board: {_board_summary(board)}\n"
        f"{_skills_line(skills, descriptions)}"
        f"{_instruction('Propose one concrete fix or improvement.')}"
    )


def build_strategy_prompt(
    task: Task,
    board: Any,
    skills: list[str],
    descriptions: list[str],
) -> str:
    return (
        f"Task type: {task.task_type}\n"
        f"Title: {task.title or ''}\n"
        f"{_objective_line(task)}"
        f"Input: {task.data}\n"
        f"Board: {_board_summary(board)}\n"
        f"{_skills_line(skills, descriptions)}"
        f"{_instruction('Propose one higher-level next action or strategy.')}"
    )


def build_critic_prompt(
    task: Task,
    board: Any,
    skills: list[str],
    descriptions: list[str],
) -> str:
    return (
        f"Task type: {task.task_type}\n"
        f"Title: {task.title or ''}\n"
        f"{_objective_line(task)}"
        f"Input: {task.data}\n"
        f"Board: {_board_summary(board)}\n"
        f"{_skills_line(skills, descriptions)}"
        f"{_instruction('Identify one important tradeoff or concern.')}"
    )
