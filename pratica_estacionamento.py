
from abc import ABC, abstractmethod

def reais(centavos: int) -> str:
    return f"R$ {centavos // 100},{centavos % 100:02d}"

# Q1 - CLASSE ABSTRATA VEICULO

class Cobravel(ABC):

    @abstractmethod
    def valor(self) -> int:
        pass
    @abstractmethod
    def descricao(self) -> str:
        pass

class Veiculo(Cobravel):
    def __init__(self, placa: str, horas: int = 0) -> None:
        self.placa = placa.strip().upper()
        self.horas = horas
    @abstractmethod
    def tarifa_hora(self) -> int:
        pass
    @abstractmethod
    def tipo(self) -> str:
        pass
    def valor(self) -> int:
        return self.tarifa_hora() * self.horas
    def descricao(self) -> str:
        return f"{self.tipo()} {self.placa} ({self.horas}h)"
    def __str__(self) -> str:
        return f"{self.descricao():<40} {reais(self.valor())}"

# Teste de erro da Q1:
# veiculo = Veiculo("abc1d23")
# TypeError: não é possível instanciar uma classe abstrata.


# Q2 - HERANÇA: CARRO, MOTO E CAMINHAO
class Carro(Veiculo):
    def tarifa_hora(self) -> int:
        return 1000
    def tipo(self) -> str:
        return "Carro"

class Moto(Veiculo):
    def tarifa_hora(self) -> int:
        return 500
    def tipo(self) -> str:
        return "Moto"
    def valor(self) -> int:
        return max(0, super().valor() - self.tarifa_hora())

class Caminhao(Veiculo):
    def __init__(self, placa: str, eixos: int, horas: int = 0) -> None:
        super().__init__(placa, horas)
        self.eixos = eixos
    def tarifa_hora(self) -> int:
        return 800 * self.eixos
    def tipo(self) -> str:
        return f"Caminhao {self.eixos} eixos"

# Q3 - SOBRESCRITA COM SUPER()
class CarroEletrico(Carro):
    def tarifa_hora(self) -> int:
        return super().tarifa_hora() // 2
    def tipo(self) -> str:
        return "Carro eletrico"

# Q4 - POLIMORFISMO
def relatorio(veiculos: list[Veiculo]) -> int:
    total = 0
    for veiculo in veiculos:
        print(veiculo)
        total += veiculo.valor()
    print(f"total: {reais(total)}")
    return total

# Q5 - MAIS CARO, FILTRO E CLASSE VAN
def mais_caro(veiculos: list[Veiculo]) -> Veiculo:
    maior = veiculos[0]
    for veiculo in veiculos:
        if veiculo.valor() > maior.valor():
            maior = veiculo
    return maior
def filtrar_por_valor(veiculos: list[Veiculo], minimo: int) -> list[Veiculo]:
    resultado = []
    for veiculo in veiculos:
        if veiculo.valor() >= minimo:
            resultado.append(veiculo)
    return resultado

class Van(Veiculo):
    def tarifa_hora(self) -> int:
        return 1200
    def tipo(self) -> str:
        return "Van"

# Q6 - TOTAL DE EIXOS
def total_eixos(veiculos: list[Veiculo]) -> int:
    total = 0
    for veiculo in veiculos:
        if isinstance(veiculo, Caminhao):
            total += veiculo.eixos
    return total

# Q7 - INTERFACE COBRAVEL E LAVAGEM
class Lavagem(Cobravel):
    def __init__(self, placa: str, completa: bool) -> None:
        self.placa = placa.strip().upper()
        self.completa = completa
    def valor(self) -> int:
        if self.completa:
            return 6000
        return 2500
    def descricao(self) -> str:
        if self.completa:
            return f"Lavagem completa {self.placa}"
        return f"Lavagem simples {self.placa}"
    def __str__(self) -> str:
        return f"{self.descricao():<40} {reais(self.valor())}"

def fechar_caixa(itens: list[Cobravel]) -> int:
    total = 0
    for item in itens:
        print(item)
        total += item.valor()
    print(f"caixa do dia: {reais(total)}")
    return total

# Q8 - CLASSE PATIO
class Patio:
    def __init__(self, capacidade: int) -> None:
        self.capacidade = capacidade
        self.veiculos: list[Veiculo] = []
    def entrar(self, veiculo: Veiculo) -> bool:
        for atual in self.veiculos:
            if atual.placa == veiculo.placa:
                print(f"veiculo {veiculo.placa} ja esta no patio")
                return False
        if len(self.veiculos) >= self.capacidade:
            print(f"patio lotado: {veiculo.placa} nao entrou")
            return False
        self.veiculos.append(veiculo)
        return True

    def sair(self, placa: str, horas: int) -> int:
        placa = placa.strip().upper()
        for veiculo in self.veiculos:
            if veiculo.placa == placa:
                veiculo.horas = horas
                valor = veiculo.valor()
                self.veiculos.remove(veiculo)
                return valor
        print(f"veiculo {placa} nao encontrado")
        return 0

    def ocupacao(self) -> str:
        return f"{len(self.veiculos)}/{self.capacidade} vagas ocupadas"

# Teste da Q2
gol = Carro("abc1d23", 3)
scania = Caminhao("cam7f89", 3, 2)
print(gol)
print(scania)

# Teste da Q3
biz = Moto("mot4e56", 2)
leaf = CarroEletrico("ele1t11", 3)
rapida = Moto("rap2d22", 1)
print(biz)
print(leaf)
print(rapida)

# Teste da Q4
dia: list[Veiculo] = [gol, biz, scania, leaf, rapida]
print("Relatorio do dia:")
total_dia = relatorio(dia)

# Teste da Q5
dia.append(Van("van3c33", 4))
print("mais caro:", mais_caro(dia))
for v in filtrar_por_valor(dia, 3000):
    print(v)

# Teste da Q6
print("Total de eixos:", total_eixos(dia))

# Teste da Q7
itens: list[Cobravel] = [gol, Lavagem("abc1d23", completa=True), biz, Lavagem("mot4e56", completa=False)]
print("Fechamento do caixa:")
total_caixa = fechar_caixa(itens)

# Teste da Q8
patio = Patio(2)
patio.entrar(Carro("aaa1a11"))
patio.entrar(Moto("bbb2b22"))
patio.entrar(Van("ccc3c33"))
print(patio.ocupacao())
print("saida AAA1A11:", reais(patio.sair("aaa1a11", 2)))
print(patio.ocupacao())
