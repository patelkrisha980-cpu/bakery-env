import json
from environment import BakeryEnv

def run_inference():
    env = BakeryEnv()
    tasks = ["easy", "medium", "hard"]

    print("[START]")

    for task in tasks:
        state = env.reset(task=task)

        if task == "easy":
            action = {"item": "bread", "quantity": 1}
        elif task == "medium":
            action = {"item": "croissant", "quantity": 8}
        else:
            action = {"item": "cake", "quantity": 3}

        next_state, reward, done, info = env.step(action)

        print(json.dumps({
            "type": "[STEP]",
            "task": task,
            "action": action,
            "reward": reward,
            "done": done,
            "info": info
        }))

    print("[END]")

if __name__ == "__main__":
    run_inference()