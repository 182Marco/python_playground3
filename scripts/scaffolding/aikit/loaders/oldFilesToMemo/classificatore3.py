from openai import OpenAI, AsyncOpenAI, AuthenticationError, RateLimitError, APIError
from dotenv import load_dotenv
from pydantic import BaseModel
import json
import asyncio

load_dotenv()

class Ticket(BaseModel):
    id: int
    message: str


def getTickets():
    with open("tickets.json", encoding="utf-8") as f:
        tickets = json.load(f)
        return [Ticket(**t) for t in tickets]

allTickets = getTickets()

client = OpenAI(max_retries=3, timeout=30)
client_async = AsyncOpenAI(max_retries=3, timeout=30)
inst = (
    "Sei un esperto classificatore. \n"
    "Rispondi sempre con una parola"
)
model = "gpt-4o-mini"

def classifica(temperature= 0):
    try:
        r = client.responses.create(
            model={model},
            instructions={inst},
            client={client},
            temperature=temperature
        )

        return r.output_text

    except AuthenticationError as e:
        return f"C' è un probelma di autenticazione: {e}"
    except RateLimitError as e:
        raise SystemError(f"Troppe chimate insime, riprova più tardi: {e}")
    except AuthenticationError as e:
        return f"Problema di connessione, controlla .env: {e}"
    except APIError as e:
        raise SystemError(f"Problema le api: {e}")


async def classifica_async( temperature= 0):
    try:
        r = await client_async.responses.create(
            model={model},
            instructions={inst},
            client={client},
            temperature=temperature
        )

        return r.output_text

    except AuthenticationError as e:
        return f"C' è un probelma di autenticazione: {e}"
    except RateLimitError as e:
        raise SystemError(f"Troppe chimate insime, riprova più tardi: {e}")
    except AuthenticationError as e:
        return f"Problema di connessione, controlla .env: {e}"
    except APIError as e:
        raise SystemError(f"Problema le api: {e}")

serie = [classifica(t.message) for t in allTickets]

async def getParallelo():
    return await asyncio.gather(*[classifica_async(t.message) for t in allTickets])

par = asyncio.run(getParallelo())