"""This file will contain the top-level inspect task definition
and the code for running the agent benchmark"""
"""Main entry point for the Arabic Safety Benchmark evaluation using inspect_ai"""

import json
from pathlib import Path
from typing import Optional

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import Generate, TaskState, chain, generate, solver 
from inspect_ai.tool import ToolFunction
from inspect_ai.model import GenerateConfig

from agents.agent import get_agent
from utils import setup_tools_from_metadata
from scorer import arabic_safety_scorer


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
    
    scenario = load_scenario("DM-TOX-SOC-01")
    
    sample = Sample(
        input=scenario["prompt"],
        metadata={
            "scenario_id": scenario["id"],
            "scenario_name": scenario["name"],
            "category": scenario["category"],
            "tools_required": scenario["tools"],
            "semantic_requirement": scenario["semantic_requirement"],
        }
    )
    
    agent_solver = get_agent(agent="default")
    
    # Create solver plan as list
    plan = [
        setup_tools_from_metadata("benchmark.harmful_tools"),
        agent_solver,
    ]
    
    return Task(
        dataset=[sample],
        solver=plan,
        scorer=arabic_safety_scorer(),
        config=GenerateConfig(
            max_retries=3,
            max_tokens=2048,
            temperature=0.0,
        ),
    )