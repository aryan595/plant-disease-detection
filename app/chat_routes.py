
import logging
from typing import Literal

from fastapi import APIRouter, HTTPException
from openai import (
    APIConnectionError,
    APIError,
    APIStatusError,
    AuthenticationError,
    RateLimitError,
)
from pydantic import BaseModel, Field

from app.chat_service import (
    CHAT_MODEL,
    SUPPORTED_LANGUAGES,
    generate_chat_reply,
)


# =========================================
# Router and logging
# =========================================

router = APIRouter(tags=["chatbot"])

logger = logging.getLogger(__name__)


# =========================================
# Request models
# =========================================

class ChatMessage(BaseModel):

    role: Literal["user", "assistant"]

    content: str = Field(
        min_length=1,
        max_length=3000,
    )


class TopPrediction(BaseModel):

    plant: str | None = Field(default=None, max_length=100)
    disease: str | None = Field(default=None, max_length=200)

    confidence: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )


class PlantContext(BaseModel):

    plant: str | None = Field(default=None, max_length=100)
    disease: str | None = Field(default=None, max_length=200)

    confidence: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    confidence_status: str | None = Field(
        default=None,
        max_length=50,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    symptoms: list[str] | None = Field(
        default=None,
        max_length=5,
    )

    management: list[str] | None = Field(
        default=None,
        max_length=5,
    )

    prevention: list[str] | None = Field(
        default=None,
        max_length=5,
    )

    top_3: list[TopPrediction] | None = Field(
        default=None,
        max_length=3,
    )


class ChatRequest(BaseModel):

    messages: list[ChatMessage] = Field(
        min_length=1,
        max_length=10,
    )

    language: str = Field(
        default="auto",
        max_length=10,
    )

    plant_context: PlantContext | None = None


# =========================================
# Health check
# =========================================

@router.get("/chat/health")
def chat_health():

    return {
        "status": "ready",
        "provider": "Groq",
        "model": CHAT_MODEL,
        "supported_languages": len(SUPPORTED_LANGUAGES),
        "plant_context_supported": True,
        "message": "Plant Health Assistant endpoint is ready.",
    }


# =========================================
# Chat endpoint
# =========================================

@router.post("/chat")
def chat(request: ChatRequest):

    # -------------------------------------
    # Validate language
    # -------------------------------------

    if request.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=422,
            detail="Unsupported language selection.",
        )

    # -------------------------------------
    # Validate messages and request size
    # -------------------------------------

    messages = []
    total_characters = 0

    for message in request.messages:

        content = message.content.strip()

        if not content:
            raise HTTPException(
                status_code=422,
                detail="Messages cannot be empty.",
            )

        total_characters += len(content)

        messages.append({
            "role": message.role,
            "content": content,
        })

    if total_characters > 8000:
        raise HTTPException(
            status_code=413,
            detail=(
                "Conversation is too long. "
                "Please start a new chat or shorten your messages."
            ),
        )

    if messages[-1]["role"] != "user":
        raise HTTPException(
            status_code=422,
            detail="The latest message must be from the user.",
        )

    # -------------------------------------
    # Prepare current plant analysis
    # -------------------------------------

    plant_context = None

    if request.plant_context is not None:

        plant_context = request.plant_context.model_dump(
            exclude_none=True,
        )

        # A serialized context is limited before reaching the AI.
        # Further text and list limits are applied in chat_service.py.
        context_characters = sum(
            len(str(value))
            for value in plant_context.values()
        )

        if context_characters > 5000:
            raise HTTPException(
                status_code=413,
                detail="Plant analysis context is too large.",
            )

    # -------------------------------------
    # Call Groq through chat_service
    # -------------------------------------

    try:

        reply = generate_chat_reply(
            messages,
            language=request.language,
            plant_context=plant_context,
        )

        return {
            "reply": reply,
            "provider": "Groq",
            "model": CHAT_MODEL,
            "language": request.language,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )

    except RuntimeError:

        logger.exception("Chatbot configuration error.")

        raise HTTPException(
            status_code=503,
            detail=(
                "The chatbot is not configured correctly. "
                "Check the backend environment settings."
            ),
        )

    except AuthenticationError:

        logger.exception("Groq authentication failed.")

        raise HTTPException(
            status_code=502,
            detail=(
                "The AI provider rejected the API credentials. "
                "Check the server's Groq API key configuration."
            ),
        )

    except RateLimitError:

        logger.exception("Groq rate limit or quota error.")

        raise HTTPException(
            status_code=429,
            detail=(
                "The AI service has reached a rate or usage limit. "
                "Check your Groq account limits and try again later."
            ),
        )

    except APIConnectionError:

        logger.exception("Could not connect to Groq.")

        raise HTTPException(
            status_code=503,
            detail=(
                "Could not connect to the AI service. "
                "Check your internet connection and try again."
            ),
        )

    except APIStatusError as exc:

        logger.exception("Groq returned an unsuccessful status.")

        raise HTTPException(
            status_code=502,
            detail=(
                "The AI provider could not complete the request "
                f"(status {exc.status_code})."
            ),
        )

    except APIError:

        logger.exception("Groq SDK returned an API error.")

        raise HTTPException(
            status_code=502,
            detail="The AI service encountered an error.",
        )

    except Exception:

        logger.exception("Unexpected chatbot error.")

        raise HTTPException(
            status_code=500,
            detail="An unexpected chatbot error occurred.",
        )
