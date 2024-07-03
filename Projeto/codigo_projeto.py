import matplotlib.pyplot as plt
import pandas as pd

DENSIADADE_DO_AR = 1.225
GRAVIDADE = 9.80665
MASSA_FOGUETE = float(input('informe a massa do foguete em kg: '))
PESO_FOGUETE = MASSA_FOGUETE * GRAVIDADE
VELOCIDADE_TERMINAL = float(input('informe a velocidade terminal desejada para o foguete em m/s: '))
ESTABILIDADE = int(input('(1)baixo - (2)médio - (3)alto\ninforme o nível de estabilidade desejado, de acordo com os números acima: '))
ARRASTO = int(input('(1)baixo - (2)médio - (3)alto\ninforme o nível de arrasto desejado, de acordo com os números acima: '))

# Base de dados: [ nome da geometria, nível de estabilidade, coeficiente de arrasto médio, nível de confiabilidade, arrasto mínimo, arrasto máximo]

geometrias = [['flat circular',               0.04, 0.775, 1, 0.75, 0.80], 
               ['conical',                    0.05, 0.825, 1, 0.75, 0.90],
               ['biconical',                  0.05, 0.835, 1, 0.75, 0.92],
               ['triconical',                 0.05, 0.880, 1, 0.80, 0.96],
               [r'extended skirt 10% flat',   0.08, 0.825, 1, 0.78, 0.87],
               [r'extended skirt 14.3% full', 0.08, 0.825, 1, 0.75, 0.90],
               ['hemisferical',               0.08, 0.695, 1, 0.62, 0.77],
               ['guide surface (ribbed)',     1.00, 0.350, 1, 0.28, 0.42],
               ['guide surface (ribless)',    0.66, 0.320, 1, 0.30, 0.34],
               ['annular',                    0.33, 0.900, 1, 0.85, 0.95],
               ['cross',                      0.66, 0.725, 1, 0.60, 0.85]]

# Dimensionamento
# calculando a área da superfície mínima e máxima

areas_superfície = []
for i in range(len(geometrias)):
    AREA_SUPERFICIE_PQD_MAX = 2 * PESO_FOGUETE / (VELOCIDADE_TERMINAL ** 2 * DENSIADADE_DO_AR * geometrias[i][4])
    AREA_SUPERFICIE_PQD_MIN = 2 * PESO_FOGUETE / (VELOCIDADE_TERMINAL ** 2 * DENSIADADE_DO_AR * geometrias[i][5])
    areas_superfície.append((round(AREA_SUPERFICIE_PQD_MIN, 2), round(AREA_SUPERFICIE_PQD_MAX, 2)))

# imprimindo os valores obtidos
for j in range(len(geometrias)):
    print(f'{geometrias[j][0]:<25}:{areas_superfície[j]} metros quadrados.')

# Cálculo da eficiência
def ordenacao(geometrias: list, x: int):  # normalização dos dados
    lista_nordenada = [geometrias[p][x] for p in range(len(geometrias))]
    return sorted(lista_nordenada)

estabilidade_ordenada = ordenacao(geometrias, 1)
arrasto_ordenado = ordenacao(geometrias, 2)

def normalizacao(x: int, y: list):
    return [round((geometrias[i][x] - y[0]) / (y[-1] - y[0]), 2) for i in range(len(geometrias))]

estabilidade_normalizada = normalizacao(1, estabilidade_ordenada)
arrasto_normalizado = normalizacao(2, arrasto_ordenado)

eficiencia = []  # avaliação da eficiência: estabilidade + arrasto + confiabilidade
for i in range(len(geometrias)):
    eficiencia.append(round(estabilidade_normalizada[i] * ESTABILIDADE + arrasto_normalizado[i] * ARRASTO + geometrias[i][3], 2))

# Preparação dos dados para o gráfico
nome_geometrias = [geometria[0] for geometria in geometrias]

df = pd.DataFrame({'geometria': nome_geometrias, 'eficiência': eficiencia})
df = df.sort_values(by='eficiência', ascending=False)
df['cum (%)'] = df['eficiência'].cumsum() / df['eficiência'].sum() * 100

# Criação do gráfico de Pareto
plt.rcParams.update({'font.size': 10})
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.set_title('Pareto')
color1 = 'royalblue'

ax1.set_ylabel('eficiência', color=color1)
ax1.bar(df['geometria'], df['eficiência'], color=color1, edgecolor='royalblue', linewidth=2, hatch='*')
ax1.tick_params(axis='y', labelcolor=color1)

color2 = 'black'
ax2 = ax1.twinx()
ax2.set_ylabel('%', color=color2)
ax2.plot(df['geometria'], df['cum (%)'], color=color2, marker='s', markersize=8, linestyle='-')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_ylim([0, 105])  # Ajuste do limite superior para 105%
ax2.set_yticks(range(0, 101, 20))  # Define de 0 a 100%

for tick in ax1.get_xticklabels():
    tick.set_rotation(60)

plt.savefig('GraficoPareto.png', format='png', dpi=600, bbox_inches='tight')
plt.show()