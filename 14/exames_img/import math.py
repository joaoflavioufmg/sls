import math

# Dados da tabela
dados = [
    (331, 4.35045317220544),
    (360, 4),
    (251, 5.73705179282869),
    (244, 5.9016393442623),
    (360, 4),
    (378, 3.80952380952381),
    (407, 3.53808353808354),
    (340, 4.23529411764706),
    (382, 3.7696335078534),
    (255, 5.64705882352941),
    (233, 6.18025751072961),
    (412, 3.49514563106796),
    (291, 4.94845360824742),
    (330, 4.36363636363636),
    (262, 5.49618320610687),
    (372, 3.87096774193548),
    (294, 4.89795918367347),
    (315, 4.57142857142857),
    (343, 4.19825072886297),
    (394, 3.65482233502538),
    (345, 4.17391304347826),
    (330, 4.36363636363636),
    (386, 3.73056994818653),
    (242, 5.9504132231405),
    (274, 5.25547445255474),
    (357, 4.03361344537815),
    (303, 4.75247524752475),
    (347, 4.14985590778098),
    (313, 4.60063897763578),
    (327, 4.40366972477064),
    (270, 5.33333333333333)
]

# Gerar o conteúdo do arquivo
linhas = []
for num_vezes, valor in dados:
    # Arredondar para baixo com 2 casas decimais
    valor_floor = math.floor(valor * 100) / 100
    # Formatar com ponto como separador decimal
    valor_formatado = f"{valor_floor:.2f}"
    # Adicionar o valor repetido
    for _ in range(int(num_vezes)):
        linhas.append(valor_formatado)

# Salvar em arquivo
with open('valores.txt', 'w') as f:
    f.write('\n'.join(linhas))

print(f"Arquivo gerado com sucesso!")
print(f"Total de linhas: {len(linhas)}")
print(f"\nPrimeiras 10 linhas:")
for i in range(min(10, len(linhas))):
    print(linhas[i])
print(f"\nÚltimas 10 linhas:")
for i in range(max(0, len(linhas)-10), len(linhas)):
    print(linhas[i])