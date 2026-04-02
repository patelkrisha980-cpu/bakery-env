import os
import json
from openai import OpenAI
from environment import BakeryEnv

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

def main():
    env = BakeryEnv()
    tasks = ["easy", "medium", "hard"]

    for task in tasks:
        state = env.reset(task=task)
        print(f"[START] task={task} env=bakery-env model={MODEL_NAME}")

        if task == "easy":
            action = {"item": "bread", "quantity": 1}
        elif task == "medium":
            action = {"item": "croissant", "quantity": 8}
        else:
            action = {"item": "cake", "quantity": 3}

        next_state, reward, done, info = env.step(action)
        error = info.get("error", None)
        error_val = error if error else "null"

        print(f"[STEP] step=1 action={json.dumps(action)} reward={reward:.2f} done={str(done).lower()} error={error_val}")
        print(f"[END] success={str(reward > 0).lower()} steps=1 rewards={reward:.2f}")

if __name__ == "__main__":
    main()
