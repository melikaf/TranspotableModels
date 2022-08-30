from p_calculator import calc_p, defaults
from pred import calc_pred, calc_loss
from config import zone_pairs
label_col = 'duration_days'
split_col = 'ECOZONE'

from csv import writer
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


for pair in zone_pairs:
    print("pair", pair)
    gp1, gp2, p, p2 = calc_p(pair[0], pair[1])
    labels, direct_prob, ratio_prob, ods_mult_prob, ratio_bad, number_of_samples = calc_pred(gp1, gp2, p, p2, label_col, split_col, defaults)
    l1, l2, l3 = calc_loss(labels, direct_prob, ratio_prob, ods_mult_prob)
    print("results", l1,l2,l3, "size", number_of_samples, "bad", ratio_bad, "percent", ratio_bad/number_of_samples)
    to_write = [pair[0], pair[1], l1, l2, l3, ratio_bad, number_of_samples, ratio_bad/number_of_samples]
    append_list_as_row("results2.csv", to_write)