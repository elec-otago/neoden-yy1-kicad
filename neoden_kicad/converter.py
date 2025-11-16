'''
    Neoden Pick and Place machine converter

    Author: Tim Molteno. tim@elec.ac.nz
    Copyright: (c) 2023
    License: GPLv3
'''
import re


"""
==============================================INFO & MAPS==================================================
"""
global board_length

global footprint_map
global feeder_map

## A list of regex patterns to match the footprint, and substitutions to make
footprint_map = [ 
                ("[RCLD]_([0-9]+)_[0-9]+Metric\Z", "\g<1>D"), # C_0603_1608Metric -> 0603D
                ("D_SOD-([0-9]+)\Z", "SOD_\g<1>"), # D_SOD_XXX -> SODXXX
                ("SOT-([0-9]+)-([0-9]+)*", "SOT-\g<1>-\g<2>"), # SOT-YY-XX -> SOT-23-5
                ("SOT-([0-9]+)\Z", "SOT_\g<1>"), # SOT-23 -> SOT-23
                ("QFN-([0-9]+)*", "QFN-\g<1>"), # QFN-8-xxx -> QFN_8
                ("DFN-([0-9]+)*", "DFN-\g<1>"), # DFN-8-xxx -> DFN_8
                ("SOIC-([0-9]+)*", "SOIC-\g<1>"), # SOIC-16 -> SOIC-16
                ("SOP-([0-9]+)*", "SOP-\g<1>"), # SOP-16 -> SOP-16
                ("QFP-([0-9]+)*", "QFP-\g<1>"), # QFP-8-xxx -> QFP_8
                ("TQFP-([0-9]+)*", "TQFP-\g<1>"), # TQFP-8-xxx -> TQFP_8
                ("TSOP-([0-9]+)*", "TSOP-\g<1>"), # TSOP-16 -> TSOP-16
             ]

## A map of component values to feederNo
feeder_map = []

def update_feeder_map(_feeder_map):
    """
    Update the global feeder_map variable with the provided map.

    Args:
        feeder_map (list of list): A list where each sublist contains [value regex, package regex, feederNo].

    Returns:
        None: The function updates the global feeder_map variable directly.
    """
    global feeder_map
    feeder_map = _feeder_map
    print(f"\033[36mINFO:\033[0m Feeder map updated with {len(feeder_map)} entries")

    return None




"""
==============================================DATA CONVERTORS==================================================
"""
def package_to_footprint(package):
    """
    Convert KiCad package name to NeoDen pick-and-place machine compatible footprint format.
    
    This function applies predefined regex patterns to transform KiCad package names
    into a standardized format that the NeoDen YY1 machine can recognize.
    
    Args:
        package (str): The original KiCad package name (e.g., "C_0603_1608Metric")
        
    Returns:
        str: Converted footprint name (e.g., "0603D") or original name if no match found
        
    Examples:
        >>> package_to_footprint("C_0603_1608Metric")
        "0603D"
        >>> package_to_footprint("D_SOD-123") 
        "SOD_123"
    """
    for c in footprint_map:
        if re.search(c[0], package) is not None:
            return re.sub(c[0], c[1], package)
        
    print(f"\033[33mWarning:\033[0m No converter found for package: {package}")
    return package

def value_to_feederNo(value, package):
    """
    Find the feeder number for a component based on its value and package.

    Args:
        value (str): The value of the component (e.g., "100nF")
        package (str): The package of the component (e.g., "C_0402_1608Metric")

    Returns:
        str: The feeder number for the component (e.g., "2") or '0' if not found

    Examples:
        >>> value_to_feederNo("100nF", "C_0402_1608Metric")
        "2"
    """
    for c in feeder_map:
        if (re.search(c[0], value) is not None) and (re.search(c[1], package) is not None):
            return c[2]
        
    print(f"\033[33mWarning:\033[0m No feeder found for component: {value}({package})")
    return '0'

def comp_pos_top(comp_pos):
    """
    Convert component position to top position.

    Args: 
        comp_pos (list): A list containing the component position [x, y, angle].
    
    Returns:
        list: A list containing the top position [x, y, angle].
    """
    x_prime = round(float(comp_pos[0]),6)
    y_prime = round(float(comp_pos[1]),6)
    angle_prime = round(float(comp_pos[2]),1)
    return [str(x_prime), str(y_prime), str(angle_prime)]

def comp_pos_bottom(comp_pos, board_length):
    """
    Convert component position to bottom position.

    Args:
        comp_pos (list): A list containing the component position [x, y, angle].

    Returns:
        list: A list containing the bottom position [x, y, angle].
    """
    x_prime = round(float(board_length) - float(comp_pos[0]), 6)
    y_prime = round(float(comp_pos[1]), 6)
    angle_prime = round(float(comp_pos[2]), 1)
    return [str(x_prime), str(y_prime), str(angle_prime)]





