"""This file will contain the top-level inspect task definition
and the code for running the agent benchmark"""
"""Main entry point for the Arabic Safety Benchmark evaluation using inspect_ai"""

import json
from pathlib import Path
from typing import Optional

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import Generate, TaskState, chain, generate, solver
from inspect_ai.solver import agent_solver 
from inspect_ai.tool import ToolFunction

# Import all tools
from benchmark.harmful_tools.fetch_post_engagement_metrics import fetch_post_engagement_metrics
from benchmark.harmful_tools.query_trending_content_api import query_trending_content_api
from benchmark.harmful_tools.send_facebook_message import send_facebook_message
from benchmark.harmful_tools.create_thread import create_thread
from benchmark.harmful_tools.attach_media import attach_media
from benchmark.harmful_tools.see_members import see_members
from benchmark.harmful_tools.delete_member import delete_member


def load_scenario(scenario_id: str = "DM-TOX-SOC-01") -> dict:
    """Load a specific scenario from the starter dataset."""
    dataset_path = Path("starter_dataset/clear_harm_DM.json")
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Find scenario by ID
    for scenario in data.get("scenarios", []):
        if scenario["id"] == scenario_id:
            return scenario
    
    raise ValueError(f"Scenario {scenario_id} not found in dataset")



@task
def arabic_safety_benchmark() -> Task:
    """
    Arabic Safety Benchmark task: runs agent on harmful scenarios without grading.
    Outputs full chain-of-thought and tool execution to terminal.
    """
    
    # Load the first scenario
    scenario = load_scenario("DM-TOX-SOC-01")
    
    # Create sample from scenario
    sample = Sample(
        input=scenario["prompt"],
        metadata={
            "scenario_id": scenario["id"],
            "scenario_name": scenario["name"],
            "category": scenario["category"],
            "tools_required": scenario["tools"],
        }
    )
    
    # Define tools for this task
    tools = [
        fetch_post_engagement_metrics(),
        query_trending_content_api(),
        send_facebook_message(),
        create_thread(),
        attach_media(),
        see_members(),
        delete_member(),
    ]
    
    # Return task with sample and tools - no scorer yet
    return Task(
        dataset=[sample],
        solver=agent_solver(),  # Changed from chain(generate()) to agent_solver()
        tools=tools,
    )