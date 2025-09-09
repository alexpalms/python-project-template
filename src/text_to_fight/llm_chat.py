"""LLM chat module."""

import json
from typing import Any

from diambra.arena.utils.gym_utils import (  # type: ignore[import-untyped]
    available_games,
)
from pydantic import BaseModel
from vllm import LLM, SamplingParams
from vllm.sampling_params import GuidedDecodingParams

MAX_TOKENS = 200


class GameAndCharacterSelection(BaseModel):
    """Model for the game and character selection."""

    game_id: str
    characters: tuple[str, ...]


def llm_generate(llm: LLM, prompt: str, output_model: type[BaseModel]) -> str:
    """Generate a response from the LLM.

    Args:
        llm: The LLM to use.
        prompt: The prompt to generate a response from.
        output_model: The model to use for the output.

    Returns:
        The response from the LLM.

    """
    json_schema = output_model.model_json_schema()
    guided_decoding_params_json = GuidedDecodingParams(json=json_schema)
    sampling_params_json = SamplingParams(
        guided_decoding=guided_decoding_params_json,
        max_tokens=MAX_TOKENS,
    )
    outputs = llm.generate(prompt, sampling_params=sampling_params_json)  # pyright: ignore[reportUnknownMemberType]
    prompt_structured_output = outputs[0].outputs[0].text
    return prompt_structured_output


def game_and_character_selection(llm: LLM) -> str:
    """Generate a response from the LLM for the game and character selection.

    Args:
        llm: The LLM to use.

    Returns:
        The response from the LLM.

    """
    game_data: Any = available_games(False)
    game_details_list: list[dict[str, Any]] = []
    for _, v in game_data.items():
        game_details_entry = {
            "game_id": v["id"],
            "game_name": v["name"],
            "game_characters": [
                elem for elem in v["char_list"] if elem not in v["char_forbidden_list"]
            ],
            "number_of_chars_to_select": v["number_of_chars_to_select"],
        }
        game_details_list.append(game_details_entry)
    game_details_list_str = ""
    for game_details_entry in game_details_list:
        game_details_list_str += json.dumps(game_details_entry) + "\n"

    prompt_json = (
        "From the following user defined text, generate a JSON with the fields:\n"
        '"game_id": game identifier\n'
        '"characters": the character(s) to be used in the game episode, the user is supposed to specify as many characters as specified in the "number_of_chars_to_select" field of the game details\n'
        "and then respond with the JSON. The following details provide context for each of the games:\n"
        f"{game_details_list_str}"
        "\n\n"
        "User defined text: "
    )

    user_input = input(
        "Describe the game and the character(s) you want to use in your agent: "
    )

    return llm_generate(llm, prompt_json + user_input, GameAndCharacterSelection)


class ActionsSelection(BaseModel):
    """Model for the actions selection."""

    custom_actions: list[list[str]]


def actions_selection(llm: LLM, game_id: str) -> str:
    """Generate a response from the LLM for the actions selection.

    Args:
        llm: The LLM to use.
        game_id: The game ID.

    Returns:
        The response from the LLM.

    """
    # Load actions mapping from JSON file
    # local_dir = os.path.dirname(os.path.abspath(__file__))
    # actions_mapping_path = os.path.join(local_dir, "actions_mapping.json")
    # assert os.path.exists(actions_mapping_path), (
    #    f"Actions mapping file not found: {actions_mapping_path}"
    # )
    #
    # with open(actions_mapping_path) as f:
    #    actions_mapping = json.load(f)
    #
    # game_data = available_games(False)
    # game_details_list = []
    # for _, v in game_data.items():
    #    game_details_entry = {
    #        "game_id": v["id"],
    #        "game_name": v["name"],
    #        "game_characters": [
    #            elem for elem in v["char_list"] if elem not in v["char_forbidden_list"]
    #        ],
    #        "number_of_chars_to_select": v["number_of_chars_to_select"],
    #    }
    #    game_details_list.append(game_details_entry)
    # game_details_list_str = ""
    # for game_details_entry in game_details_list:
    #    game_details_list_str += json.dumps(game_details_entry) + "\n"
    #
    # prompt_json = (
    #    'From the following user defined text, generate a JSON with a field named "custom_actions", containing a list of lists of strings, each list of strings representing a custom action and then respond with the JSON. The following details provide context for each of the games:\n'
    #    f"{game_details_list_str}"
    #    "\n\n"
    #    "User defined text: "
    # )
    #
    # user_input = input(
    #    "Describe the game and the character(s) you want to use in your agent: "
    # )
    #
    # return llm_generate(llm, prompt_json + user_input, ActionsSelection)

    return "test"
