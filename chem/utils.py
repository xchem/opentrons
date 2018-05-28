class FileHolder(object):
    def __init__(self,name="NULL",data="NULL"):
        self.name = name
        self.data = data

class Vector(object):
    def tolist(self):
        return list(self.input_list)

    def astype(self, input_type):
        if input_type == int:
            return Vector([int(float(x)) for x in self.input_list])
        return Vector([input_type(x) for x in self.input_list])

    def __init__(self, input_list):
        self.input_list = input_list

class DataFrame(object):
    def __len__(self):
        return self.length

    def __getitem__(self, value):
        return Vector(self.dict_input[value])

    def __init__(self, dict_input, length):
        self.dict_input = dict_input
        self.length = length

#Function that reads a csv file correctly without having to import anything (issues with molport). Uses 2 classes, Vector and DataFrame
def read_csv(input_file):
    lines = open(input_file).readlines()
    header = lines[0].rstrip().split(",")
    out_d = {}
    for head in header:
        out_d[head] = []
    for line in lines[1:]:
        spl_line = line.rstrip().split(",")
        for i, head in enumerate(header):
            out_d[head].append(spl_line[i])
    df = DataFrame(out_d, len(lines[1:]))
    return df



def get_smis(csv_file,smiles_header):
    header_col = csv_file.split("\n")[0].split(",")
    cols = [x for x in csv_file.split("\n")[1:] if x]
    smi_list = []
    for i,line in enumerate(cols):
        for j, col in enumerate(header_col):
            if col == smiles_header:
                smi_list.append(line.split(",")[j].rstrip())
    return smi_list

def merge_lists(list_one,list_two):
    out_list = []
    for i,val in enumerate(list_one):
        out_list.append(list_two[i],val)
    return out_list

def get_name(name,index,subindex):
    return "_".join([str(index),chr(subindex+97),name])+".py"


class BuildProtocol(object):

    def __init__(self):
        self.single_vars = []
        self.list_vars = None
        self.trough_vars = None
        self.files = []
        self.subindex = 0


    def get_list_from_header(self, csv_file, header):
        return read_csv(csv_file)[header].tolist()

    def do_variables(self):
        if self.list_vars:
            for key in self.list_vars:
                csv_file = self.list_vars[key]["file"]
                header = self.list_vars[key]["header"]
                self.conv_to_var(
                    self.get_list_from_header(csv_file,header),
                    key)
        if self.trough_vars:
            trough_csv = self.trough_vars["path"]
            id_header = self.trough_vars["id_header"]
            trough_setup = TroughSetUp(trough_csv, id_header)
            for key in self.trough_vars:
                if key in ["path","id_header"]: continue
                variable = self.trough_vars[key]
                self.conv_to_var(
                    trough_setup.get_well_from_id(
                        variable["col_header"],
                        variable["solvent_name"],
                    ),
                    key
                )
        for single_var in self.single_vars:
            self.conv_to_var(self.single_vars[single_var], single_var)


    def do_imports(self):
        return "from opentrons import robot, containers, instruments"

    def do_setup(self):
        raise NotImplementedError

    def do_protocol(self):
        raise NotImplementedError

    def conv_to_var(self, variable, variable_name):

        try:
            variable = float(variable)
        except ValueError:
            pass
        except TypeError:
            pass

        if type(variable) == str:
            self.data += variable_name + " = '" + str(variable) + "'\n"
        else:
            self.data += variable_name + " = " + str(variable) + "\n"

    def write_protocol(self):
        self.data = self.do_imports()
        self.data += self.do_setup()
        self.do_variables()
        self.data += self.do_protocol()
        self.files.append(FileHolder(get_name(self.name, self.index, self.subindex), self.data))


class TroughSetUp(object):

    def __init__(self,trough_csv,id_header):
        self.csv_df = read_csv(trough_csv)
        self.id_list = self.csv_df[id_header]

    def get_well_from_id(self,header_id,solvent):
        location_list = self.csv_df[header_id].tolist()
        for i, x in enumerate(self.id_list.tolist()):
            if x == solvent:
                solvent_location = location_list[i]
                return solvent_location



def get_number_rows(csv_file):
    return len(read_csv(csv_file))