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
        # action = {"item": "bread", "quantity": 5}
        item = action.get("item")
        quantity = action.get("quantity", 0)
        cost = quantity * 10

        reward = 0.0
        done = False
        info = {}

        if self.current_task == "easy":
            # Sirf check karo — item available hai?
            if self.stock.get(item, 0) > 0:
                reward = 1.0
            else:
                reward = 0.0
            done = True

        elif self.current_task == "medium":
            # Reorder karo agar demand zyada hai stock se
            if self.demand[item] > self.stock[item]:
                self.stock[item] += quantity
                reward = min(1.0, quantity / self.demand[item])
            else:
                reward = 0.2
            done = True

        elif self.current_task == "hard":
            # Budget mein rehke optimal order
            if cost <= self.budget:
                self.budget -= cost
                self.stock[item] += quantity
                fulfillment = min(self.stock[item] / self.demand[item], 1.0)
                budget_efficiency = self.budget / 100
                reward = round((fulfillment + budget_efficiency) / 2, 2)
            else:
                reward = 0.0
                info["error"] = "Budget exceeded!"
            done = True

        return self.state(), reward, done, info
