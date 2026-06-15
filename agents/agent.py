from typing import Any, Callable

from inspect_ai.solver import Solver

from agents.default_agent import default_agent

AGENT_DICT: dict[str, Callable[..., Solver]] = {
    "default": default_agent,
}


def get_agent(agent: str = "default", **kwargs: Any) -> Solver:
    """Get agent solver by name."""
    if agent in AGENT_DICT:
        return AGENT_DICT[agent](**kwargs)
    else:
        raise ValueError(f"Invalid agent: {agent}. Available: {list(AGENT_DICT.keys())}")