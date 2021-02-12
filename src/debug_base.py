import numpy as np
import re
import os
####### Inicio ###########

### TODO - make the relatable parameters a dynamic function, maybe a can digest the files as txt and parse them....that could work



#Relação entre nome das variáveis do paython e o nome das variáveis recebidas pelo fortran budget.f90
#A ordem das variáveis está conforme elas precisam estar para chamar a subrotina daily_budget
#É um array onde cada elemento é um array de duas posições, 
# na posição [0] é o nome da variável no python e 
# no [1] é o nome da variábel na budget.f90
# relatable_parameters = [
#        ["pls_table", "dt"], 
#        ['wfim',"w1"], 
#        ['gfim',"g1"], 
#        ['sfim',"s1"],
#        ['soil_temp',"ts"], 
#        ['temp[step]',"temp"],
#        ['prec[step]',"prec"],
#        ['p_atm[step]',"p0"],
#        ['ipar[step]',"ipar"], 
#        ['ru[step]',"rh"], 
#        ['sp_available_n',"mineral_n"], 
#        ['sp_available_p',"labile_p"],
#        ['ton', "on"], 
#        ['top',"sop"], 
#        ['sp_organic_p',"op"], 
#        ['co2', "catm"], 
#        ['sto', "sto_budget_in"], 
#        [ 'cleaf', "cl1_in"], 
#        ['cwood', "ca1_in"], 
#        ['croot', "cf1_in"], 
#        ['csap', "cs1_in"], 
#        ['cheart', "ch1_in"], 
#        ['dcl', "dleaf_in"],
#        ['dca', "dwood_in"], 
#        ['dcf',"droot_in"], 
#        ['uptk_costs',"uptk_costs_in"]
# ]

# Essa é a lista de nomes de variáveis do arquivo debug_caete.f90
debug_variable_names = ['dt', 'w1', 'g1', 's1', 'ts', 'temp', 'prec', 'p0', 'ipar', 'rh',
         'mineral_n', 'labile_p', 'on', 'sop', 'op', 'catm', 'sto_budg', 'cl1_pft', 
         'ca1_pft', 'cf1_pft', 'cs1', 'ch1', 'dleaf', 'dwood','droot', 'uptk_costs']

# Como o fortran tem um número máximo de colunas por linha, essa função garante
# que as linhas não sejam muito grandes e adiciona o & para o fortran entender a quebra de linha
# No caso aqui ele quebra de linha a cada 5 valores
def format_values(values, every=3):
       lines = []
       for i in range(0, len(values), every):
              lines.append(', '.join(values[i:i+every]))
       return ",&\n ".join(lines)

# Esse loop vasculha a variável data e para cada variável constrói uma string que pode ser usada para 
# setar a variável no fortran.
def format_for_fortran(data_array, relatable_parameters):
       formated_data = []
       for index, item in enumerate(data_array):
              
              if type(item) == list: item = np.array(item)
              if type(item) == list or type(item) == np.ndarray:
                     farray = np.asfortranarray(item)
                     formated_forf = ''
                     fortran_value = []
                     for kk in np.nditer(farray, order="F"): 
                            formated_forf += f"{kk}, "
                            fortran_value.append(f"{kk}") 
                     
                     f_string = format_values(fortran_value)
                     # Essa linha cria a declaração da variável com o nome que ela tem dentro da subrotina daily_budget, tipo droot_in
                     formated_data.append(f"{relatable_parameters[index][1]} = reshape((/{f_string}/),shape({relatable_parameters[index][1]}))")
                     
                     # Essa linha cria o arquivo txt com a a inicialização das variáveis de acordo com o nome no debug_caete.f90
                     #formated_data.append(f"{debug_variable_names[index]} = reshape((/{f_string}/),shape({debug_variable_names[index]}))")
              else:
                     formated_data.append(f"{relatable_parameters[index][1]} = {item}")
                     
       return formated_data

def get_budget_call_from_python():
       f = open('caete.py','r')
       file_string = f.read()
       f.close()
       call_matches = re.findall("out = model.daily_budget\([\w\.,$\s\[\]]*\)", file_string)
       variable_list = call_matches[0].replace('out = model.daily_budget(','').replace('\n','').replace(' ','').replace(')','')
       
       variable_list_with_self_and_step = variable_list.split(',')
       variable_names_list = variable_list.replace('self.','').replace('[step]','').split(',')
       return variable_list_with_self_and_step

def get_budget_definition_from_fortran():
       f = open('budget.f90')
       file_string = f.read()
       f.close()
       definition_matches = re.findall("subroutine daily_budget\([\w\s,&_]*\)", file_string)
       variable_list = definition_matches[0].replace('subroutine daily_budget(','').replace(')','').replace('&','').replace('\n','').replace(' ','').split(',')
       
       return variable_list

def build_relatable_params(python_params, fortran_params):
       both_params = []
       
       for i,o in enumerate(python_params):
              both_params.append([python_params[i], fortran_params[i]])
       return both_params

def save_step_values_to_txt(step_array, step):
       fortran_budget_variable_list = get_budget_definition_from_fortran()
       python_budget_variable_list = get_budget_call_from_python()

       relatable_parameters = build_relatable_params(python_budget_variable_list, fortran_budget_variable_list)

       formated_for_fortran = format_for_fortran(step_array, relatable_parameters)

       

       if not os.path.exists('../fortran_tests'):
              os.makedirs('../fortran_tests')
       
       # Printa as strings que podem ser usadas para inicializar as variáveis no fortran.
       # Esse loop printa o texto formatado tanto no arquivo test_budget_values.txt
       # quanto no terminal

       f = open(f"../fortran_tests/test_budget_values_step_{step}.txt",'w')
       print(f"!!!!!!!      Step = {step}  !!!!!!!!!!!!!!!", file=f)
       print(f"!!!!!!!      Step = {step}  !!!!!!!!!!!!!!!")
       for item in formated_for_fortran:
              print(item, file=f)
              print("\n", file=f)
              print(item)
              print("\n")

       f.close()
       print('Step saved in ')
