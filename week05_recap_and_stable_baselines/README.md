**Practice:**

Previous seminar notebook: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/girafe-ai/reinforcement-learning/blob/23f_msai/week04_approx_qlearning/seminar_pytorch.ipynb)

[Stable baselines 3](https://stable-baselines3.readthedocs.io/en/master/index.html) solution:

```
!pip install gymnasium
!pip install stable_baselines3

import gymnasium as gym
from stable_baselines3 import DQN

env = gym.make("CartPole-v1", render_mode="human")

model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000, log_interval=4)
model.save("dqn_cartpole")

# del model # remove to demonstrate saving and loading

# model = DQN.load("dqn_cartpole")

obs, info = env.reset()
while True:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()
```

[Stable baselines](https://stable-baselines3.readthedocs.io/en/master/index.html) DQN notebook: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Stable-Baselines-Team/rl-colab-notebooks/blob/sb3/dqn_sb3.ipynb)