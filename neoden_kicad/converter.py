'''
    Neoden Pick and Place machine converter

    Author: Tim Molteno. tim@elec.ac.nz
    Copyright: (c) 2023
    License: GPLv3
'''
import re

## A list of regex patterns to match the footprint, and substitutions to make

converters = [ 
                ("[RCLD]_([0-9]+)_[0-9]+Metric\Z", "\g<1>D"), # C_0603_1608Metric -> 0603D
                ("D_SOD-([0-9]+)\Z", "SOD_\g<1>"), # D_SOD_XXX -> SODXXX
                ("SOT-([0-9]+)-([0-9]+)\Z", "SOT-\g<1>-\g<2>"), # SOT-YY-XX -> SOT-23-5
                ("SOT-([0-9]+)\Z", "SOT_\g<1>"), # SOT-23 -> SOT-23
             ]

def package_to_footprint(package):
    for c in converters:
        if re.search(c[0], package) is not None:
            return re.sub(c[0], c[1], package)
           
    
    print("Warning: No converter found for package: {}".format(package))
    return package


def convert(input_data):
    # Convert the input dictionary to the output dictionary

    # List of substitutions of headers
    substitute_headers = {
        'Comment': 'Val',
        'Ref': 'Designator',
        'Mid X': 'PosX',
        'Mid Y': 'PosY',
        'Rotation': 'Rot'
    } 
    for row in input_data:
        row['Head'] = '00'
        row['FeederNo'] = '0'
        row['Mount Speed (%)'] = '100'
        row['Pick Height(mm)'] = '0'
        row['Place Height(mm)'] = '0'
        row['Mode'] = '1'
        row['Skip'] = '0'
        row['Footprint'] = package_to_footprint(row['Package'])
	
        for key in substitute_headers.keys():
            try:
                row[key] = row[substitute_headers[key]]
            except:
                pass

    output_data = []
    # List of output headers required by NeoDen. 
    output_header = ['Designator', 'Comment', 'Footprint', 'Mid X', 'Mid Y', 
                     'Rotation', 'Head', 'FeederNo', 'Mount Speed (%)', 'Pick Height(mm)', 'Place Height(mm)', 'Mode', 'Skip']
    for row in input_data:
        output_data.append([row[key] for key in output_header])

    return output_data, output_header
