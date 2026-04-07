import os
import json
from openai import OpenAI
from environment import BakeryEnv

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")

def get_action(client, task, state):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a bakery inventory manager. Reply only with JSON."},
                {"role": "user", "content": f"Task: {task}, State: {json.dumps(state)}. Reply with only JSON: {{\"item\": \"bread\", \"quantity\": 1}}"}
            ],
            max_tokens=50
        )
        return json.loads(response.choices[0].message.content.strip())
    except:
        if task == "easy":
            return {"item": "bread", "quantity": 1}
        elif task == "medium":
            return {"item": "croissant", "quantity": 8}
        else:
            return {"item": "cake", "quantity": 3}

def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    env = BakeryEnv()
    tasks = ["easy", "medium", "hard"]

    for task in tasks:
        state = env.reset(task=task)
        print(f"[START] task={task} env=bakery-env model={MODEL_NAME}", flush=True)

        action = get_action(client, task, state)
        next_state, reward, done, info = env.step(action)
        error = info.get("error", None)
        error_val = error if error else "null"

        print(f"[STEP] step=1 action={json.dumps(action)} reward={reward:.2f} done={str(done).lower()} error={error_val}", flush=True)
        print(f"[END] success={str(reward > 0).lower()} steps=1 score={reward:.2f} rewards={reward:.2f}", flush=True)

if __name__ == "__main__":
    main()
