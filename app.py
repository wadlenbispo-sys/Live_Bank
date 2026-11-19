import json
import re
from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, url_for

from classes import Agencia, Cliente


app = Flask(__name__)
app.secret_key = "troque-por-uma-chave-secreta"
ARQUIVO = Path(__file__).with_name("dados.json")

TIPOS_VALIDOS = {
    "corrente": "Conta Corrente",
    "poupanca": "Conta Poupança",
    "salario": "Conta Salário",
}

PERMISSOES = {
    "corrente": {"saque", "deposito", "transferencia"},
    "poupanca": {"deposito", "rendimento"},
    "salario": {"saque"},
}

TEXTO_OPERACAO = {
    "saque": "Saque",
    "deposito": "Depósito",
    "rendimento": "Rendimento",
    "transferencia": "Transferência",
}

AGENCIA_UNICA = Agencia("0001", "Sergipe", "SE")


def carregar_dados():
    try:
        dados = json.loads(ARQUIVO.read_text(encoding="utf-8"))
    except FileNotFoundError:
        dados = {}
    except json.JSONDecodeError as erro:
        raise ValueError(f"O arquivo {ARQUIVO.name} contém JSON inválido.") from erro

    if not isinstance(dados, dict):
        raise ValueError(f"O arquivo {ARQUIVO.name} deve conter um objeto JSON.")

    for chave in ("clientes", "agencias", "contas"):
        if not isinstance(dados.get(chave), dict):
            dados[chave] = {}

    agencia_unica = {AGENCIA_UNICA.codigo: AGENCIA_UNICA.converter_para_dicionario()}
    dados_migrados = dados["agencias"] != agencia_unica
    dados["agencias"] = agencia_unica
    for conta in dados["contas"].values():
        if conta.get("agencia_codigo") != AGENCIA_UNICA.codigo:
            conta["agencia_codigo"] = AGENCIA_UNICA.codigo
            dados_migrados = True
        if "agencia_cnpj" in conta:
            del conta["agencia_cnpj"]
            dados_migrados = True

    if dados_migrados and ARQUIVO.exists():
        salvar_dados(dados)
    return dados


