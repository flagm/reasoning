import re
import numpy as np
def eliminate_implication(formula):
    formula = re.sub(r'(\w+\(\w+\))\s*=>\s*(\w+\(\w+\))', r'~\1 | \2', formula)
    return formula

def move_negation_inward(formula):
    formula = re.sub(r'(.*?)', r'\1', formula)
    formula = re.sub(r'\((.?) & (.?)\)', r'(\1 | ~\2)', formula)

    formula = re.sub(r'\((.?) \| (.?)\)', r'(\1 & ~\2)', formula)

    formula = re.sub(r'∃(.?) (.?)\)', r'∀\1\2)', formula)

    formula = re.sub(r'∀(.?) (.?)\)', r'∃\1\2)', formula)

    return formula
def Remove_double_negation(formula):
    formula = re.sub(r'(.*?)', r'\1', formula)
    return formula
def prenex(formula):
    formula_list = [char for char in formula]
    golden_list = []
    i = 0
    while i < len(formula_list):
        if formula_list[i] == "∃" or formula_list[i] == "∀":
            golden_list += [formula_list[i] + formula_list[i + 1]]
            i += 1
        i += 1
    formula=Skolemization(formula)
    formula=Remove_Universal(formula)
    golden_list+=[formula]
    formula = ' '.join(golden_list)
    return formula
def Skolemization(formula):
    formula = re.sub(r'∃.', r'', formula)
    return formula
def Standardize(sentence):
    sentence=[char for char in sentence]
    golden_variables=[]
    for i in range(len(sentence)):
        if sentence[i]=="∃" or sentence[i]=="∀":
            golden_variables+=[sentence[i+1]]
    n=np.unique(golden_variables)
    s_list=['o','y','z','u','p','k','l']
    k=0
    n=0
    for i in range(len(sentence)):
        if sentence[i-1]=="∃" or sentence[i-1]=="∀":
            n+=1

        if sentence[i]==golden_variables[0] and n>1:
            if sentence[i-1]=="∃" or sentence[i-1]=="∀":
                k += 1
                sentence[i]=s_list[k]
            elif k>0:
                sentence[i] = s_list[k]
    sentence = ''.join(sentence)
    return sentence
def Remove_Universal(formula):
    formula = re.sub(r'∀.', r'', formula)
    return formula
def distribute_disjunctions(formula):
    match = re.search(r'(\w+\([^)]\))\s\|\s*\((.?)\s&\s*(.*?)\)', formula)
    while match:
        left_part = match.group(1)
        conjunction_part = match.group(2)
        right_part = match.group(3)
        distributed_formula = f"({left_part} | {conjunction_part}) & ({left_part} | {right_part})"
        formula = formula[:match.start()] + distributed_formula + formula[match.end():]
        match = re.search(r'(\w+\([^)]\))\s\|\s*\((.?)\s&\s*(.*?)\)', formula)
    return formula

def clauses(formula):
    formula_list = [char for char in formula]
    small_list=[]
    big_list=[]
    for i in range(len(formula_list)):
        if formula_list[i]!= "&":
            small_list+=[formula_list[i]]

        else:
            word = ''.join(small_list)
            big_list+=[word]
            small_list=[]
        if (i+1)==len(formula_list):
            word = ''.join(small_list)
            big_list+=[word]
            small_list=[]

    return big_list
def Rename_clauses(big_list):
    s_list=['x','y','z','u','p','k','l']
    golden_values=[]
    for i in range(len(big_list)):
        match = re.findall(r'\(([^()]+)\)', big_list[i])
        unique_values_set = set(match)
        unique_values_list = list(unique_values_set)
        golden_values+=[unique_values_list]
    for i in range(len(big_list)):
        new_text = re.sub(r'\(([^()]+)\)', "("+s_list[i]+")", big_list[i])
        big_list[i] = new_text
    return big_list
f="∃  ∀"
formula = "∀x(S(x) | (P(x) => Q(x))) | ~~∃x P(x) | (R(x) & S(x))"
step1=clauses(formula)
cnf_formula = Rename_clauses(step1)

step1=eliminate_implication(formula)
print(step1)
step2=move_negation_inward(step1)
print(step2)
step3=move_negation_inward(step2)
print(step3)
step4=Standardize(step3)
print(step4)
step5=prenex(step4)
print(step5)
step6=Skolemization(step5)
print(step6)
step7=Remove_Universal(step6)
print(step7)
step8=distribute_disjunctions(step7)
print(step8)
step9=clauses(step8)
print(step9)
step10=Rename_clauses(step9)
print("output:-")
for item in step10:
    print(item)