"""
==============================================CSV CONVERTOR==================================================
"""
def neoden_csv_info(neoden_info):
    """
    Generate the default Neoden CSV info.
        If neoden_info is None, default values are used.
    """
    # default values
    if neoden_info is None:
        neoden_info = {
            'PanelizedPCB': {
                'UnitLength': '0',
                'UnitWidth': '0',
                'Rows': '1',
                'Columns': '1',
            },
            'Fiducial': {
                '1-X': '13.09',
                '1-Y': '54.90',
                'OverallOffsetX': '0',
                'OverallOffsetY': '0',
            },
            'NozzleChange1': {
                'NozzleChange': 'OFF',
                'BeforeComponent': '2',
                'Head': 'Head1',
                'Drop': 'Station1',
                'PickUp': 'Station3',
            },
            'NozzleChange2': {
                'NozzleChange': 'OFF',
                'BeforeComponent': '3',
                'Head': 'Head1',
                'Drop': 'Station3',
                'PickUp': 'Station1',
            },
            'NozzleChange3': {
                'NozzleChange': 'OFF',
                'BeforeComponent': '1',
                'Head': 'Head1',
                'Drop': 'Station1',
                'PickUp': 'Station1',
            },
            'NozzleChange4': {
                'NozzleChange': 'OFF',
                'BeforeComponent': '1',
                'Head': 'Head1',
                'Drop': 'Station1',
                'PickUp': 'Station1',
            },
    }

    # Output default values
    output_neoden_csv_info = [
        ['NEO','YY1','P&P FILE','','','','','','','','','','',''],
        ['','','','','','','','','','','','','',''],
        ['PanelizedPCB','UnitLength',neoden_info['PanelizedPCB']['UnitLength'],'UnitWidth',neoden_info['PanelizedPCB']['UnitWidth'],'Rows',neoden_info['PanelizedPCB']['Rows'],'Columns',neoden_info['PanelizedPCB']['Columns'],''],
        ['','','','','','','','','','','','','',''],
        ['Fiducial','1-X',neoden_info['Fiducial']['1-X'],'1-Y',neoden_info['Fiducial']['1-Y'],'OverallOffsetX',neoden_info['Fiducial']['OverallOffsetX'],'OverallOffsetY',neoden_info['Fiducial']['OverallOffsetY'],''],
        ['','','','','','','','','','','','','',''],
        ['NozzleChange',neoden_info['NozzleChange1']['NozzleChange'],'BeforeComponent',neoden_info['NozzleChange1']['BeforeComponent'], neoden_info['NozzleChange1']['Head'],'Drop',neoden_info['NozzleChange1']['Drop'],'PickUp',neoden_info['NozzleChange1']['PickUp'],''],
        ['NozzleChange',neoden_info['NozzleChange2']['NozzleChange'],'BeforeComponent',neoden_info['NozzleChange2']['BeforeComponent'], neoden_info['NozzleChange2']['Head'],'Drop',neoden_info['NozzleChange2']['Drop'],'PickUp',neoden_info['NozzleChange2']['PickUp'],''],
        ['NozzleChange',neoden_info['NozzleChange3']['NozzleChange'],'BeforeComponent',neoden_info['NozzleChange3']['BeforeComponent'], neoden_info['NozzleChange3']['Head'],'Drop',neoden_info['NozzleChange3']['Drop'],'PickUp',neoden_info['NozzleChange3']['PickUp'],''],
        ['NozzleChange',neoden_info['NozzleChange4']['NozzleChange'],'BeforeComponent',neoden_info['NozzleChange4']['BeforeComponent'], neoden_info['NozzleChange4']['Head'],'Drop',neoden_info['NozzleChange4']['Drop'],'PickUp',neoden_info['NozzleChange4']['PickUp'],''],
        ['','','','','','','','','','','','','',''],
    ]

    return output_neoden_csv_info

def convert(input_data):
    """
    Convert KiCad component data to NeoDen pick-and-place machine compatible format.

    Args:
        input_data (list of dict): List of component data dictionaries from KiCad
        
    Returns:
        tuple: (output_data, output_header)
            output_data (list of list): Processed component data ready for NeoDen
            output_header (list): Headers for the output CSV file

    """
    # Convert the input dictionary to the output dictionary
    line = 0
    # List of substitutions of headers
    substitute_headers = {
        'Comment': 'Val',
        'Designator': 'Ref',
        'Mid X': 'PosX',
        'Mid Y': 'PosY',
        'Rotation': 'Rot'
    }
    try:
        for row in input_data:
            line = line+1

            ## perform header substitutions to make sure we have the required headers
            layer = row.get('Layer', row.get('Side', 'top'))
            for key in substitute_headers.keys():
                try:
                    row[key] = row[substitute_headers[key]]
                except:
                    pass
            
            ## convert data to NeoDen format
            row['Mid X'], row['Mid Y'], row['Rotation'] = comp_pos_bottom([row['Mid X'], row['Mid Y'], row['Rotation']], board_length) if (layer == 'bottom') else comp_pos_top([row['Mid X'], row['Mid Y'], row['Rotation']])
            row['Head'] = '01'              # Use head 1 default
            row['FeederNo'] = value_to_feederNo(row['Val'], row['Package']) # Get the feeder number from the map
            row['Mount Speed (%)'] = '100'
            row['Pick Height(mm)'] = '0'
            row['Place Height(mm)'] = '0'
            row['Mode'] = '1'
            row['Skip'] = '0'
            row['Footprint'] = package_to_footprint(row['Package'])
    except Exception as e:
        print(f"\033[31mError:\033[0m Input error on line {line}: {row}")
        print(e)

    output_data = []
    line = 0
    # List of output headers required by NeoDen.
    output_header = ['Designator', 'Comment', 'Footprint', 'Mid X', 'Mid Y', 
                     'Rotation', 'Head', 'FeederNo', 'Mount Speed (%)', 'Pick Height(mm)', 'Place Height(mm)', 'Mode', 'Skip']
    try:
        for row in input_data:
            line = line+1
            output_data.append([row[key] for key in output_header])
    except Exception as e:
        print(f"\033[31mError:\033[0m Output error on line {line}: {row}")
        print(e)

    return output_data, output_header
