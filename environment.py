import random
from pydantic import BaseModel
from typing import Dict, Optional

class BakeryAction(BaseModel):
    item: str
    quantity: int

class BakeryObservation(BaseModel):
    stock: Dict[str, int]
    demand: Dict[str, int]
    budget: float
    task: str

class BakeryReward(BaseModel):
    reward: float
    done: bool
    info: Dict

class BakeryEnv:
    def __init__(self):
        self.items = ["bread", "croissant", "cake", "muffin", "cookie"]
        self.stock = {}
        self.budget = 0
        self.demand = {}
        self.current_task = None
        self.reset()

    def reset(self, task="easy"):
        self.current_task = task
        self.stock = {item: random.randint(0, 20) for item in self.items}
        self.demand = {item: random.randint(5, 15) for item in self.items}
        self.budget = 100
        return self.state()

    def state(self):
        return {
            "stock": self.stock,
            "demand": self.demand,
            "budget": self.budget,
            "task": self.current_task
        }

    def step(self, action):
    item = action.get("item")
    quantity = action.get("quantity", 0)
    cost = quantity * 10

    reward = 0.0
    done = False
    info = {}

    if self.current_task == "easy":
        if self.stock.get(item, 0) > 0:
            reward = 0.9  # 1.0 nahi!
        else:
            reward = 0.1  # 0.0 nahi!
        done = True

    elif self.current_task == "medium":
        if self.demand[item] > self.stock[item]:
            self.stock[item] += quantity
            reward = min(0.9, quantity / self.demand[item])
            reward = max(0.1, reward)  # 0.0 nahi!
        else:
            reward = 0.2
        done = True

    elif self.current_task == "hard":
        if cost <= self.budget:
            self.budget -= cost
            self.stock[item] += quantity
            fulfillment = min(self.stock[item] / self.demand[item], 0.9)
            budget_efficiency = self.budget / 100
            reward = round((fulfillment + budget_efficiency) / 2, 2)
            reward = max(0.1, min(0.9, reward))  # strictly between 0 and 1!
        else:
            reward = 0.1  # 0.0 nahi!
            info["error"] = "Budget exceeded!"
        done = True

    return self.state(), reward, done, info
