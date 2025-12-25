class PromptController:
    def __init__(self, role: str):
        self.role = role

    def build_prompt(self, user_input: str, memory) -> str:
        system_prompt = f"""
You are Jarvis, a personal AI assistant.

Role: {self.role}

Capabilities:
- Tutor  : Explain theory with examples
- Coder  : Write clean code and explain it
- Mentor : Give career and learning guidance
"""

        conversation = ""
        for mem in memory.get_history():
            conversation += f"{mem['role'].capitalize()}: {mem['message']}\n"

        return f"""{system_prompt}

{conversation}
User: {user_input}
Jarvis:"""