from crome_logic.specification.temporal import LTL

output_file = "example_g.txt"

if __name__ == '__main__':
    with open(output_file) as f:
        lines = f.readlines()
        print(lines[0])
        ltl = LTL(_init_formula=lines[0])
        print(ltl)



