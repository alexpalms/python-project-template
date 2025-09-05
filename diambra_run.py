#!/usr/bin/env python3
from pydantic import BaseModel

from vllm import LLM, SamplingParams
from vllm.sampling_params import GuidedDecodingParams

import diambra.arena
from diambra.arena import SpaceTypes, Roles, EnvironmentSettings
from diambra.arena.utils.gym_utils import available_games
import json
import argparse

from agents import RandomAgent
from agents import RandomAgentWithCustomMoves

MAX_TOKENS = 200

class PromptStructuredOutput(BaseModel):
    game_id: str
    characters: tuple[str, ...]

json_schema = PromptStructuredOutput.model_json_schema()
guided_decoding_params_json = GuidedDecodingParams(json=json_schema)
sampling_params_json = SamplingParams(
    guided_decoding=guided_decoding_params_json,
    max_tokens=MAX_TOKENS,
)

def user_chat(llm: LLM):

    game_data = available_games(False)
    game_details_list = []
    for k, v in game_data.items():
        game_details_entry = {
            "game_id": v["id"],
            "game_name": v["name"],
            "game_characters": [elem for elem in v["char_list"] if elem not in v["char_forbidden_list"]],
            "number_of_chars_to_select": v["number_of_chars_to_select"],
        }
        game_details_list.append(game_details_entry)
    game_details_list_str = ""
    for game_details_entry in game_details_list:
        game_details_list_str += json.dumps(game_details_entry) + "\n"


    prompt_json = (
        "From the following user defined text, generate a JSON with the fields:\n"
        "\"game_id\": game identifier\n"
        "\"characters\": the character(s) to be used in the game episode, the user is supposed to specify as many characters as specified in the \"number_of_chars_to_select\" field of the game details\n"
        "and then respond with the JSON. The following details provide context for each of the games:\n"
        f"{game_details_list_str}"
        "\n\n"
        "User defined text: "
    )


    user_input = input("Describe the game and the character(s) you want to use in your agent: ")

    outputs = llm.generate(prompt_json + user_input, sampling_params=sampling_params_json)
    prompt_structured_output = outputs[0].outputs[0].text

    return prompt_structured_output

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
        agent = RandomAgentWithCustomMoves(env, None)
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
            prompt_structured_output = json.loads(user_chat(llm))
        else:
            prompt_structured_output = {"game_id": "sfiii3n", "characters": ["Ryu"]}

        print("Environment settings: ", prompt_structured_output)
        run_diambra(args.agent_type, prompt_structured_output)
        continue_answer = input("New episode? (y/[n]): ")
        if continue_answer.lower() != "y":
            break

    if args.llm == "true":
        llm.close()