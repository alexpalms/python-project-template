"""Utils module."""

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import AxesImage
from numpy.typing import NDArray


class TypedEnvironment:
    """Environment that selects actions."""

    def __init__(self, env: Any):
        """Initialize the environment.

        Args:
            env: The environment to use.

        """
        self.diambra_env = env
        self._render_mode = self.diambra_env.render_mode
        self._fig = None
        self._ax = None
        if self._render_mode == "rgb_array":
            self._fig, self._ax = plt.subplots(figsize=(6, 4))  # pyright: ignore[reportUnknownMemberType]
            self._im: AxesImage | None = None

    def reset(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """Reset the environment.

        Returns:
            The observation and info.

        """
        observation, info = self.diambra_env.reset()
        return observation, info

    def step(
        self, action: list[int]
    ) -> tuple[dict[str, Any], float, bool, bool, dict[str, Any]]:
        """Step the environment.

        Args:
            action: The action to execute.

        Returns:
            The observation, reward, terminated, truncated, and info.

        """
        observation, reward, terminated, truncated, info = self.diambra_env.step(action)
        return observation, reward, terminated, truncated, info

    def render(self) -> None:
        """Render the environment."""
        if self._render_mode == "rgb_array":
            frame: NDArray[np.int_] = self.diambra_env.render()
            if self._ax is None:
                raise ValueError("self._ax is None")
            if self._im is None:
                # First time: create the image
                self._im = self._ax.imshow(frame)  # pyright: ignore[reportUnknownMemberType]
                self._ax.axis("off")
            else:
                # Update existing image
                self._im.set_data(frame)

            plt.pause(0.001)

    def close(self) -> None:
        """Close the environment."""
        self.diambra_env.close()
        if self._render_mode == "rgb_array":
            plt.close(self._fig)
