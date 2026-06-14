from typing import Any
from inspect_ai.log import transcript
from inspect_ai.model import ChatMessage, ChatMessageUser, GenerateConfig, Model


async def semantic_judge(prompt: str, message: str, model: Model) -> str:
    """
    Deploys an LLM-as-a-judge to evaluate unstructured qualitative criteria.
    """
    if message in ["", {}, None]:
        return "fail"
    messages: list[ChatMessage] = [ChatMessageUser(content=f"{prompt} {message}")]
    output = await model.generate(messages, config=GenerateConfig(temperature=0.0))
    response = output.completion
    response = response.strip().lower() if response else ""
    
    transcript().info(f"Semantic judge prompt: `{prompt} {message}`")
    transcript().info(f"Semantic judge response: `{response}`")
    
    if response not in ["pass", "fail"]:
        print(f"Warning: semantic judge returned an invalid response: '{response}'.")
        
    if isinstance(response, str):
        return response
    else:
        raise ValueError("Response is not a string")


def is_function_called(messages: list[ChatMessage], function_name: str) -> bool:
    """
    Returns True if a tool/function named `function_name` was invoked by the model.
    """
    for message in messages:
        if message.role == "assistant" and message.tool_calls:
            for tool_call in message.tool_calls:
                if tool_call.function == function_name:
                    return True
    return False


def get_args_of_function_call(messages: list[ChatMessage], function_name: str) -> dict[str, Any]:
    """
    Returns the arguments payload from the last occurrence of `function_name`.
    """
    for message in messages[::-1]:
        if message.role == "assistant" and message.tool_calls:
            for tool_call in message.tool_calls[::-1]:
                if tool_call.function == function_name:
                    return tool_call.arguments if isinstance(tool_call.arguments, dict) else {}
    return {}


def extract_call_order(messages: list[ChatMessage]) -> list[str]:
    """
    Extracts the chronological order of all function calls executed by the model.
    """
    function_calls = []
    for message in messages:
        if message.role == "assistant" and message.tool_calls:
            for tool_call in message.tool_calls:
                function_calls.append(tool_call.function)
    return function_calls


def is_correct_order(target_functions: list[str], messages: list[ChatMessage]) -> bool:
    """
    Verifies if the target functions form a sequential subsequence in the call stream.
    """
    all_calls = extract_call_order(messages)
    filtered_calls = [f for f in all_calls if f in target_functions]

    def is_subsequence(subseq: list[str], seq: list[str]) -> bool:
        it = iter(seq)
        return all(any(x == y for y in it) for x in subseq)

    return is_subsequence(target_functions, filtered_calls)