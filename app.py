from fastapi import FastAPI
from environment import BakeryEnv

app = FastAPI()
env = BakeryEnv()

@app.get("/")
def home():
    return {"status": "ok", "env": "BakeryInventoryEnv"}

@app.post("/reset")
def reset(task: str = "easy"):
    state = env.reset(task=task)
    return state

@app.post("/step")
def step(item: str, quantity: int):
    action = {"item": item, "quantity": quantity}
    state, reward, done, info = env.step(action)
    return {
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()