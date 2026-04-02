from agent import process_message

messages = []

print("Chat with Claude - type 'quit' to exit\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    reply, messages = process_message(messages, user_input)
    print(f"Claude: {reply}\n")