def salvar_dados(dados):
    ARQUIVO.write_text(
        json.dumps(dados, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def somente_digitos(texto):
    return re.sub(r"\D", "", texto or "")

#bloqueando validação
#def validar_cpf(cpf):
   # return len(cpf) == 11 and cpf.isdigit() and cpf != cpf[0] * 11


def ler_valor():
    try:
        valor = float(request.form.get("valor", "").replace(",", "."))
    except ValueError:
        return None
    return valor if valor > 0 else None


def erro(mensagem):
    flash(mensagem, "erro")


def ok(mensagem):
    flash(mensagem, "ok")


@app.template_filter("moeda")
def moeda(valor):
    texto = f"{float(valor):,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")

# bloqueando a validação do cpf
#@app.template_filter("cpf")
def formatar_cpf(valor):
    cpf = str(valor)
    if len(cpf) != 11:
        return cpf
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

@app.template_filter("telefone")
def formatar_telefone(valor):
    telefone = str(valor)
    if len(telefone) != 11:
        return telefone
    return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"

@app.route("/")
@app.route("/dashboard")
@app.route("/Live-Bank")
def index():
    dados = carregar_dados()
    saldos_por_tipo = {
        tipo: {"nome": nome, "quantidade": 0, "saldo": 0.0}
        for tipo, nome in TIPOS_VALIDOS.items()
    }

    for conta in dados["contas"].values():
        resumo = saldos_por_tipo.get(conta.get("tipo"))
        if resumo is not None:
            resumo["quantidade"] += 1
            resumo["saldo"] += conta.get("saldo", 0)

    for resumo in saldos_por_tipo.values():
        resumo["saldo"] = round(resumo["saldo"], 2)

    return render_template(
        "index.html",
        total_clientes=len(dados["clientes"]),
        total_agencias=len(dados["agencias"]),
        total_contas=len(dados["contas"]),
        saldos_por_tipo=saldos_por_tipo,
    )


@app.route("/clientes")
def clientes():
    return render_template("clientes.html", clientes=carregar_dados()["clientes"])


@app.route("/clientes/cadastrar", methods=["POST"])
def cadastrar_cliente():
    nome = request.form.get("nome", "").strip()
    cpf = somente_digitos(request.form.get("cpf"))
    telefone = request.form.get("telefone", "")
    email = request.form.get("email", "").strip()

    if not nome or not telefone or not email:
        erro("Preencha nome, telefone e Email.")
        return redirect(url_for("clientes"))

    dados = carregar_dados()
    if cpf in dados["clientes"]:
        erro("CPF já cadastrado.")
        return redirect(url_for("clientes"))

    cliente = Cliente(nome, cpf, telefone, email)
    dados["clientes"][cpf] = cliente.converter_para_dicionario()
    dados["clientes"] = dict(
        sorted(dados["clientes"].items(), key=lambda item: item[1]["nome"].casefold())
    )
    salvar_dados(dados)
    ok("Cliente cadastrado com sucesso!")
    return redirect(url_for("clientes"))


@app.route("/clientes/deletar/<cpf>", methods=["POST"])
def deletar_cliente(cpf):
    dados = carregar_dados()
    if cpf not in dados["clientes"]:
        erro("Cliente não encontrado.")
        return redirect(url_for("clientes"))

    if any(conta.get("cliente_cpf") == cpf for conta in dados["contas"].values()):
        erro("Não é possível excluir: o cliente possui contas.")
        return redirect(url_for("clientes"))

    del dados["clientes"][cpf]
    salvar_dados(dados)
    ok("Cliente removido.")
    return redirect(url_for("clientes"))


@app.route("/agencias")
def agencias():
    dados = carregar_dados()
    return render_template(
        "agencias.html",
        agencia=dados["agencias"][AGENCIA_UNICA.codigo],
    )


@app.route("/contas")
def contas():
    dados = carregar_dados()
    return render_template(
        "contas.html",
        contas=dados["contas"],
        clientes=dados["clientes"],
        agencias=dados["agencias"],
        nomes=TIPOS_VALIDOS,
        permissoes=PERMISSOES,
    )


@app.route("/contas/cadastrar", methods=["POST"])
def cadastrar_conta():
    tipo = request.form.get("tipo")
    cliente_cpf = request.form.get("cliente_cpf")
    agencia_codigo = request.form.get("agencia_codigo")
    numero_conta = request.form.get("numero_conta", "").strip()

    try:
        saldo = round(
            float((request.form.get("saldo_inicial") or "0").replace(",", ".")), 2
        )
    except ValueError:
        saldo = -1

    dados = carregar_dados()
    if tipo not in TIPOS_VALIDOS:
        erro("Selecione um tipo de conta válido.")
        return redirect(url_for("contas"))

    if cliente_cpf not in dados["clientes"]:
        erro("Selecione um cliente cadastrado.")
        return redirect(url_for("contas"))

    if agencia_codigo not in dados["agencias"]:
        erro("Selecione uma agência cadastrada.")
        return redirect(url_for("contas"))

    if not numero_conta or numero_conta in dados["contas"]:
        erro("Número da conta vazio ou já cadastrado.")
        return redirect(url_for("contas"))

    if saldo < 0:
        erro("Saldo inicial inválido.")
        return redirect(url_for("contas"))

    dados["contas"][numero_conta] = {
        "numero_conta": numero_conta,
        "tipo": tipo,
        "cliente_cpf": cliente_cpf,
        "agencia_codigo": agencia_codigo,
        "saldo": saldo,
    }
    salvar_dados(dados)
    ok("Conta cadastrada com sucesso!")
    return redirect(url_for("contas"))


@app.route("/contas/<numero_conta>/<operacao>", methods=["POST"])
def operar_conta(numero_conta, operacao):
    if operacao not in TEXTO_OPERACAO:
        erro("Operação inválida.")
        return redirect(url_for("contas"))

    valor = ler_valor()
    if valor is None:
        erro("O valor informado é inválido.")
        return redirect(url_for("contas"))

    dados = carregar_dados()
    conta = dados["contas"].get(numero_conta)
    numero_destino = request.form.get("conta_destino", "").strip()
    conta_destino = (
        dados["contas"].get(numero_destino) if operacao == "transferencia" else None
    )

    if not conta:
        erro("Conta não encontrada.")
        return redirect(url_for("contas"))

    if operacao not in PERMISSOES.get(conta.get("tipo"), set()):
        erro(f"Este tipo de conta não permite {TEXTO_OPERACAO[operacao].lower()}.")
        return redirect(url_for("contas"))

    if operacao == "transferencia" and not conta_destino:
        erro("Conta de destino não encontrada.")
        return redirect(url_for("contas"))

    if operacao == "transferencia" and numero_destino == numero_conta:
        erro("A conta de destino deve ser diferente da conta de origem.")
        return redirect(url_for("contas"))

    if (
        operacao == "transferencia"
        and "deposito" not in PERMISSOES.get(conta_destino.get("tipo"), set())
    ):
        erro("A conta de destino não aceita transferências.")
        return redirect(url_for("contas"))

    if operacao in ("saque", "transferencia") and conta["saldo"] < valor:
        erro(f"Saldo insuficiente para realizar {TEXTO_OPERACAO[operacao].lower()}.")
        return redirect(url_for("contas"))

    if operacao == "saque":
        conta["saldo"] = round(conta["saldo"] - valor, 2)
    if operacao == "deposito":
        conta["saldo"] = round(conta["saldo"] + valor, 2)
    if operacao == "transferencia":
        conta["saldo"] = round(conta["saldo"] - valor, 2)
        conta_destino["saldo"] = round(conta_destino["saldo"] + valor, 2)
    if operacao == "rendimento":
        conta["saldo"] = round(conta["saldo"] * (1 + valor / 100), 2)

    salvar_dados(dados)
    ok(f"{TEXTO_OPERACAO[operacao]} realizado com sucesso!")
    return redirect(url_for("contas"))


@app.route("/contas/deletar/<numero_conta>", methods=["POST"])
def deletar_conta(numero_conta):
    dados = carregar_dados()
    if numero_conta not in dados["contas"]:
        erro("Conta não encontrada.")
        return redirect(url_for("contas"))

    del dados["contas"][numero_conta]
    salvar_dados(dados)
    ok("Conta removida.")
    return redirect(url_for("contas"))


@app.route("/relatorio")
def relatorio():
    dados = carregar_dados()
    registros = {}

    for tipo, nome in TIPOS_VALIDOS.items():
        contas_tipo = {
            numero: conta
            for numero, conta in dados["contas"].items()
            if conta.get("tipo") == tipo
        }
        saldos = [conta.get("saldo", 0) for conta in contas_tipo.values()]
        saldo_total = round(sum(saldos), 2)
        registros[tipo] = {
            "nome": nome,
            "contas": contas_tipo,
            "saldo_geral": saldo_total,
            "maior_saldo": max(saldos, default=0),
            "menor_saldo": min(saldos, default=0),
            "media": round(saldo_total / len(saldos), 2) if saldos else 0,
        }

    total_geral = round(
        sum(registro["saldo_geral"] for registro in registros.values()), 2
    )
    return render_template(
        "relatorio.html",
        clientes=dados["clientes"],
        agencias=dados["agencias"],
        registros=registros,
        total_geral=total_geral,
    )


if __name__ == "__main__":
    print("Servidor iniciado em http://127.0.0.1:5003")
    app.run(host="127.0.0.1", port=5003, debug=True)
