from typing import Literal

from inspect_ai.solver import (
    Generate,
    Solver,
    TaskState,
    chain,
    generate,
    prompt_template,
    solver,
    system_message,
)

from prompts import get_system_prompt, get_prompt_template
from inspect_ai.tool import ToolFunction

@solver  
def set_tool_choice(choice: Literal["forced_first", "auto", "none"] = "auto") -> Solver:
    async def solve(state: TaskState, gen: Generate) -> TaskState:
        if choice == "forced_first":
            state.tool_choice = ToolFunction(name=state.metadata["tools_required"][0])
        elif choice == "auto":
            state.tool_choice = "auto"
        elif choice == "none":
            state.tool_choice = "none"
        return state
    return solve

@solver
def system_prompt_solver(
    system_prompt_template: str = "default",
    prompt_technique: Literal["standard", "cot", "react"] = "standard",
) -> Solver:
    """Apply system prompt to state."""
    async def solve(state: TaskState, gen: Generate) -> TaskState:
        system_prompt = get_system_prompt(system_prompt_template, prompt_technique)
        if system_prompt:
            state = await system_message(system_prompt)(state, gen)
        return state
    return solve


def default_agent(
    system_prompt_template: str = "default",
    prompt_technique: Literal["standard", "cot", "react"] = "standard",
) -> Solver:
    """Simple agent: system prompt + template + generate with tool loop."""
    return chain(
        system_prompt_solver(system_prompt_template, prompt_technique),
        prompt_template(get_prompt_template("empty")),
        set_tool_choice("auto"),
        generate(tool_calls="loop"),
    )