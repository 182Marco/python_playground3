from openai import OpenAI, AsyncOpenAI, RateLimitError, AuthenticationError, APIError
from dotenv import load_dotenv
from pydantic import BaseModel
import json
import asyncio

load_dotenv()

client = OpenAI()
client_async = AsyncOpenAI()
model = "gpt-4o-mini"
istruzioni = (
    "Sei un classificatore di ticket. "
    "Rispondi con una sola parola tra: "
    "commerciale, tecnico, fatturazione, spedizione, generale"
)


class Ticket(BaseModel):
     id: int
     messaggio: str

def getTickets():
    with open("tickets.json", encoding="utf-8") as f:
        tickets = json.load(f)
        return [Ticket(**t) for t in tickets]
    

def classifica(msg: str) -> str:
    try:
            r = client.responses.create(
                input=msg,
                instructions=istruzioni,
                model=model,
            )
    except RateLimitError:
        raise SystemExit("Hai fatto troppe chimate riprova più tardi")
    except AuthenticationError as e:
        return f"AuthenticationError: {type(e).__name__}"
    except APIError as e:
        self.costo_ultimoUso = 0, 0, 0.0
        return f"APIError: {type(e).__name__}"
    
    return r.output_text



async def classifica_async(msg:str) -> str:
    try:
            r = await client_async.responses.create(
                input={msg},
                instructions=istruzioni,
                model=model,
            )
    except RateLimitError:
        raise SystemExit("Hai fatto troppe chimate riprova più tardi")
    except AuthenticationError as e:
        return f"AuthenticationError: {type(e).__name__}"
    except APIError as e:
        self.costo_ultimoUso = 0, 0, 0.0
        return f"APIError: {type(e).__name__}"
    
    return r.output_text


tickets = getTickets()

serie = [classifica(t.messaggio) for t in tikets]

async def getPrallelo():
  return await asyncio.gather(*[classifica(t.messaggio) for t in tikets])

par = asyncio.run(getPrallelo())


