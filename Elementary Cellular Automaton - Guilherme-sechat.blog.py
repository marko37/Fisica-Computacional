import matplotlib.pyplot as plt
import numpy as np
import sys

# This code was created by Guilherme Vieira
# (@guilhermewells/sechat.blog for the youtube channel
# https://www.youtube.com/user/guilhermewellsful), please don't
# remove this message.

# Procurei seguir a PEP 8 (https://www.python.org/dev/peps/pep-0008/),
# que é só uma recomendação, não uma obrigação. O que procurei seguir:
#
# - Tabulação de 4 espaços
# - Linhas com no máximo 72 caracteres
# - Nomes:
#   Classes: CamelCase
#   Metodos e funções: lower_case_with_underscores
#   Atributos e variáveis: lower_case_with_underscores
# - Um espaço depois de , e :


class Rule:
    """ These are the following rules for elementary celular automata
    and totalistic cellular automata. Each method tells about
    one of them"""

    # Em regra1, os arrays ca e ca_new são formados por str,
    # assim menos conversões são feitas na execução.
    # Em regra2, esses arrays são formados por int.
    
    def __init__(self, value):
        self.value = value
        # Creating the first line for each iteration
        self.ca = ['0'] * (2*size + 2)

    # Elementary cellular automata
    def regra1(self):
        # The middle term is set to be 1
        # Parece que há uma falha aqui, porque o valor 1 é
        # atribuído em cada iteração, sendo que isso era 
        # para acontecer só na primeira, não é?
        # O mesmo acontece no Modo 2.
        self.ca[int((2*size+2)/2)] = '1'
        ca_new = ['0']
        
        # Transforming into binary and
        # keeping fixed the number of digits
        x = '{0:08b}'.format(self.value)
        
        # A dictionary for the rules
        comb = {'111': x[0], '110': x[1], '101': x[2], '100': x[3],
                '011': x[4], '010': x[5], '001': x[6], '000': x[7]}
        
        for i in range(1, (2*size+2)-1):
            # Here we apply the rules according to 'comb'
            y = self.ca[i-1] + self.ca[i] + self.ca[i+1]
            ca_new.append(comb[y])
        ca_new.append('0')
        self.ca = ca_new

    # Totallistic cellular automata
    def regra2(self):
        
        self.ca = list(map(int, self.ca))
        
        self.ca[int((2*size+2)/2)] = 2
        ca_new = [0]

        # Seria melhor colocar este método fora de regra2,
        # assim a regra2 fica menor.
        # Transforming into ternary
        # https://www.codevscolor.com/
        # python-convert-decimal-ternarybase-3/
        def find_ternary(b):
            quotient = b/3
            remainder = b%3
            if quotient == 0:
                return ""
            else:
                return find_ternary(int(quotient)) + str(int(remainder))
        

        x = find_ternary(self.value).zfill(7)
        
        # A dictionary for the rules
        comb = {6: int(x[0]), 5: int(x[1]), 4: int(x[2]), 3: int(x[3]),
                2: int(x[4]), 1: int(x[5]), 0: int(x[6])}
        
        for i in range(1, (2*size+2)-1):
            # Here we apply the rules according to 'comb'
            y = self.ca[i-1] + self.ca[i] + self.ca[i+1]
            ca_new.append(comb[y])
        ca_new.append(0)
        self.ca = ca_new


if len(sys.argv) > 1:
    size = int(sys.argv[1])
    regra = sys.argv[2]
    rules = Rule(int(sys.argv[3]))
    
else:

    size = int(input('What is the size of the grid? '))

    # We will get the final size, or a time step, then choose the
    # elementary cellular automaton(Modo1) or the totallistic cellular
    # automaton (Modo2).
    regra = input('Modo 1(ECA) or Modo 2(TCA)? ')

    if regra == 'Modo1':
        rules = Rule(int(input(
            'Diga uma regra de automata, de 0 a 256: ')))
    elif regra == 'Modo2':
        rules = Rule(int(input(
            'Diga uma regra de automata totalista, de 0 a 6561: ')))
        
# The 'rules' set the entrance rule for nearest neighborhoods for each
# case(Modo), the loop bellow makes the updates into a matrix for the
# chosee Rule and "Modo"

for j in range(size):
    if j == 0:
        # Há uma falha aqui, o valor central é atribuido só depois.
        # Agora rules.ca é só um array de zeros.
        # As funções list e map aqui convertem de str para int.
        A = [list(map(int, rules.ca))]

    if regra == 'Modo1':
        # Como eu coloquei a conversão de str para int antes,
        # o valor central não é alterado pela regra1,
        # então coloquei este comando para fazer isso.
        A[0][int((2*size + 2) / 2)] = 1
        rules.regra1()
    elif regra == 'Modo2':
        # O mesmo que a situação anterior.
        A[0][int((2*size + 2) / 2)] = 2
        rules.regra2()
    A = np.insert(A, [j+1], [rules.ca], axis=0)
    # Just another way of including the terms
    # A = np.vstack((A, rules.ca)).astype(float)

fig, ax = plt.subplots(1, 1, dpi=120)
ax.imshow(A, interpolation='nearest')

prog_name=sys.argv[0].split('.')[0]
fig.savefig('folder/it' + str(j) + '.png')
plt.show()
