import yaml,os,sys,datetime

def gen_prot_dict():
    """
    :param input_list:
    :return:
    """
    from utils.protocols import StockSolution,MonoDispensing,MultiBase,SMTransfer,ReactionQC,DMATransfer,\
        PostWorkupTransfer,Workup,PostWorkupQCAndTransfer,PostWorkupDMSOAddition,BaseT3PMulti, PoisedReactor
    input_list = [StockSolution,MonoDispensing,MultiBase,SMTransfer,ReactionQC,DMATransfer,PostWorkupTransfer,
                           Workup,PostWorkupQCAndTransfer,PostWorkupDMSOAddition,BaseT3PMulti, PoisedReactor]
    out_dict = {}
    for protocol in input_list:
        out_dict[protocol.__str__(None)] = protocol
    return out_dict


def add_input_dict_to_process(process_dict,input_dict):
    if process_dict == None:
        process_dict = {}
    keys_to_add = ["general_reagents", "general_headers", "volume_headers"]
    for key in keys_to_add:
        for new_key in input_dict[key]:
            if new_key in process_dict:
                continue
            elif new_key not in input_dict[key]:
                continue
            process_dict[new_key] = input_dict[key][new_key]
    return process_dict

def open_dict(input_yaml):
    new_dict = yaml.load(open(input_yaml).read())
    if "inherit" in new_dict:
        inherit_path = new_dict["inherit"]
        if not os.path.isfile(inherit_path):
            print("File not found: " + inherit_path)
            sys.exit()
        newer_dict = yaml.load(open(inherit_path).read())
    else:
        return new_dict
    new_procs = newer_dict["processes"]
    newer_dict.update(new_dict)
    for proc in new_procs:
        if proc in newer_dict["processes"]:
            pass
        else:
            newer_dict["processes"][proc]=new_procs[proc]
    return newer_dict


def check_files(input_dict):
    for file_name in input_dict["files"]:
        file_path  =input_dict["files"][file_name]
        if not os.path.isfile(file_path):
            print("File not found: " + file_path + "\nWith name: " + file_name)
            sys.exit()

def run_parser(input_yaml_file):
    makefiles = gen_prot_dict()
    input_dict = open_dict(input_yaml_file)
    check_files(input_dict)
    processes = input_dict["processes"]
    if "name" in input_dict:
        precursor = input_dict["name"]
    else:
        precursor = "reaction"
    output_dir = datetime.datetime.now().strftime(precursor  + '_%Y_%m_%d_%H_%M_%S')
    os.mkdir(output_dir)
    for i in range(len(processes)):
        # Inject data into script
        name = list(processes[i].keys())[0]
        proc_dict = add_input_dict_to_process(processes[i][name],input_dict)
        if name in makefiles:
            procedure = makefiles[name](proc_dict,input_dict,name,index=i)
            procedure.write_protocol()
        else:
            print("Skipping: " + name)
            continue
        for f in procedure.files:
            out_f = open(os.path.join(output_dir,f.name),"w")
            out_f.write(f.data)
            out_f.close()

def run_function():
    import argparse

    parser = argparse.ArgumentParser(description='Read in a YAML and make some Opentrons protocols')
    parser.add_argument('--yaml_path', dest='yaml_path',
                        help='The path of the YAML file to use to build the protocols')
    args = parser.parse_args()
    if args.yaml_path:
        run_parser(args.yaml_path)
    else:
        parser.print_help()
