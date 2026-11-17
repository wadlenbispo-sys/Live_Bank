from abc import ABC, abstractmethod
from datetime import datetime

class Conta(ABC):

   def __init__(self, numero, cliente, saldo: int, agencia="0001"):
       self.numero_da_conta = numero
       self.cliente = cliente
       self.agencia = agencia
       self._saldo = saldo
       self.extrato = []  # Aqui será guardado o histórico de movimentos
    
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
   def sacar(self, valor):
       pass
      
   def depositar(self, valor):
       if valor < 0:
          raise ValueError("acrescente um valor positivo para depositar")
       else:
          self.saldo += valor
          self.extrato.append({"Cliente": self.cliente, "numero_da_conta": self.numero_da_conta, "D": valor, "Saldo_final": self.saldo})

# classe reponsavel pelas operações da conta corrente.
class contacorrente(Conta):

   def __init__(self, numero, titular, saldo):
       super().__init__(numero, titular, saldo)

   @property
   def tipo(self) -> str:
       return "Conta Corrente"

   def sacar(self, valor):
       if valor > self.saldo:
          raise ValueError("valor maior do que já tem")
       else:
          self.saldo -= valor
          self.extrato.append({"Cliente": self.cliente, "numero_da_conta": self.numero_da_conta, "S": valor, "saldo_final": self._saldo})
          
   def depositar(self, valor):
       if valor < 0:
          raise ValueError("acrescente um valor positivo para depositar")
       else:
          self.saldo += valor
          self.extrato.append({"Cliente": self.cliente, "numero_da_conta": self.numero_da_conta, "S": valor, "saldo_final": self._saldo})

   def registrar_transacao(self, descricao: str, valor: float):
       data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
       self.extrato.append(f"[{data_hora}] {descricao}: R$ {valor:.2f}")
      
# classe responsavel pelas operações da conta poupança.
class contapoupanca(Conta):

    def __init__(self, numero, titular, saldo, taxa_mensal=0.005):
        super().__init__(numero, titular, saldo)
        self.taxa_mensal = taxa_mensal  # Ex: 0.005 equivale a 0,5% ao mês

    @property
    def tipo(self) -> str:
        return "Conta Poupança"

    def sacar(self, valor):
        if valor > self.saldo:
           raise ValueError("valor maior do que já tem")
        else:
           self.saldo -= valor
           self.extrato.append({"Cliente": self.cliente, "numero_da_conta": self.numero_da_conta, "S": valor, "saldo_final": self._saldo})
   





