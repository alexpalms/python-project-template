#!/usr/bin/env python3
from enum import Enum

from pydantic import BaseModel

from vllm import LLM, SamplingParams
from vllm.sampling_params import GuidedDecodingParams

import diambra.arena
from diambra.arena import SpaceTypes, Roles, EnvironmentSettings
from diambra.arena.utils.gym_utils import available_games
import json

MAX_TOKENS = 200

class PromptStructuredOutput(BaseModel):
    game_id: str
    characters: str


json_schema = PromptStructuredOutput.model_json_schema()
guided_decoding_params_json = GuidedDecodingParams(json=json_schema)
sampling_params_json = SamplingParams(
    guided_decoding=guided_decoding_params_json,
    max_tokens=MAX_TOKENS,
)
prompt_json = (
    "From the following user defined text, generate a JSON with the game_id and character to be used in the diambra environment, and then respond with the JSON. Consider the following mapping between game name and game_id:\n"
    "Dead or alive -> doapp\n"
    "Street fighter -> sfiii3n\n"
    "Tekken -> tektagt\n"
    "Mortal kombat -> umk3\n"
    "Samurai showdown -> samsh5sp\n"
    "King of fighter -> kof98umh\n"
    "Marvel VS Capcom -> mvsc\n"
    "X-Men VS Street Fighter -> xmvsf\n"
    "Soul Calibur -> soulclbr\n"
    "\nCharacter names are always with the first letter capitalized, and no leading or trailing spaces.\n"
    "User defined text: "
)

def generate_output(prompt: str, sampling_params: SamplingParams, llm: LLM):
    outputs = llm.generate(prompt, sampling_params=sampling_params)
    return outputs[0].outputs[0].text

def user_chat(llm: LLM):
    user_input = input("Describe the game id and the character you want to use in your agent: ")
    prompt_structured_output = generate_output(prompt_json + user_input, sampling_params_json, llm)

    return prompt_structured_output

def run_diambra_random_agent(prompt_structured_output: PromptStructuredOutput):
    game_id = prompt_structured_output["game_id"]
    characters = prompt_structured_output["characters"].strip()

    # Settings
    settings = EnvironmentSettings()
    settings.step_ratio = 6
    settings.role = Roles.P1
    settings.characters = characters
    settings.action_space = SpaceTypes.MULTI_DISCRETE

    env = diambra.arena.make(game_id, settings)
    observation, info = env.reset()

    while True:
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            observation, info = env.reset()
            break

    # Close the environment
    env.close()

    # Return success
    return 0

if __name__ == "__main__":
    # Initialize the LLM
    llm = LLM(model="unsloth/Llama-3.2-3B-Instruct-bnb-4bit", max_model_len=200, gpu_memory_utilization=0.7)

    prompt_structured_output = json.loads(user_chat(llm))
    print("Prompt decoded settings: ", prompt_structured_output)
    run_diambra_random_agent(prompt_structured_output)