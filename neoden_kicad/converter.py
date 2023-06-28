'''
    Neoden Pick and Place machine converter

    Author: Tim Molteno. tim@elec.ac.nz
'''
import re

## A list of regex patterns to match the footprint
converters = [ ("[RCLD]_([0-9]+)_[0-9]+Metric", "\g<1>D")]       # C_0603_1608Metric -> 0603D

def package_to_footprint(package):
    for c in converters:
        ret = re.sub(c[0], c[1], package)
        if ret != package:
            return ret
    return ret


def convert(input_data):
    # Convert the input dictionary to the output dictionary

    for row in input_data:
        row['Comment'] = row['Val']
        row['Head'] = '00'
        row['FeederNo'] = '0'
        row['Mount Speed (%)'] = '100'
        row['Pick Height(mm)'] = '0'
        row['Place Height(mm)'] = '0'
        row['Mode'] = '1'
        row['Skip'] = '0'
        row['Footprint'] = package_to_footprint(row['Package'])

    output_data = []
    output_header = ['Designator', 'Val', 'Footprint', 'Mid X', 'Mid Y', 
                     'Rotation', 'Head', 'FeederNo', 'Mount Speed (%)', 'Pick Height(mm)', 'Place Height(mm)', 'Mode', 'Skip']
    for row in input_data:
        output_data.append([row[key] for key in output_header])

    return output_data, output_header