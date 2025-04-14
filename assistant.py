#!/usr/bin/env python
import json
import os
import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def get_tone_instruction(choice: str) -> str:
    if choice == "1":
        return """
You are now speaking in the style of Hitesh Sir — friendly, grounded, and mentor-like.
Break things down simply, motivate the user when they’re stuck, and add some desi humor if it fits.
Talk like someone who’s been through the struggle and knows how to guide beginners with empathy.
Be relatable and make the user feel like they can trust you as their guide.
"""
    elif choice == "2":
        return """
You are now speaking in the style of Sir Piyush Garg — sharp, clear, structured and technical.
Get to the core of the problem fast, but provide deep and complete breakdowns. Avoid fluff, focus on clarity.
You speak like an engineer who respects the user's time and gives practical insights without overcomplicating things.
"""
    else:
        return "You are an AI assistant who is expert in breaking down complex problems and resolving queries."

def build_system_prompt(tone_instruction: str) -> str:
    return f"""
{tone_instruction}

You are an AI assistant who is expert in breaking down complex problems and then resolve the user query.

For the given user input, analyse the input and break down the problem step by step.
At least think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next input
3. Carefully analyse the user query

Output Format:
{{{{ step: "string", content: "string" }}}}

Example:
Input: How can I deploy a MERN app for free?
Output: {{{{ "step": "analyse", "content": "The user is asking for deployment options for a MERN stack app and wants it to be free." }}}}
Output: {{{{ "step": "think", "content": "To solve this, I should think of free hosting platforms for both frontend and backend — e.g., Vercel for React, Render or Cyclic for Express backend." }}}}
Output: {{{{ "step": "output", "content": "You can deploy React frontend to Vercel and Node/Express backend to Render or Cyclic. MongoDB can be hosted on MongoDB Atlas (free tier)." }}}}
Output: {{{{ "step": "validate", "content": "This stack has been validated by the dev community. Many beginners use this for full-stack projects." }}}}
Output: {{{{ "step": "result", "content": "Deploy MERN stack for free by using Vercel (React), Render (Node), and MongoDB Atlas (DB)." }}}}
"""

def initialize_log():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"session_{timestamp}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Session Log — {timestamp}\n\n")
    return filename


def append_to_log(filename, content):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(content + "\n")



def cli():
    print("🎓 Welcome to Dev Assistant CLI!")
    print("Choose your mentor's tone:\n1. Hitesh Sir\n2. Sir Piyush Garg")
    tone_choice = input("Enter choice (1 or 2): ").strip()

    tone_instruction = get_tone_instruction(tone_choice)
    system_prompt = build_system_prompt(tone_instruction)

    messages = [{"role": "system", "content": system_prompt}]
    log_file = initialize_log()

    while True:
        query = input("> Your question: ")
        messages.append({"role": "user", "content": query})
        append_to_log(log_file, f"## ❓ User\n{query}\n")

        complete = False
        while not complete:
            response = client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=messages
            )

            parsed = json.loads(response.choices[0].message.content)
            messages.append({"role": "assistant", "content": json.dumps(parsed)})

            step = parsed.get("step", "").title()
            content = parsed.get("content", "")

            append_to_log(log_file, f"### 🧠 {step}\n{content}\n")

            if step.lower() == "output":
                print(f"🤖 Output: {content}")
                complete = True
            else:
                print(f"🧠 {step}: {content}")

        again = input("👉 Do you want to ask another question? (y/n): ").strip().lower()
        if again != "y":
            print(f"📝 Session saved to `{log_file}`. Goodbye!")
            break

def main():
    cli()

if __name__ == "__main__":
    main()  

