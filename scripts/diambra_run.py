#!/usr/bin/env python3
"""Diambra run script."""

import argparse
import json
import logging
from typing import Any

import diambra.arena  # type: ignore[import-untyped]
from diambra.arena import EnvironmentSettings, Roles, SpaceTypes
from vllm import LLM

from text_to_fight.agents import Agent, RandomAgent, RandomAgentWithCustomActions
from text_to_fight.llm_chat import game_and_character_selection
from text_to_fight.utils import TypedEnvironment

logging.basicConfig(level=logging.INFO)


def run_diambra(
    agent_type: str,
    game_id_and_character_selection_config: dict[str, Any],
) -> None:
    """Run the Diambra environment.

    Args:
        agent_type: The type of agent to use.
        game_id_and_character_selection_config: The game ID and character selection configuration.

    """
    game_id = game_id_and_character_selection_config["game_id"]
    characters = game_id_and_character_selection_config["characters"]

    # Settings
    settings = EnvironmentSettings()
    settings.step_ratio = 6
    settings.role = Roles.P1  # pyright: ignore
    settings.characters = characters
    settings.action_space = SpaceTypes.MULTI_DISCRETE  # pyright: ignore

    env = TypedEnvironment(
        diambra.arena.make(game_id, settings, render_mode="rgb_array"),  # pyright: ignore
    )

    agent: Agent
    if agent_type == "random":
        agent = RandomAgent(env)
    elif agent_type == "random_with_custom_moves":
        custom_actions = [["D", "F-D", "F+MP"]]
        agent = RandomAgentWithCustomActions(env, custom_actions)
    else:
        raise ValueError(f"Invalid agent type: {agent_type}")
    observation, _ = env.reset()

    while True:
        env.render()
        action = agent.get_action(observation)
        logging.info("Action: %s", action)
        observation, _, terminated, truncated, _ = env.step(action)

        if terminated or truncated:
            observation, _ = env.reset()
            break

    # Close the environment
    env.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-type", type=str, default="random")
    parser.add_argument("--llm", type=str, default="false")
    args = parser.parse_args()

    # Initialize the LLM
    llm: LLM | None = None
    if args.llm == "true":
        llm = LLM(
            model="unsloth/Llama-3.2-3B-Instruct-bnb-4bit",
            max_model_len=2000,
            gpu_memory_utilization=0.7,
        )

    while True:
        if llm is not None:
            prompt_structured_output = json.loads(game_and_character_selection(llm))
        else:
            prompt_structured_output = {"game_id": "sfiii3n", "characters": ["Ryu"]}

        logging.info("Environment settings: %s", prompt_structured_output)
        run_diambra(args.agent_type, prompt_structured_output)
        continue_answer = input("New episode? (y/[n]): ")
        if continue_answer.lower() != "y":
            break
