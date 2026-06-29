from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import requests
from pathlib import Path

# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# -----------------------------
# Weather Tool
# -----------------------------

def get_weather(city: str):

    url = f"https://wttr.in/{city.lower()}?format=%C+%t"

    try:

        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return f"Current weather in {city}: {response.text}"

        return "Unable to fetch weather."

    except Exception as e:
        return str(e)

# -----------------------------
# File System Tools
# -----------------------------

def create_folder(name):

    try:

        os.makedirs(name, exist_ok=True)

        return f"Folder '{name}' created."

    except Exception as e:

        return str(e)


def create_file(path, content):

    try:

        folder = os.path.dirname(path)

        if folder != "":
            os.makedirs(folder, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:

            f.write(content)

        return f"{path} created successfully."

    except Exception as e:

        return str(e)


def read_file(path):

    try:

        with open(path, "r", encoding="utf-8") as f:

            return f.read()

    except Exception as e:

        return str(e)


def update_file(path, content):

    try:

        with open(path, "w", encoding="utf-8") as f:

            f.write(content)

        return f"{path} updated."

    except Exception as e:

        return str(e)


BASE_DIR = Path(__file__).resolve().parent
def list_directory(path="."):

    try:

        target = BASE_DIR / path if path else BASE_DIR
        if not target.exists():
            return f"Path does not exist: {target}"
        return "\n".join(os.listdir(target))

    except Exception as e:

        return str(e)

# -----------------------------
# Available Tools
# -----------------------------

available_tools = {

    "get_weather": get_weather,

    "create_folder": create_folder,

    "create_file": create_file,

    "read_file": read_file,

    "update_file": update_file,

    "list_directory": list_directory

}
# -----------------------------
# SYSTEM PROMPT
# -----------------------------

SYSTEM_PROMPT = """
You are an autonomous AI Agent.

Always respond using VALID JSON.

Allowed steps:

PLAN
TOOL
OUTPUT

JSON PLAN format:

{
    "step":"PLAN",
    "content":"text"
}

JSON TOOL format:

{
    "step":"TOOL",
    "tool":"tool_name",
    "input":"tool_input"
}

JSON OUTPUT format:

{
    "step":"OUTPUT",
    "content":"final answer"
}

Available Tools:

1. get_weather(city)

Returns current weather information.

2. create_folder(name)

Creates a new folder.

3. create_file(path||content)

Creates a file.

4. read_file(path)

Reads a file.

5. update_file(path||content)

Updates a file.

6. list_directory(path)

Lists files and folders.

Rules:

1. Think step by step.

2. Never invent tool names.

3. Call only one tool at a time.

4. Wait for OBSERVE before continuing.

5. Finally generate OUTPUT.

6. If a tool does not exist, apologize and continue planning.

7. Never output plain text.

Only output JSON.

"""

# -----------------------------
# Conversation History
# -----------------------------

message_history = [

    {

        "role": "system",

        "content": SYSTEM_PROMPT

    }

]

print()

print("=" * 60)

print("🚀 AI AGENT STARTED")

print("Type exit to quit")

print("=" * 60)

print()

# -----------------------------
# Main Loop
# -----------------------------

while True:

    user_query = input("👉 ")

    if user_query.lower() == "exit":

        print()

        print("👋 Goodbye!")

        break

    message_history.append(

        {

            "role": "user",

            "content": user_query

        }

    )

    while True:

        response = client.chat.completions.create(

            model="gpt-4o",

            response_format={

                "type": "json_object"

            },

            messages=message_history

        )

        raw_result = response.choices[0].message.content

        parsed = json.loads(raw_result)

        step = parsed.get("step")

        if step == "PLAN":

            print()

            print("🧠", parsed.get("content"))

            print()

            message_history.append(

                {

                    "role": "assistant",

                    "content": raw_result

                }

            )

            continue

        # ------------------------------------
        # TOOL STEP
        # ------------------------------------

        elif step == "TOOL":

            tool_name = parsed.get("tool")
            tool_input = parsed.get("input")

            print()
            print(f"🔧 Calling Tool : {tool_name}")
            print()

            # -----------------------------
            # Unknown Tool Handling
            # -----------------------------

            if tool_name not in available_tools:

                tool_output = f"""
Tool '{tool_name}' is not available.

Available tools:

- get_weather
- create_folder
- create_file
- read_file
- update_file
- list_directory
"""

            else:

                # -----------------------------
                # create_file
                # input format:
                # path||content
                # -----------------------------

                if tool_name == "create_file":

                    parts = tool_input.split("||", 1)

                    if len(parts) != 2:

                        tool_output = (
                            "Invalid input format. "
                            "Expected path||content"
                        )

                    else:

                        path = parts[0].strip()
                        content = parts[1]

                        tool_output = available_tools[
                            tool_name
                        ](path, content)

                # -----------------------------
                # update_file
                # path||content
                # -----------------------------

                elif tool_name == "update_file":

                    parts = tool_input.split("||", 1)

                    if len(parts) != 2:

                        tool_output = (
                            "Invalid input format."
                        )

                    else:

                        path = parts[0].strip()
                        content = parts[1]

                        tool_output = available_tools[
                            tool_name
                        ](path, content)

                # -----------------------------
                # Normal Tools
                # -----------------------------

                else:

                    tool_output = available_tools[
                        tool_name
                    ](tool_input)

            print("✅")
            print(tool_output)
            print()

            # -----------------------------
            # OBSERVE
            # -----------------------------

            observe_json = {

                "step": "OBSERVE",

                "tool": tool_name,

                "input": tool_input,

                "output": tool_output

            }

            message_history.append(

                {

                    "role": "developer",

                    "content": json.dumps(
                        observe_json
                    )

                }

            )

            continue

                # ------------------------------------
        # OUTPUT
        # ------------------------------------

        elif step == "OUTPUT":

            print()
            print("🤖")
            print(parsed.get("content"))
            print()

            message_history.append(

                {

                    "role": "assistant",

                    "content": raw_result

                }

            )

            break

        # ------------------------------------
        # OBSERVE (Safety)
        # ------------------------------------

        elif step == "OBSERVE":

            print()

            print("👀")

            print(parsed.get("output"))

            print()

            message_history.append(

                {

                    "role": "assistant",

                    "content": raw_result

                }

            )

            continue

        # ------------------------------------
        # Unknown Step
        # ------------------------------------

        else:

            print()

            print("❌ Unknown Step")

            print(step)

            print()

            message_history.append(

                {

                    "role": "developer",

                    "content": json.dumps(

                        {

                            "step": "OBSERVE",

                            "output": f"Unknown step : {step}"

                        }

                    )

                }

            )

            continue

# ------------------------------------
# End Program
# ------------------------------------

print()

print("=" * 60)

print("Session Ended")

print("=" * 60)