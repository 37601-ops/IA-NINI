import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# 1. ARQUITETURA DA REDE NEURAL (CRIADA DO ZERO)
class RedeVisaogEometrica(nn.Module):
    def __init__(self, tamanho_entrada, tamanho_oculto, tamanho_saida):
        super(RedeVisaogEometrica, self).__init__()
        # Primeira camada linear (conecta a entrada às variáveis ocultas)
        self.camada1 = nn.Linear(tamanho_entrada, tamanho_oculto)
        # Função de ativação para trazer não-linearidade (ajuda a IA a aprender padrões complexos)
        self.relu = nn.ReLU()
        # Segunda camada linear (conecta as variáveis ocultas à resposta final)
        self.camada2 = nn.Linear(tamanho_oculto, tamanho_saida)
        
    def forward(self, x):
        out = self.camada1(x)
        out = self.relu(out)
        out = self.camada2(out)
        return out

# 2. PROCESSADOR DE TEXTO (Conversor simples de palavras para números/vetores)
# Em um projeto real do zero, criamos um dicionário de palavras (Vocabulário)
vocabulario = {"calcular": 0, "area": 1, "quadrado": 2, "perimetro": 3, "triangulo": 4, "lado": 5, "base": 6, "altura": 7}

def vetorizar_texto(texto):
    vetor = np.zeros(len(vocabulario), dtype=np.float32)
    for palavra in texto.lower().split():
        if palavra in vocabulario:
            vetor[vocabulario[palavra]] +=
1.0
    return torch.tensor(vetor)

# Exemplo conceitual do loop de atendimento
def responder_cliente(mensagem_usuario):
    # 1. Identifica o que o usuário quer (Intenção)
    intencao = modelo_intent(mensagem_usuario) 
    
    if intencao == "buscar_produto":
        # 2. Busca os dados direto no seu banco de dados (Backend)
        dados_produtos = backend.buscar_no_catalogo(mensagem_usuario)
        
        # 3. Alimenta a IA Generativa com o contexto real do banco
        prompt_final = f"Produtos encontrados: {dados_produtos}. Responda ao cliente: {mensagem_usuario}"
        resposta = modelo_gerativo.generate(prompt_final)
        
    elif intencao == "status_pedido":
        # Busca informações logísticas
        status = backend.verificar_pedido(usuario_id)
        resposta = f"Identifiquei aqui que seu pedido está: {status}."
        
    else:
        # Conversa fiada / Saudações / Dúvidas gerais
        resposta = modelo_gerativo.generate(mensagem_usuario)
        
    return resposta


# 3. PREPARAÇÃO DOS DADOS DE TREINO (Exemplos para a IA aprender)
# Cada entrada é um vetor de texto + duas variáveis numéricas (ex: base e altura, ou lado)
# Formato dos dados: [vetor_texto, valor1, valor2] -> Classe Alvo (0: Área Quadrado, 1: Perímetro Quadrado, 2: Área Triângulo)
dados_treino = [
    ("calcular area quadrado lado", 5.0, 0.0, 0),
    ("area quadrado", 10.0, 0.0, 0),
    ("calcular perimetro quadrado lado", 4.0, 0.0, 1),
    ("perimetro quadrado", 7.0, 0.0, 1),
    ("calcular area triangulo base altura", 6.0, 4.0, 2),
    ("area triangulo base altura", 10.0, 5.0, 2)
]

X_treino = []
y_treino = []

for texto, v1, v2, classe in dados_treino:
    vetor_txt = vetorizar_texto(texto)
    # Junta as características de texto com os dados numéricos do problema geométrico
    caracteristicas = torch.cat((vetor_txt, torch.tensor([v1, v2], dtype=torch.float32)))
    X_treino.append(caracteristicas)
    y_treino.append(classe)

X_treino = torch.stack(X_treino)
y_treino = torch.tensor(y_treino, dtype=torch.long)

# 4. CONFIGURAÇÃO DO TREINAMENTO
TAMANHO_ENTRADA = len(vocabulario) + 2 # Palavras + 2 valores numéricos
TAMANHO_OCULTO = 16
TAMANHO_SAIDA = 3 # 3 classes de problemas geométricos

modelo = RedeVisaogEometrica(TAMANHO_ENTRADA, TAMANHO_OCULTO, TAMANHO_SAIDA)
criterio_perda = nn.CrossEntropyLoss() # Mede o quão errada a IA está
otimizador = optim.Adam(modelo.parameters(), lr=0.01) # Ajusta os pesos matemáticos

# 5. LOOP DE TREINAMENTO (A IA rodando os dados e aprendendo com os erros)
print("Treinando a inteligência artificial geométrica...")
for epoca in range(200):
    otimizador.zero_grad()
    saidas = modelo(X_treino)
    perda = criterio_perda(saidas, y_treino)
    perda.backward() # Algoritmo de Backpropagation (retropropagação do erro)
    otimizador.step() # Atualiza os pesos neurais

print("Treinamento concluído com sucesso!\n")

# 6. MOTOR DE CÁLCULO (Executado após a interpretação da IA)
def executar_calculo_geometrico(classe_prevista, v1, v2):
    if classe_prevista == 0:
        return f"Área do Quadrado: {v1 * v1} cm²"
    elif classe_prevista == 1:
        return f"Perímetro do Quadrado: {4 * v1} cm"
    elif classe_prevista == 2:
        return f"Área do Triângulo: {(v1 * v2) / 2} cm²"
    return "Falha ao interpretar a geometria."

# 7. TESTANDO A IA COM UM PROBLEMA INÉDITO
texto_teste = "calcular area quadrado"
valor1_teste = 8.0
valor2_teste = 0.0 # Quadrado só precisa de 1 valor

vetor_teste = vetorizar_texto(texto_teste)
entrada_teste = torch.cat((vetor_teste, torch.tensor([valor1_teste, valor2_teste], dtype=torch.float32)))

# Faz a previsão sem atualizar os pesos
with torch.no_grad():
    previsao = modelo(entrada_teste)
    classe_escolhida = torch.argmax(previsao).item()

# Resultado final interpretado e calculado pela sua própria IA
print(f"Enunciado recebido: '{texto_teste}' com valor {valor1_teste}")
print(f"Classe identificada pela IA: {classe_escolhida}")
resultado_final = executar_calculo_geometrico(classe_escolhida, valor1_teste, valor2_teste)
print(f"Resultado do cálculo: {resultado_final}")
