from groq import Groq
from bot.config import GROQ_API_KEY
client = Groq(api_key=GROQ_API_KEY)

def generate_reply(messages, user_name):
    prompt = build_prompt(messages, user_name)

    # DEBUG: Print what we're sending
    print("=" * 50)
    print("MESSAGES RECEIVED:", messages)
    print("=" * 50)
    print("PROMPT SENT TO LLM:")
    print(prompt)
    print("=" * 50)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content

def build_prompt(messages, user_name):
    chat_history = "\n".join([f"{msg['name']}: {msg['text']}" for msg in messages])

    user_messages = [msg['text'] for msg in messages if msg['name'] == user_name]
    user_examples = "\n".join(user_messages[-10:])  # Last 10 messages from this user

    # Get the last message from someone OTHER than the user (what we need to respond to)
    other_messages = [msg for msg in messages if msg['name'] != user_name]
    last_message = other_messages[-1] if other_messages else {"name": "Unknown", "text": ""}

    prompt = f"""## STEP 1: READ THE CONVERSATION
Here is a group chat conversation. Understand what everyone is talking about:

{chat_history}

## STEP 2: IDENTIFY WHAT NEEDS A RESPONSE
The last message is from {last_message['name']}: "{last_message['text']}"

This is what you need to respond to. If it's a question, answer it. If it's a statement, reply naturally.

## STEP 3: MATCH THIS WRITING STYLE
You are replying as {user_name}. Here's how {user_name} typically writes:

{user_examples}

Copy their tone, slang, emoji usage, punctuation, and message length.

## NOW GENERATE YOUR REPLY
- Respond to what {last_message['name']} said/asked
- Write exactly like {user_name} would
- Output ONLY the message, no quotes or explanations

Reply:"""

    return prompt
