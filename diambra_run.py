#!/usr/bin/env python3
from llm_chat import game_and_character_selection
from llm_chat import PromptStructuredOutput

from vllm import LLM

import diambra.arena
from diambra.arena import SpaceTypes, Roles, EnvironmentSettings

import json
import argparse

from agents import RandomAgent
from agents import RandomAgentWithCustomActions

def run_diambra(agent_type: str, prompt_structured_output: PromptStructuredOutput):
    game_id = prompt_structured_output["game_id"]
    characters = prompt_structured_output["characters"]

    # Settings
    settings = EnvironmentSettings()
    settings.step_ratio = 6
    settings.role = Roles.P1
    settings.characters = characters
    settings.action_space = SpaceTypes.MULTI_DISCRETE

    env = diambra.arena.make(game_id, settings, render_mode="human")
    if agent_type == "random":
        agent = RandomAgent(env)
    elif agent_type == "random_with_custom_moves":
        custom_actions = [["D", "F-D", "F+MP"]]
        agent = RandomAgentWithCustomActions(env, custom_actions)
    else:
        raise ValueError(f"Invalid agent type: {agent_type}")
    observation, info = env.reset()

    while True:
        env.render()
        action = agent.get_action()
        print("Action: ", action)
        observation, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            observation, info = env.reset()
            break

    # Close the environment
    env.close()

    # Return success
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-type", type=str, default="random")
    parser.add_argument("--llm", type=str, default="false")
    args = parser.parse_args()

    # Initialize the LLM
    if args.llm == "true":
        llm = LLM(model="unsloth/Llama-3.2-3B-Instruct-bnb-4bit", max_model_len=2000, gpu_memory_utilization=0.7)
    else:
        llm = None

    while True:
        if args.llm == "true":
            prompt_structured_output = json.loads(game_and_character_selection(llm))
        else:
            prompt_structured_output = {"game_id": "sfiii3n", "characters": ["Ryu"]}

        print("Environment settings: ", prompt_structured_output)
        run_diambra(args.agent_type, prompt_structured_output)
        continue_answer = input("New episode? (y/[n]): ")
        if continue_answer.lower() != "y":
            break

    if args.llm == "true":
        llm.close()