from google import genai

client = genai.Client(api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

from clubs import CHAT_LOGS, CLUBS


files = []
for d in CLUBS:
    files.append(open(f"reports/{d}.md", "r").read())


logs = []
for d in CHAT_LOGS:
    logs.append(open(f"{d}", "r").read())

print(logs)
