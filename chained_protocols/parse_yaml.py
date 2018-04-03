import yaml,os
from xchem_ot.protocols.do_reaction import DoReaction

makefiles = {'do_reaction': DoReaction}

input_dict = yaml.load(open("96_well_reaction.yml").read())
reagents = input_dict["reagents"]
couplers = input_dict["couplers"]
processes = input_dict["processes"]
this_dir = "NEW_DIR"
os.mkdir()
for process in processes:
    # Inject data into script
    if process in makefiles:
        process = makefiles[process](reagents,couplers)
    else:
        continue
    for f in process.files:
        out_f = os.path.join(this_dir,f.name)
        out_f.write(f.data)
        out_f.close()