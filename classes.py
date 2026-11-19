
from abc import ABC, abstractmethod
from datetime import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Cliente:
    nome: str
    cpf: str
    senha: str
    cidade: str
    estado: str

    def converter_para_dicionario(self) -> dict[str, str]:
        return {
            "nome": self.nome,
            "senha": self.senha,
            "cidade": self.cidade,
            "estado": self.estado,
        }


@dataclass(frozen=True)
class Agencia:
    codigo: str
    cidade: str
    estado: str

    def converter_para_dicionario(self) -> dict[str, str]:
        return {
            "codigo": self.codigo,
            "cidade": self.cidade,
            "estado": self.estado,
        }


class Conta(ABC):
    def __init__(self, numero, cliente, saldo: float, agencia="0001"):
        self.numero_da_conta = numero
        self.cliente = cliente
        self.agencia = agencia
        self._saldo = saldo
        self.extrato = []

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

    @property
    def saldo_formatado(self) -> str:
        valor = f"{self._saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {valor}"

    @abstractmethod
    def registrar_transacao(self, descricao: str, valor: float):
        pass

    def depositar(self, valor: float, descricao: str = "Depósito") -> dict:
        if valor <= 0:
            raise ValueError("Acrescente um valor positivo para depositar.")

        self.saldo += valor
        self.registrar_transacao(descricao, valor)
        return {
            "sucesso": True,
            "mensagem": f"{descricao} realizado com sucesso!",
            "novo_saldo": self.saldo_formatado,
        }

    @abstractmethod
    def sacar(self, valor: float) -> dict:
        pass

    def converter_para_dicionario(self) -> dict:
        return {
            "tipo": self.tipo,
            "agencia": self.agencia,
            "numero": self.numero_da_conta,
            "cliente": self.cliente,
            "saldo": self.saldo,
            "saldo_formatado": self.saldo_formatado,
            "extrato": self.extrato,
        }


class contacorrente(Conta):
    def __init__(self, numero, titular, saldo: float, limite: float = 500.0, ):
        super().__init__(numero, titular, saldo)
        self.limite = limite

    @property
    def tipo(self) -> str:
        return "Conta Corrente"

    def sacar(self, valor: float): -> float:
        if valor <= 0:
            raise ValueError("O valor precisar se positivo para sacar")
        if valor > self.saldo + self.limite:
            raise ValueError("Saldo e limite insuficientes para o saque.")

        self.saldo -= valor
        self.registrar_transacao("Saque", -valor)
        return {
            "sucesso": True,
            "mensagem": "Saque realizado com sucesso!",
            "novo_saldo": self.saldo_formatado,
        }

    def registrar_transacao(self, descricao: str, valor: float):
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.extrato.append(f"[{data_hora}] {descricao}: R$ {valor:.2f}")


class contapoupanca(Conta):
    def __init__(self, numero, titular, saldo, taxa_mensal=0.005):
        super().__init__(numero, titular, saldo)
        self.taxa_mensal = taxa_mensal

    @property
    def tipo(self) -> str:
        return "Conta Poupança"

    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("Informe um valor positivo para sacar.")
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente para o saque.")

        self.saldo -= valor
        self.registrar_transacao("Saque", -valor)
        return {
            "sucesso": True,
            "mensagem": "Saque realizado com sucesso!",
            "novo_saldo": self.saldo_formatado,
        }

    def registrar_transacao(self, descricao: str, valor: float):
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.extrato.append(f"[{data_hora}] {descricao}: R$ {valor:.2f}")

    def aplicar_rendimento(self, meses: int = 1) -> dict:
        if meses <= 0:
            raise ValueError("A quantidade de meses deve ser maior que zero.")

        if self.saldo <= 0:
            return {
                "sucesso": False,
                "mensagem": "Sem saldo para render juros.",
                "rendimento": 0.0,
            }

        novo_saldo = self.saldo * ((1 + self.taxa_mensal) ** meses)
        rendimento = round(novo_saldo - self.saldo, 2)

        if rendimento > 0:
            descricao = f"Rendimento ({meses} {'mês' if meses == 1 else 'meses'})"
            self.depositar(rendimento, descricao=descricao)

        return {
            "sucesso": True,
            "mensagem": f"Rendimento de R$ {rendimento:.2f} aplicado!",
            "rendimento": rendimento,
            "novo_saldo": self.saldo_formatado,
        }
