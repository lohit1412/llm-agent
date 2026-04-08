import memory
from agent import process_message

# Load summary from previous sessions
summary = memory.load_summary()

# Inject summary as opening context
messages = []

if summary:
    messages.append({
        "role": "user",
        "content": f"Here is context from our previous conversations: {summary}"
    })
    messages.append({
        "role": "assistant", 
        "content": "Understood. I have context from our previous conversations and will use it naturally."
    })

print("Chat with Claude - type 'quit' to exit\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        memory.save_memory(messages)
        memory.save_summary(messages)
        break

    reply, messages = process_message(messages, user_input)
    print(f"Athena: {reply}\n")