import tiktoken
from typing import TypedDict, Literal
from llmClient import LLMClient


class Msg(TypedDict):
    content: str
    role: Literal["user", "assistant"]



def getTokenNum(msgs: list[Msg]) -> int:
    enc = tiktoken.get_encoding("o200k_base")
    return sum(len(enc.encode(m["content"])) for m in msgs)


class Chatbox():
    def __init__(self, model, name="Aiko", tono="formale", max_tokenNum=2000):
        self.instructions = (
            f"Ti chiami {name}\n"
            f"rispondi sempre con tono {tono}"
            "Quando non sai qualcosa lo dici e non inventi"
        )
        self.history: list[Msg] = []
        self.model = model or "gpt-4o-mini"
        self.__client = LLMClient()
        self.maxToken = max_tokenNum

    def send(self, msg):
        self.history.append({"role": "user", "content": msg})
        self.__tronca()
        r = self.__client.chat(self.history, self.instructions)
        self.history.append({"role": "assistant", "content": r})
        return r
    
    def __tronca(self):
        while len(self.history) > 1 and getTokenNum(self.history) > self.max_tokenNum:
            self.history.pop(0)

    def chat(self):
        print("Per uscire dalla chat scrivi 'Quit' o 'Exit\n'")
        while True:
            msg = input("Tu> ").strip()
            if msg.lower() in {"quit", exit}:
                break
            if not msg:
                continue
            r = self.send(msg)
            print(f"\nBot> {r}")
            tokIn, tokOut, cost = self.__client.costo_ultimoUso
            print(f"token in input: {tokIn}, token in output: {tokOut}, costo ultima domanda ${cost:.5f}\n")
            print(f"Fin'ora in totale hai speso ${self.__client.costoTot:.5f} facendo {self.__client.n_chimate} chimate")


if __name__ == "__main__":
    Chatbox().chat()





