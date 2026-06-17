import importlib
from inspect_ai.solver import Generate, Solver, TaskState, solver
import benchmark.harmful_tools as harmful_tools_module


@solver
def setup_tools_from_metadata(tool_module_path: str = "benchmark.harmful_tools") -> Solver:
    """
    Load tools from metadata["tools_required"] using static module import.
    """
    # Import the module ONCE at solver-definition time, not inside the async function
    module = importlib.import_module(tool_module_path)

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        tools_list = []
        tool_names = state.metadata.get("tools_required", [])

        for tool_name in tool_names:
            tool_func = getattr(module, tool_name, None)
            if tool_func is None:
                raise ValueError(
                    f"Tool '{tool_name}' not found in module '{tool_module_path}'. "
                    f"Make sure the function is exported in benchmark/harmful_tools/__init__.py"
                )
            tools_list.append(tool_func())

        state.tools = tools_list
        return state

    return solve