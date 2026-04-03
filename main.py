import memory
from agent import process_message

messages = memory.load_memory()

print("Chat with Claude - type 'quit' to exit\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        memory.save_memory(messages)
        break

    reply, messages = process_message(messages, user_input)
    print(f"Athena: {reply}\n")