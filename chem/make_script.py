def clean_lines(input_lines):
    out_lines = []
    for line in input_lines:
        if line.startswith("from chem."):
            continue
        if line.endswith("\n"):
            pass
        else:
            line = line+"\n"
        out_lines.append(line)
    return out_lines

def input_script_name(script_file):
    model_lines = clean_lines(open("models.py").readlines())
    util_lines = clean_lines(open("utils.py").readlines())
    script_lines = clean_lines(open(script_file).readlines())
    model_lines.extend(util_lines)
    model_lines.extend(script_lines)
    out_file = open(script_file.replace(".py","_compiled.py"),"w")
    out_file.writelines(model_lines)

if __name__ == "__main__":
    import sys
    input_script_name(sys.argv[1])
