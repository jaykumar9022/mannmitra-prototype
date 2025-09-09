# backend/vertex_client.py
import os
import random

# MOCK mode for development (no Google credentials needed)
MOCK = os.environ.get("MOCK_VERTEX", "true").lower() == "true"

# Simple in-memory context store for each user
user_context = {}

# Some sample empathetic / supportive responses
GENERIC_REPLIES = [
    "I hear you. Can you tell me a bit more?",
    "Thanks for sharing that with me.",
    "I understand. How does that make you feel?",
    "That sounds important. Can you elaborate?",
    "I'm listening. Please go on.",
    "I appreciate you opening up about this.",
]

STRESS_REPLIES = [
    "I know things can get overwhelming. Want to try a 2-minute breathing exercise?",
    "Take a deep breath. How about we focus on one thing at a time?",
    "It sounds stressful. Remember, small steps can help a lot.",
]

MOOD_REPLIES = [
    "Got it! How long have you been feeling like this?",
    "Thanks for sharing your mood. Would you like some tips to feel better?",
    "Noted! Remember, it's okay to have ups and downs.",
]

HELP_REPLIES = [
    "I can guide you through: Mood Tracker, Journal, Exercises, and Quotes.",
    "Here are some tools I can help you with: Mood Tracker, Journal, Exercises.",
]

def generate_response(prompt: str, user_id: str = "anon"):
    """
    Returns dynamic empathetic responses without relying on hard keywords.
    Uses per-user context to make conversation feel more natural.
    """
    if MOCK:
        # Initialize context for user if not exists
        if user_id not in user_context:
            user_context[user_id] = {"last_prompt": None, "mood": None}

        context = user_context[user_id]
        lower_prompt = prompt.lower()

        response = ""

        # Detect if user asks for help
        if "help" in lower_prompt or "tool" in lower_prompt:
            response = random.choice(HELP_REPLIES)
        # Detect if user mentions mood words
        elif any(word in lower_prompt for word in ["happy", "sad", "angry", "tired", "low"]):
            response = random.choice(MOOD_REPLIES)
        # Detect stress-related sentences
        elif any(word in lower_prompt for word in ["stress", "exam", "pressure", "anxious", "nervous"]):
            response = random.choice(STRESS_REPLIES)
        else:
            # Generic empathetic response
            response = random.choice(GENERIC_REPLIES)

        # Update context
        context["last_prompt"] = prompt

        return response

    else:
        # Template for real Vertex AI call
        from google.oauth2 import service_account
        import google.auth.transport.requests
        import requests

        SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
        sa_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not sa_path:
            raise ValueError("Set GOOGLE_APPLICATION_CREDENTIALS to your service account JSON path.")

        credentials = service_account.Credentials.from_service_account_file(sa_path, scopes=SCOPES)
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
        token = credentials.token

        model_endpoint = os.environ.get("VERTEX_ENDPOINT")  # e.g. https://.../v1/projects/...
        if not model_endpoint:
            raise ValueError("Set VERTEX_ENDPOINT env var to your Vertex generative endpoint.")

        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {
            "instances": [
                {"input": prompt}
            ],
            # "parameters": {...}  # depending on your model
        }

        resp = requests.post(model_endpoint, headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        j = resp.json()
        return j.get("predictions", [{}])[0].get("content", "Sorry, I couldn't generate a reply.")
