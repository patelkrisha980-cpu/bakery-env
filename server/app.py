from fastapi import FastAPI
from environment import BakeryEnv
import uvicorn

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
    return {"state": state, "reward": reward, "done": done, "info": info}

@app.get("/state")
def state():
    return env.state()

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
