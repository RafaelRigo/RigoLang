import sys
import sympy
import re

program_filepath = sys.argv[1]
program_lines = []

alphabet = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'
varstart = alphabet.split(' ')

variables = {'a': '1'}

def error(line, line_index, message):
    print(f"Error in file {program_filepath}, line {line_index}:")
    print(f"\t{line}")
    print("\t" + "^" * len(line))
    print(message)
    sys.exit()

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def main() -> None:

    with open(program_filepath, 'r') as program_file:
        program_lines = [line.strip() for line in program_file.readlines()]

    a = ""
    for line in program_lines:
        a += line + '\n'

    code = a.split('\n')

    for i in code:

        if i == '':
            continue

        elif i.split('~')[0].strip() == 'writeLn':
            output = i.split('~')[1].strip()
            if output.startswith('"') and output.endswith('"'):
                slash = False
                for a in output:
                    if a == '\\':
                        slash = True
                    elif a == 'n' and slash:
                        print('\n', end='')
                        slash = False
                    elif a == '"' and slash:
                        print(a, end='')
                        slash = False
                    elif a != '"':
                        print(a, end='')
                print()
            else:
                if output in variables.keys():
                    output = variables[output]
                    slash = False
                    for a in output:
                        if a == '\\':
                            slash = True
                        elif a == 'n' and slash:
                            print('\n', end='')
                            slash = False
                        elif a == '"' and slash:
                            print(a, end='')
                            slash = False
                        elif a != '"':
                            print(a, end='')
                    print()

                elif output.isnumeric() or is_float(output):
                    print(output)

                elif '+' in output or '-' in output or '*' in output or '/' in output:
                    for item in re.split(r'[*+/-]', output):
                        if item.isnumeric() or is_float(item):
                            continue
                        else:
                            if item.strip() in variables.keys():
                                output = output.replace(item.strip(), variables[item.strip()])
                            else:
                                error(i, code.index(i), f"var {item} is not defined...")
                    if is_float(str(sympy.sympify(output))):
                        print(str(sympy.sympify(output)).split(".")[0] + "." + str(sympy.sympify(output)).split(".")[1].rstrip('0'))
                    else:
                        print(sympy.sympify(output))

                elif output[0] in varstart:
                    if output.strip() in variables.keys():
                        output = variables[output.strip()]
                        print(output)

                    elif len(output.split(' ')) > 1:
                        error(i, code.index(i), "Incorrect syntax")

                    else:
                        error(i, code.index(i), f"var {output} is not defined...")

                else:
                    error(i, code.index(i), "Incorrect syntax")

        elif i.split('=')[0].strip()[0] in varstart:
            var_name = i.split('=')[0].strip()
            value = i.split('=')[1].strip()
            if value.startswith('"') and value.endswith('"'):
                variables[var_name] = value

main()