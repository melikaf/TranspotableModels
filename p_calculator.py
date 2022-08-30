import pandas as pd
from config import defaults, important_cols
#
# important_cols = [
#    'Size>2', 'Size>1', 'Wildfire', 'Surface', 'Winter' , 'after2000', 'Size>3' , 'after2010', 'Size>-1', 'cause_H'
# ]
# new_def = {
# 'cause_H': '1',
# 'Surface': '0',
# 'Wildfire': '0',
# 'Winter': '0',
# 'Size>-1': '1',
# 'Size>1': '0',
# 'Size>2': '0',
# 'Size>3': '0',
# 'after2000': '0',
# 'after2010': '0'
#
# }
# important_cols = [
#     'Size>2', 'Wildfire', 'Winter' , 'after2000',  'cause_H'
# ]


def calc_p(zone1, zone2):

    fp = "Data/correct_encoded.csv"
    df = pd.read_csv(fp, dtype=str)
    df = df.drop('Unnamed: 0',axis = 1)

    df['duration_days'] = df['duration_days'].astype(int)

    df = df[~(df['duration_days'] < 0)] #remove error
    df.loc[df['duration_days'] > 10, 'duration_days'] = -1 #large
    df.loc[df['duration_days'] >= 0, 'duration_days'] = 0
    df.loc[df['duration_days'] == -1, 'duration_days'] = 1

    label_col = 'duration_days'
    all_label_values = list(set(list(df[label_col].values)))
    print(all_label_values)
    gp1 = df.loc[df['ECOZONE'] == zone1]
    gp2 = df.loc[df['ECOZONE'] == zone2]
    print(gp1.shape , gp2.shape)
    from collections import defaultdict

    counter_dict = defaultdict(lambda: 0)  # h ^ v, the keys would be (h, column_name, value of column)
    not_counter_dict = defaultdict(lambda: 0)
    columns = list(gp1.columns)
    columns.remove(label_col)
    columns.remove('ECOZONE')
    for index, row in gp1.iterrows():
        h = row[label_col]
        for c in columns:
            key = (h, c, row[c])
            counter_dict[key] += 1
            for val in all_label_values:
                if val != h:
                    not_counter_dict[(val, c, row[c])] += 1
    from collections import defaultdict

    counter_dict2 = defaultdict(lambda: 0)  # h ^ v, the keys would be (h, column_name, value of column)
    not_counter_dict2 = defaultdict(lambda: 0)
    columns = list(gp2.columns)
    columns.remove(label_col)
    columns.remove('ECOZONE')

    for index, row in gp2.iterrows():
        h = row[label_col]
        for c in columns:
            key = (h, c, row[c])
            counter_dict2[key] += 1
            for val in all_label_values:
                if val != h:
                    not_counter_dict2[(val, c, row[c])] += 1
    c0 = 1
    c1 = 2
    p = defaultdict(lambda: 0)  # a dictionary for p(h | v_i), the keys would be (h, column_name, value of column)
    p2 = defaultdict(lambda: 0)  # a dictionary for p(h | v_i), the keys would be (h, column_name, value of column)

    for index, row in gp1.iterrows():
        h = row[label_col]

    for index, row in gp2.iterrows():
        h = row[label_col]
        for c in columns:
            key = (h, c, row[c])
            not_key = (1-h, c, row[c])
            p2[key] = (counter_dict2[key] + c0) / (counter_dict2[key] + not_counter_dict2[key] + c1)
            p2[not_key] = (counter_dict2[not_key] + c0) / (counter_dict2[not_key] + not_counter_dict2[not_key] + c1)
            p[key] = (counter_dict[key] + c0) / (counter_dict[key] + not_counter_dict[key] + c1)
            p[not_key] = (counter_dict[not_key] + c0) / (counter_dict[not_key] + not_counter_dict[not_key] + c1)

    return gp1, gp2, p, p2


def calc_p_def(zone1, zone2):

    fp = "/Users/melika/Documents/MScProject/FireData/correct_encoded.csv"
    df = pd.read_csv(fp, dtype=str)
    df = df.drop('Unnamed: 0',axis = 1)

    df['duration_days'] = df['duration_days'].astype(int)

    df = df[~(df['duration_days'] < 0)] #remove error
    df.loc[df['duration_days'] > 10, 'duration_days'] = -1 #large
    df.loc[df['duration_days'] >= 0, 'duration_days'] = 0
    df.loc[df['duration_days'] == -1, 'duration_days'] = 1

    label_col = 'duration_days'
    all_label_values = list(set(list(df[label_col].values)))
    print(all_label_values)
    gp1 = df.loc[df['ECOZONE'] == zone1]
    gp2 = df.loc[df['ECOZONE'] == zone2]
    print(gp1.shape , gp2.shape)
    from collections import defaultdict

    counter_dict = defaultdict(lambda: 0)  # h ^ v, the keys would be (h, column_name, value of column)
    not_counter_dict = defaultdict(lambda: 0)
    counter_dict2 = defaultdict(lambda: 0)  # h ^ v, the keys would be (h, column_name, value of column)

    columns = list(gp1.columns)
    columns.remove(label_col)
    columns.remove('ECOZONE')
    label_counter2 = defaultdict(lambda : 0)
    for index, row in gp2.iterrows():
        h = row[label_col]
        label_counter2[h] += 1
        key = []
        bad = False
        for c in columns:
            #if row[c] != defaults[c]:
            #    bad = True
            #    break
            if c not in important_cols:
                continue
            key.append((c,row[c]))
        if bad:
            continue
        key = tuple(key)

        counter_dict2[(h,key)] += 1
    label_counter1 = defaultdict(lambda : 0)

    for index, row in gp1.iterrows():
        h = row[label_col]
        label_counter1[h] += 1
        key = []
        bad = False
        for c in columns:
            #if row[c] != defaults[c]:
            #    bad = True
            #    break
            if c not in important_cols:
                continue
            key.append((c,row[c]))
        if bad:
            continue
        key = tuple(key)

        counter_dict[(h,key)] += 1
    return gp1, gp2, counter_dict, counter_dict2