# FrozenLake Q-Learning Agent

## Objective
Train a reinforcement learning agent using the **Q-learning algorithm** to navigate the **FrozenLake** environment and reach the goal (`G`) while avoiding holes (`H`).

## Environment Description

The **FrozenLake-v1** environment from **OpenAI Gym** simulates a 4x4 icy grid world:
- `S` — Starting point (safe)
- `F` — Frozen surface (safe)
- `H` — Hole (danger — episode ends)
- `G` — Goal (reward = 1)

The agent can move **up**, **down**, **left**, or **right**.  
The objective is to reach the goal while avoiding holes.

## Environment Variants

| Parameter | Description | Behavior | Typical Success Rate |
|------------|--------------|-----------|----------------------|
| `is_slippery=False` | Deterministic | The agent moves exactly as intended | ✅ ~100% |
| `is_slippery=True` | Stochastic (slippery ice) | The agent may slip in random directions | ⚠️ ~50–70% |

```python
# Example:
env = gym.make("FrozenLake-v1", is_slippery=True, render_mode="ansi")
```

## Q-Learning Algorithm

Q-learning is a model-free **reinforcement learning** algorithm that learns the optimal policy through trial and error.

### Q-Value Update Rule:
\[
Q(s, a) \leftarrow Q(s, a) + \alpha [r + \gamma \max_a Q(s', a) - Q(s, a)]
\]

Where:
- **α (alpha)**: Learning rate  
- **γ (gamma)**: Discount factor  
- **ε (epsilon)**: Exploration rate for epsilon-greedy policy  

---

## Hyperparameters

| Parameter | Value |
|------------|--------|
| Learning rate (α) | 0.9 |
| Discount factor (γ) | 0.95 |
| Exploration rate (ε) | 1.0 → 0.01 (decayed) |
| Episodes | 10,000 |
| Max steps per episode | 100 |

---

## Training Process

1. Initialize the Q-table with zeros.
2. For each episode:
   - Start from the initial state.
   - Choose an action using an **epsilon-greedy** policy.
   - Observe the next state and reward.
   - Update the Q-table using the Q-learning update rule.
3. Gradually decrease **epsilon** to reduce exploration.

Training progress is logged every 1000 episodes and displayed in a scrollable output cell.

---

## Evaluation

After training, the agent is evaluated over 20 episodes without exploration.  
The following metrics are computed:

- **Success rate** — % of episodes where the goal was reached  
- **Average steps** — mean number of steps per episode  
- **Average reward** — mean reward per episode  

### Sample Results

#### `is_slippery=False`
```
Success rate: 100.00%
Average steps per episode: 6.00
Average reward per episode: 1.00
```

#### `is_slippery=True`
```
Success rate: 55–70%
Average steps per episode: 40–60
Average reward per episode: 0.55–0.70
```

---

## Conclusion

- **`is_slippery=False`** → Deterministic world, perfect control, **100% success**.  
- **`is_slippery=True`** → Stochastic world, random slips, **lower success (50–70%)**.  

> Deterministic environments are great for verifying algorithm correctness,  
> while slippery ones better reflect real-world uncertainty and robustness testing.

---

## Requirements

- Python ≥ 3.8  
- `gymnasium` or `gym`  
- `numpy`  
- `IPython` (for scrollable outputs in notebooks)

Install dependencies:
```bash
pip install gymnasium numpy ipython
```

---

## 📁 Project Structure
```
FrozenLake_Q_Learning/
│
├── FrozenLake_Q_Learning.ipynb   # Jupyter notebook (training + evaluation)
├── README.md                     # Project documentation
└── requirements.txt              # (optional) dependencies list
```

---

## Lamia Rahmani
Developed with ❤️ using **Q-learning** and **OpenAI Gym**.
