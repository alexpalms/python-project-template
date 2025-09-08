#!/usr/bin/env python3
from text_to_fight.llm_chat import game_and_character_selection

from vllm import LLM
from typing import Optional

import diambra.arena # type: ignore[import-untyped]
from diambra.arena import SpaceTypes, Roles, EnvironmentSettings

import json
import argparse
from typing import Any

from text_to_fight.utils import TypedEnvironment

from text_to_fight.agents import RandomAgent, Agent
from text_to_fight.agents import RandomAgentWithCustomActions

def run_diambra(agent_type: str, game_id_and_character_selection_config: dict[str, Any]) -> None:
    game_id = game_id_and_character_selection_config["game_id"]
    characters = game_id_and_character_selection_config["characters"]

    # Settings
    settings = EnvironmentSettings()
    settings.step_ratio = 6
    settings.role = Roles.P1 # pyright: ignore
    settings.characters = characters
    settings.action_space = SpaceTypes.MULTI_DISCRETE # pyright: ignore

    env = TypedEnvironment(diambra.arena.make(game_id, settings, render_mode="rgb_array")) # pyright: ignore

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
        print("Action: ", action)
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
    llm: Optional[LLM] = None
    if args.llm == "true":
        llm = LLM(model="unsloth/Llama-3.2-3B-Instruct-bnb-4bit", max_model_len=2000, gpu_memory_utilization=0.7)

    while True:
        if llm is not None:
            prompt_structured_output = json.loads(game_and_character_selection(llm))
        else:
            prompt_structured_output = {"game_id": "sfiii3n", "characters": ["Ryu"]}

        print("Environment settings: ", prompt_structured_output)
        run_diambra(args.agent_type, prompt_structured_output)
        continue_answer = input("New episode? (y/[n]): ")
        if continue_answer.lower() != "y":
            break