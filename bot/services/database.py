from postgrest.exceptions import APIError
from supabase import create_client, Client
from bot.config import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_or_create_user(telegram_id, username, display_name):
    try:
        response = supabase.table("users").upsert(
            {
                "telegram_id": telegram_id,
                "username": username,
                "display_name": display_name
            },
            on_conflict="telegram_id"
        ).execute()

        return response.data[0] if response.data else None

    except APIError as e:
        # Handle specific DB errors (wrong table, column types, etc.)
        print(f"Database Error: {e.message}")
        return None
    except Exception as e:
        # Handle unexpected errors (network out, etc.)
        print(f"Unexpected Error: {e}")
        return None

def get_or_create_group(telegram_chat_id, chat_name):
    try:
        response = supabase.table("group_chats").upsert(
            {
                "telegram_chat_id": telegram_chat_id,
                "chat_name": chat_name,
            },
            on_conflict="telegram_chat_id"
        ).execute()

        return response.data[0] if response.data else None

    except APIError as e:
        # Handle specific DB errors (wrong table, column types, etc.)
        print(f"Database Error: {e.message}")
        return None
    except Exception as e:
        # Handle unexpected errors (network out, etc.)
        print(f"Unexpected Error: {e}")
        return None

# Save every message sent
def database_save_message(chat_id, sender_id, message_text):
    try:
        supabase.table("messages").insert({
            "chat_id": chat_id,
            "sender_id": sender_id,
            "message_text": message_text
        }).execute()
    except APIError as e:
        print(f"Database Error: {e.message}")
        return None
    except Exception as e:
        # Handle unexpected errors (network out, etc.)
        print(f"Unexpected Error: {e}")
        return None

# Get last 50 message
def get_recent_messages(chat_id, limit=50):
    try:
        response = supabase.table("messages").select("*, users(display_name)").eq("chat_id", chat_id).order("created_at", desc=True).limit(limit).execute()
        messages = []
        for msg in response.data:
            messages.append({
                "name": msg["users"]["display_name"],
                "text": msg["message_text"]
            })
        # Reverse so oldest is first, newest is last
        messages.reverse()
        return messages
    except APIError as e:
        print(f"Database Error: {e.message}")
        return None
    except Exception as e:
        # Handle unexpected errors (network out, etc.)
        print(f"Unexpected Error: {e}")
        return None