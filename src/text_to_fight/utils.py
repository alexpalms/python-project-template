from typing import Any, Tuple

class TypedEnvironment:
    def __init__(self, env: Any):
        self._env = env

    def reset(self) -> Tuple[dict[str, Any], dict[str, Any]]:
        observation, info = self._env.reset()
        return observation, info

    def step(self, action: Any) -> Tuple[dict[str, Any], float, bool, bool, dict[str, Any]]:
        observation, reward, terminated, truncated, info = self._env.step(action)
        return observation, reward, terminated, truncated, info

    def render(self) -> None:
        self._env.render()

    def close(self) -> None:
        self._env.close()