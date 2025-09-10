"""Agents module."""

import json
import random
from abc import abstractmethod
from importlib import resources
from typing import Any

from diambra.arena import Roles  # type: ignore[import-untyped]

from text_to_fight.utils import TypedEnvironment


class Agent:
    """Agent that selects actions."""

    @abstractmethod
    def __init__(self, env: TypedEnvironment) -> None:
        """Initialize the agent.

        Args:
            env: The environment to use.

        """
        raise NotImplementedError

    @abstractmethod
    def get_action(self, observation: dict[str, Any]) -> list[int]:
        """Get an action from the agent.

        Args:
            observation: The observation from the environment.

        Returns:
            The action to execute.

        """
        raise NotImplementedError


class RandomAgent(Agent):
    """Agent that selects random actions."""

    def __init__(self, env: TypedEnvironment):
        """Initialize the agent.

        Args:
            env: The environment to use.

        """
        self.env = env.diambra_env

    def get_action(self, observation: dict[str, Any]) -> list[int]:
        """Get an action from the agent.

        Args:
            observation: The observation from the environment.

        Returns:
            The action to execute.

        """
        actions: list[int] = self.env.action_space.sample()
        return actions


class RandomAgentWithCustomActions(Agent):
    """Agent that selects actions from a list of custom actions."""

    def __init__(self, env: TypedEnvironment, custom_actions: list[list[str]]):
        """Initialize the agent.

        Args:
            env: The environment to use.
            custom_actions: The list of custom actions to use.

        """
        self.env = env.diambra_env
        try:
            with (
                resources.files("text_to_fight.data")
                .joinpath("actions_mapping.json")
                .open() as f
            ):
                self.actions_mapping = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Actions mapping file not found") from None

        self.actions: list[list[list[list[int]]]] = [[], []]
        moves_p1 = self.actions_mapping["all"]["moves_p1"]
        moves_p2 = self.actions_mapping["all"]["moves_p2"]
        attacks = self.actions_mapping[self.env.env_settings.game_id]["attacks"]
        for custom_action in custom_actions:
            new_action_p1: list[list[int]] = [[], []]
            new_action_p2: list[list[int]] = [[], []]
            for action_item in custom_action:
                if "+" in action_item:
                    action = action_item.split("+")
                    if not (action[0] in moves_p1 and action[1] in attacks):
                        raise ValueError(f"The custom action {action} is not valid")
                    action_p1 = [moves_p1.index(action[0]), attacks.index(action[1])]
                    action_p2 = [moves_p2.index(action[0]), attacks.index(action[1])]
                else:
                    if action_item in moves_p1:
                        action_p1 = [moves_p1.index(action_item), 0]
                        action_p2 = [moves_p2.index(action_item), 0]
                    elif action_item in attacks:
                        action_p1 = [0, attacks.index(action_item)]
                        action_p2 = [0, attacks.index(action_item)]
                    else:
                        raise ValueError(
                            f"The custom action {action_item} is not valid"
                        )
                new_action_p1[0].append(action_p1[0])
                new_action_p1[1].append(action_p1[1])
                new_action_p2[0].append(action_p2[0])
                new_action_p2[1].append(action_p2[1])
            self.actions[0].append(new_action_p1)
            self.actions[1].append(new_action_p2)

        for i in range(2):
            for side_action_item in self.actions[i]:
                if len(side_action_item[0]) != len(side_action_item[1]):
                    raise ValueError(
                        "The number of moves and the attacks must be the same"
                    )

        self.executing_action = False
        self.execution_idx = 0
        self.selected_action = [[0], [0]]

    def get_action(self, observation: dict[str, Any]) -> list[int]:
        """Get an action from the agent.

        Args:
            observation: The observation from the environment.

        Returns:
            The action to execute.

        """
        role_name = Roles.Name(
            self.env.env_settings.pb_model.episode_settings.player_settings[0].role
        )
        action_to_execute = [0, 0]
        side: int = observation[role_name]["side"]
        if not self.executing_action:
            # Randomly select an action from the list of actions
            self.selected_action = self.actions[side][
                random.randint(0, len(self.actions[side]) - 1)  # noqa: S311
            ]

            if len(self.selected_action[0]) > 1:
                self.executing_action = True
            action_to_execute = [
                self.selected_action[0][self.execution_idx],
                self.selected_action[1][self.execution_idx],
            ]
        else:
            self.execution_idx += 1
            action_to_execute = [
                self.selected_action[0][self.execution_idx],
                self.selected_action[1][self.execution_idx],
            ]
            if self.execution_idx == (len(self.selected_action[0]) - 1):
                self.executing_action = False
                self.execution_idx = 0

        return action_to_execute
