# tests/test_agents.py
"""Test the agents module."""

from gymnasium.spaces import MultiDiscrete

from text_to_fight.agents import RandomAgent
from text_to_fight.utils import TypedEnvironment


class DummyEnv:
    """Dummy environment."""

    action_space = MultiDiscrete([2, 2])
    render_mode = None


def test_random_agent() -> None:
    """Test the random agent."""
    env = TypedEnvironment(DummyEnv())
    agent = RandomAgent(env)
    action = agent.get_action({})
    assert action[0] in [0, 1] and action[1] in [0, 1]  # noqa: S101
