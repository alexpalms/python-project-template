from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import AxesImage
from numpy.typing import NDArray


class TypedEnvironment:
    def __init__(self, env: Any):
        self.diambra_env = env
        self._render_mode = self.diambra_env.render_mode
        self._fig = None
        self._ax = None
        if self._render_mode == "rgb_array":
            self._fig, self._ax = plt.subplots(figsize=(6, 4))  # pyright: ignore[reportUnknownMemberType]
            self._im: AxesImage | None = None

    def reset(self) -> tuple[dict[str, Any], dict[str, Any]]:
        observation, info = self.diambra_env.reset()
        return observation, info

    def step(
        self, action: list[int]
    ) -> tuple[dict[str, Any], float, bool, bool, dict[str, Any]]:
        observation, reward, terminated, truncated, info = self.diambra_env.step(action)
        return observation, reward, terminated, truncated, info

    def render(self) -> None:
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
        self.diambra_env.close()
        if self._render_mode == "rgb_array":
            plt.close(self._fig)
