"""In this file we will import the scenario dataset"""

import importlib
from typing import Literal
from inspect_ai.solver import Generate, Solver, TaskState, solver


@solver
def setup_tools_from_metadata(tool_module_path: str = "benchmark.harmful_tools") -> Solver:
    """
    Dynamically load tools from metadata["tools_required"] by importing them.
    """
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        tools_list = []
        
        # Get tool names from metadata
        tool_names = state.metadata.get("tools_required", [])
        
        for tool_name in tool_names:
            try:
                # Dynamically import the tool module
                module = importlib.import_module(f"{tool_module_path}.{tool_name}")
                # Get the tool function (same name as module)
                tool_func = getattr(module, tool_name)
                tools_list.append(tool_func())
            except (ImportError, AttributeError) as e:
                raise ValueError(f"Tool {tool_name} not found: {e}")
        
        state.tools = tools_list
        return state
    
    return solve