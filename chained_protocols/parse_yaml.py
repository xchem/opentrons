import yaml,os
from protocols.do_reaction import DoReaction

makefiles = {'do_reaction': DoReaction}

input_dict = yaml.load(open("96_well_reaction.yml").read())
reagents = input_dict["reagents"]
couplers = input_dict["couplers"]
processes = input_dict["processes"]
this_dir = "NEW_DIR"
#TODO
os.mkdir(this_dir)
for name in processes:
    # Inject data into script
    process = processes[name]
    if name in makefiles:
        procedure = makefiles[name](process,reagents,couplers)
    else:
        continue
    for f in procedure.files:
        out_f = open(os.path.join(this_dir,f.name),"w")
        out_f.write(f.data)
        out_f.close()