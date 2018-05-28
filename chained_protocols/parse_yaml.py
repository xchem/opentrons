import yaml,os,sys,datetime

from protocols.new_protocols import StockSolution,\
    MultiBase,MonoDispensing,\
    SMTransfer,\
    ReactionQC,\
    DMATransfer,\
    PostWorkupDMSOAddition, PostWorkupQCAndTransfer, PostWorkupTransfer,Workup, BaseT3PMulti


def gen_prot_dict(input_list):
    """

    :param input_list:
    :return:
    """
    out_dict = {}
    for protocol in input_list:
        out_dict[protocol.__str__(None)] = protocol
    return out_dict

makefiles = gen_prot_dict([StockSolution,MonoDispensing,MultiBase,SMTransfer,ReactionQC,DMATransfer,PostWorkupTransfer,
                           Workup,PostWorkupQCAndTransfer,PostWorkupDMSOAddition,BaseT3PMulti])

input_yaml = sys.argv[1]
input_dict = yaml.load(open(input_yaml).read())
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
    if name in makefiles:
        procedure = makefiles[name](processes[i][name],input_dict,name,index=i)
        procedure.write_protocol()
    else:
        print("Skipping: " + name)
        continue
    for f in procedure.files:
        out_f = open(os.path.join(output_dir,f.name),"w")
        out_f.write(f.data)
        out_f.close()