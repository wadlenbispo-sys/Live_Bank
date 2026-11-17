from abc import ABC, abstractmethod
from datetime import datetime

class Conta(ABC):

   def __init__(self, numero, cliente, saldo: int, agencia="0001"):
       self.numero_da_conta = numero
       self.cliente = cliente
       self.agencia = agencia
       self._saldo = saldo
       self.extrato = []  # Aqui será guardado o histórico de movimentos na conta
    
   @property
   def saldo(self) -> float:
       return self._saldo

   @saldo.setter
   def saldo(self, valor):
       self._saldo = valor

   @property
   @abstractmethod
   def tipo(self) -> str:
       pass

   @abstractmethod
   def registrar_transacao(self, descricao: str, valor: float):
       pass

   @abstractmethod
   def sacar(self, valor) -> float:
       pass

   # metodo que será herdado pelas classes contacorrente e contapoupança.
   def depositar(self, valor):
       if valor < 0:
          raise ValueError("acrescente um valor positivo para depositar")
       else:
          self.saldo += valor
          self.registrar_transacao(descricao, valor)
          return {"sucesso": True, "mensagem": f"{descricao} realizado com sucesso!", "novo_saldo": self.saldo_formatado}

    @abstractmethod
    def sacar(self, valor: float) -> dict:
        pass

    def to_dict(self) -> dict:
        """Exporta todos os dados da conta para templates HTML ou respostas JSON."""
        return {
            "tipo": self.tipo,
            "agencia": self.agencia,
            "numero": self.numero_da_conta,
            "cliente": self.cliente,
            "saldo": self.saldo,
            "saldo_formatado": self.saldo_formatado,
            "extrato": self.extrato
        }

# classe reponsavel pelas operações da conta corrente.
class contacorrente(Conta):

   def __init__(self, numero, titular, saldo, limite: float = 500.0):
       super().__init__(numero, titular, saldo)
       self.limite = limite

   @property
   def tipo(self) -> str:
       return "Conta Corrente"

   def sacar(self, valor):
       if valor <= 0:
          raise ValueError("O valor precisar se positivo para sacar")
          
       if valor > (self.saldo + self.limite):
            raise ValueError("Saldo e limite insuficientes para o saque.")
       else:
          self.saldo -= valor
          self.registrar_transacao("Saque", -valor)
          return {"sucesso": True, "mensagem": "Saque realizado com sucesso!", "novo_saldo": self.saldo_formatado}



   # responsavel por registrar as tansações acrescentando a hora e descrição do que foi feito.
   def registrar_transacao(self, descricao: str, valor: float):
       data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
       self.extrato.append(f"[{data_hora}] {descricao}: R$ {valor:.2f}")
      
# classe responsavel pelas operações da conta poupança.
class contapoupanca(Conta):

    def __init__(self, numero, titular, saldo, taxa_mensal=0.005):
        super().__init__(numero, titular, saldo)
        self.taxa_mensal = taxa_mensal   #0.005 equivale a 0,5% ao mês

    @property
    def tipo(self) -> str:
        return "Conta Poupança"

    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("Informe um valor positivo para sacar.")
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente para o saque.")
        else:
           self.saldo -= valor
           self.registrar_transacao("Saque", -valor)
           return {"sucesso": True, "mensagem": "Saque realizado com sucesso!", "novo_saldo": self.saldo_formatado}

   
    # responsavel por registrar as tansações acrescentando a hora e descrição do que foi feito.
    def registrar_transacao(self, descricao: str, valor: float):
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.extrato.append(f"[{data_hora}] {descricao}: R$ {valor:.2f}")

    def render_juros(self, meses: int = 1) -> dict:
        if meses <= 0:
            raise ValueError("A quantidade de meses deve ser maior que zero.")
        
        if self.saldo <= 0:
            return {"sucesso": False, "mensagem": "Sem saldo para render juros.", "rendimento": 0.0}

        novo_saldo = self.saldo * ((1 + self.taxa_mensal) ** meses)
        rendimento = round(novo_saldo - self.saldo, 2)

        if rendimento > 0:
            descricao = f"Rendimento ({meses} {'mês' if meses == 1 else 'meses'})"
            self.depositar(rendimento, descricao=descricao)

        return {
            "sucesso": True,
            "mensagem": f"Rendimento de R$ {rendimento:.2f} aplicado!",
            "rendimento": rendimento,
            "novo_saldo": self.saldo
        }




