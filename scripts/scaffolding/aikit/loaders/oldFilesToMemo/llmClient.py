from openai import OpenAI, RateLimitError, APIError, AuthenticationError
from pricing import cost_usd
from dotenv import load_dotenv

load_dotenv()


class LLMClient():
    def __init__(self, model="gpt-4o-mini", temperature=1):
        self.client = OpenAI(max_retries=3, timeout=30)
        self.model = model
        self.temperature = temperature
        self.n_chimate = 0
        self.costoTot = 0
        self.costo_ultimoUso = 0, 0, 0.0
    
    def chat(self, history, informazioni:str):
        try:
            r = self.client.responses.create(
                input={history},
                instructions=informazioni,
                model=self.model,
                temperature=self.temperature
            )
        except RateLimitError:
            raise SystemExit("Hai fatto troppe chimate riprova più tardi")
        except AuthenticationError as e:
            return f"AuthenticationError: {type(e).__name__}"
        except APIError as e:
            self.costo_ultimoUso = 0, 0, 0.0
            return f"APIError: {type(e).__name__}"
        
        u = r.usage
        costNow = cost_usd(self.model, u.input_tokens, u.output_tokens)
        self.costoTot += costNow
        self.n_chimate += 1
        self.costo_ultimoUso = u.input_tokens, u.output_tokens, costNow

        return r.output_text

