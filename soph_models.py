from p_calculator import calc_p, defaults, calc_p_def
from pred import soph
from config import zone_pairs, def_key
label_col = 'duration_days'
from csv import writer


def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)


for pair in zone_pairs:
    print("pair", pair)
    gp1, gp2, counter_dict, counter_dict2 = calc_p_def(pair[0], pair[1])
    p1_def_0 = counter_dict[(0, def_key)] / (counter_dict[(1, def_key)] + counter_dict[(0, def_key)])
    p1_def_1 = counter_dict[(1, def_key)] / (counter_dict[(1, def_key)] + counter_dict[(0, def_key)])
    p2_def_0 = counter_dict2[(0, def_key)] / (counter_dict2[(1, def_key)] + counter_dict2[(0, def_key)])
    p2_def_1 = counter_dict2[(1, def_key)] / (counter_dict2[(1, def_key)] + counter_dict2[(0, def_key)])

    l1, l2, l3, l4, l5, l6 = soph(gp1, gp2,label_col, p1_def_0, p1_def_1, p2_def_0, p2_def_1)
    to_write = [pair[0], pair[1], l1, l2, l3, l4, l5, l6]
    append_list_as_row("soph_models.csv", to_write)