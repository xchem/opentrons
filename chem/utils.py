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
def finish():
    robot.commands()
    robot.home()


def get_pipette_dict(name):
    pipette_dict = {"eppendorf1000":{"max_vol":1000,"min_vol":0,"channels":1},
                        "dlab300_8": {"max_vol": 300, "min_vol": 10, "channels": 8}}
    if not name:
        raise ValueError("MUST SPECIFY NAME")
    if name not in pipette_dict:
        raise ValueError("NAME NOT IN OPTIONS " + pipette_dict.keys())
    return pipette_dict[name]