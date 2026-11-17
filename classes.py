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
