defaults = {
    'cause_H': '1',
    'cause_PB': '0',
    'cause_L': '0',
    'cause_RE': '0',
    'cause_U': '0',
    '1': '0',
    '2': '0',
    '3': '0',
    '4': '0',
    'Crown': '0',
    'Dump': '0',
    'Forest': '0',
    'Grass': '0',
    'Ground': '0',
    'IFR': '0',
    'OFR': '0',
    'Other': '0',
    'Prescribed Burn': '0',
    'Req For Assist': '0',
    'Request For Ass*': '0',
    'Surface': '0',
    'Wildfire': '0',
    'Summer': '1',
    'Fall': '0',
    'Winter': '0',
    'Spring': '0',
    'Size>-4': '1', 'Size>-2': '1', 'Size>-1': '1', 'Size>0': '1',
    'Size>1': '0', 'Size>2': '0', 'Size>3': '0', 'Size>4': '0', 'Size>5': '0', 'Size>6': '0',
    'after1940': '1', 'after1950': '1', 'after1960': '1', 'after1970': '1', 'after1980': '1', 'after1990': '1',
    'after2000': '0', 'after2010': '0', 'after2020': '0'
}


zone_pairs = [
    # ('4', '9'),
    # ('9', '10'),
    # ('6', '14'),
    # ('14', '12'),
    # ('12', '4'),
    # ('5', '9'),
    # ('9', '6'),
    # ('5', '7'),
     ('8', '14'),
    # ('11', '12'),
    # ('4', '11'),
    # ('8', '7'),
    # ('6', '4'),
    # ('9', '11'),
    # ('12', '8'),
    # ('6', '10'),
    # ('7', '11'),
    # ('11', '10'),
    # ('9', '14'),
    #('5', '6'),
]
important_cols = [
   'Size>2', 'Size>1', 'Wildfire', 'Surface', 'Winter' , 'after2000', 'Size>3' , 'after2010', 'Size>-1', 'cause_H'
]
def_key = (('cause_H', '0'), ('Surface', '0'), ('Wildfire', '0'), ('Winter', '0'), ('Size>-1', '1'), ('Size>1', '0'), ('Size>2', '0'), ('Size>3', '0'), ('after2000', '1'), ('after2010', '0'))
