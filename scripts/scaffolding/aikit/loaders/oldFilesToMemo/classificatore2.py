from openai import OpenAI, AsyncOpenAI, RateLimitError, AuthenticationError, APIError
from dotenv import load_dotenv
from pydantic import BaseModel
import json
import asyncio

load_dotenv()

client= OpenAI()
client_async = AsyncOpenAI()
model="gpt-4o-mini"
instruzioni = (
    "Sei un esperto classificatore "
    "Rispondi con una sola parola tra cane e gatto"
)

class Ticket(BaseModel):
    id: int
    messaggio: str


def getTickets():
    with open("tickets.json", encoding="utf-8") as f:
        file = json.load(f)
    return [Ticket(**t) for t in file]

tickets = getTickets()

def classificatore(text: str):
    try:
        r = client.responses.create(
            model=model,
            input=text,
            instructions=instruzioni
        )
        return r.output_text
    
    except RateLimitError:
        return "Troppe chiamate, riprova più tardi"
    except AuthenticationError as e:
        return f"Errore di autenticazione, controlla .env: {e}"
    except APIError as e:
        raise SystemError(f"Problema con le api: {e}")
    

async def classificatore_async(text: str):
    try:
        r = await client_async.responses.create(
            model=model,
            input=text,
            instructions=instruzioni
        )
        return r.output_text
    
    except RateLimitError:
        return "Troppe chiamate, riprova più tardi"
    except AuthenticationError as e:
        return f"Errore di autenticazione, controlla .env: {e}"
    except APIError as e:
        raise SystemError(f"Problema con le api: {e}")


serie = [classificatore(t.messaggio) for t in tickets]

async def getParallel():
    return await asyncio.gather(*[classificatore_async(t.messaggio) for t in tickets])

par = asyncio.run(getParallel())

