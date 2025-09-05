from pydantic import BaseModel

from vllm import LLM, SamplingParams
from vllm.sampling_params import GuidedDecodingParams

from diambra.arena.utils.gym_utils import available_games

import json

MAX_TOKENS = 200

class GameAndCharacterSelection(BaseModel):
    game_id: str
    characters: tuple[str, ...]

def llm_generate(llm: LLM, prompt: str, output_model: BaseModel):
    json_schema = output_model.model_json_schema()
    guided_decoding_params_json = GuidedDecodingParams(json=json_schema)
    sampling_params_json = SamplingParams(
        guided_decoding=guided_decoding_params_json,
        max_tokens=MAX_TOKENS,
    )
    outputs = llm.generate(prompt, sampling_params=sampling_params_json)
    prompt_structured_output = outputs[0].outputs[0].text
    return prompt_structured_output

def game_and_character_selection(llm: LLM):

    game_data = available_games(False)
    game_details_list = []
    for _, v in game_data.items():
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

    return llm_generate(llm, prompt_json + user_input, GameAndCharacterSelection)

class ActionsSelectionOutput(BaseModel):
    game_id: str
    characters: tuple[str, ...]

def actions_selection(llm: LLM):

    #game_data = available_games(False)
    #game_details_list = []
    #for _, v in game_data.items():
    #    game_details_entry = {
    #        "game_id": v["id"],
    #        "game_name": v["name"],
    #        "game_characters": [elem for elem in v["char_list"] if elem not in v["char_forbidden_list"]],
    #        "number_of_chars_to_select": v["number_of_chars_to_select"],
    #    }
    #    game_details_list.append(game_details_entry)
    #game_details_list_str = ""
    #for game_details_entry in game_details_list:
    #    game_details_list_str += json.dumps(game_details_entry) + "\n"
#
#
    #prompt_json = (
    #    "From the following user defined text, generate a JSON with the fields:\n"
    #    "\"game_id\": game identifier\n"
    #    "\"characters\": the character(s) to be used in the game episode, the user is supposed to specify as many characters as specified in the \"number_of_chars_to_select\" field of the game details\n"
    #    "and then respond with the JSON. The following details provide context for each of the games:\n"
    #    f"{game_details_list_str}"
    #    "\n\n"
    #    "User defined text: "
    #)
#
#
    #user_input = input("Describe the game and the character(s) you want to use in your agent: ")
#
    #outputs = llm.generate(prompt_json + user_input, sampling_params=sampling_params_json)
    #prompt_structured_output = outputs[0].outputs[0].text

    return llm_generate(llm, prompt_json + user_input, GameAndCharacterSelectionOutput)