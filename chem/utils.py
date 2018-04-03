class FileHolder(object):
    def __init__(self,name="NULL",data="NULL"):
        self.name = name
        self.data = data

def get_vol_pos_list(csv_file,vol_col_header,rack_col_header):
    header_col = csv_file.split("\n")[0].split(",")
    cols = [x for x in csv_file.split("\n")[1:] if x]
    vol_pos_list = []
    for i,line in enumerate(cols):
        for j, col in enumerate(header_col):
            if col == vol_col_header:
                vol_to_add = float(line.split(",")[j].rstrip())
            if col == rack_col_header:
                pos_to_take = str(line.split(",")[j].rstrip())
        vol_pos_list.append((vol_to_add,pos_to_take))
    return vol_pos_list

