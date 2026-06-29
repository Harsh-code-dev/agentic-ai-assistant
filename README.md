# 🤖 Agentic AI Assistant

## 📖 Overview

Agentic AI Assistant is an autonomous AI agent built using Python and the OpenAI API. Unlike a traditional chatbot, the agent follows a reasoning loop where it plans tasks, selects appropriate tools, observes their outputs, and continues executing until the user's request is completed.

The project demonstrates the fundamentals of **Agentic AI**, including tool calling, multi-step reasoning, autonomous decision making, and workflow execution.

---

## ✨ Features

* 🧠 Multi-step reasoning using PLAN → TOOL → OBSERVE → OUTPUT
* 🔧 Tool calling architecture
* 🌦️ Real-time weather information
* 📁 Create folders
* 📄 Create files
* ✏️ Update files
* 📖 Read files
* 📂 List directory contents
* 💬 Conversation memory during the session
* 🤖 JSON-based structured responses

---

## 🛠 Tech Stack

| Category        | Technology                     |
| --------------- | ------------------------------ |
| Language        | Python                         |
| LLM             | OpenAI GPT-4o                  |
| Environment     | python-dotenv                  |
| HTTP Requests   | Requests                       |
| AI Architecture | Agentic AI                     |
| Prompting       | Tool Calling + Structured JSON |

---

## 🏗 Agent Workflow

```text
User
   │
   ▼
OpenAI GPT
   │
   ▼
PLAN
   │
   ▼
Select Tool
   │
   ▼
Execute Tool
   │
   ▼
Observe Result
   │
   ▼
Continue Planning
   │
   ▼
Final Output
```

---

## 🔧 Available Tools

* Weather Lookup
* Create Folder
* Create File
* Read File
* Update File
* List Directory

---

## 📂 Project Structure

```text
agentic_ai_assistant/
│── agent.py
│── requirements.txt
│── .env.example
│── .gitignore
│── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Harsh-code-dev/agentic-ai-assistant.git
cd agentic-ai-assistant
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it (Windows)

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
OPENAI_API_KEY=your_openai_api_key
```

Run the agent

```bash
python agent.py
```

---

## 🚀 Example Capabilities

* "Create a folder named Notes"
* "Create a Python file named hello.py"
* "Update the README file"
* "List all files in the project"
* "What's the weather in Delhi?"

---

## 🔮 Future Improvements

* Web interface using Streamlit or React
* Support for multiple LLM providers
* Voice interaction
* Database integration
* Long-term memory
* Multi-agent collaboration

---

## 👨‍💻 Author

**Harsh Kumar**

GitHub: https://github.com/Harsh-code-dev
