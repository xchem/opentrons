import json,os

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

def generate_reagent_text(reagent):
    """
    reagent_1 = Reagent(reagent_name="amines", plate_location="B1", plate_type='FluidX_24_5ml',
                    csv_data=csv_data)
    :param reagent:
    :return:
    """
    reagent_name = reagent["reagent_name"].replace("-","_")
    plate_type = reagent["plate_type"]
    plate_location = reagent["plate_location"]
    csv_path = None
    if "csv_path" in reagent:
        my_csv_path = os.path.join(*reagent["csv_path"])
        csv_path = reagent_name +'_DATA="""'+open(my_csv_path).read()+'"""\n'
        script_path = reagent_name + '= Reagent(reagent_name="'+reagent_name+'", plate_location="'+\
                  plate_location+'", plate_type="'+plate_type+'",csv_data='+reagent_name+"_DATA)"
    else:
        script_path = reagent_name + '= Reagent(reagent_name="' + reagent_name + '", plate_location="' + \
                      plate_location + '", plate_type="' + plate_type + '")'
    return csv_path,script_path+"\n"

def generate_pipette(pipette):
    """
          "pipette_name": "p1000",
      "axis": "a",
      "tiprack": ["tiprack-1000"],
      "trash": "trash"

    p1000 = Pipette("eppendorf1000", "a", [tiprack1], trash)
    :param pipette:
    :return:
    """
    str_list = ["tiprack"]
    base_args = pipette["pipette_name"]+" = Pipette("
    for key in pipette:
        if key not in str_list:
            base_args+=key+"='"+str(pipette[key])+"',"
        else:
            base_args+=key+"="+str(pipette[key])+","
    base_args+=")\n"
    return base_args


def compile_action(mode,offset):
    if mode == "transfer":
        return ".transfer(dst_offset="+str(offset)+")"
    if mode == "distribute-cols":
        return '.distribute("rows",dst_offset='+str(offset)+")"
    if mode == "distribute-rows":
        return '.distribute("cols",dst_offset='+str(offset)+")"

def generate_action(action):
    """
    "pipette": "p1000",
      "dest_vol_col": "Volume to add for 0.8M (uL)",
      "source": "DMA",
      "destination": "amines",
      "dest_rack_col": "Location rack",
      "mode": "transfer",
      "offset": -30
     Action(pipette=p1000, dest_vol_col='Volume to add for 0.8M (uL)',
           source=trough_big, destination=reagent_1, src_rack_col='Location rack').transfer(dst_offset=-30)
    :param action:
    :return:
    """
    base_args = "Action("
    skip_list = ["mode","offset"]
    str_list = ["destination","source"]
    for key in action:
        if key in skip_list:
            continue
        if key in str_list:
            base_args+=key+"="+action[key]+","
        else:
            base_args+=key+"='"+action[key]+"',"
    base_args+=")"+compile_action(action["mode"],action["offset"])+"\n"
    return base_args


def get_script_from_json(input_json):
    python_dict = json.load(open(input_json))
    top_data = []
    function_data = []
    for reagent in python_dict["reagents"]:
        csv_data, script_data = generate_reagent_text(reagent)
        if csv_data:
            top_data.append(csv_data)
        function_data.append(script_data)
    for pipette in python_dict["pipettes"]:
        script_data = generate_pipette(pipette)
        function_data.append(script_data)
    for action in python_dict["actions"]:
        script_data = generate_action(action)
        function_data.append(script_data)
    return top_data,function_data



def input_script_name(script_file):
    """
    Compile this script into all the things needed to run.
    :param script_file:
    :return:
    """
    model_lines = clean_lines(open("../chem/models.py").readlines())
    util_lines = clean_lines(open("../chem/utils.py").readlines())
    top_data,funct_data = get_script_from_json(script_file)
    model_lines.extend(util_lines)
    model_lines.extend(top_data)
    model_lines.extend(funct_data)
    out_file = open(script_file.replace(".json","_compiled.py"),"w")
    out_file.writelines(model_lines)

if __name__ == "__main__":
    import sys
    input_script_name(sys.argv[1])