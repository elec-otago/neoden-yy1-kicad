# neoden_kicad

Post-processor to allow Kicad centroid files to work on the Neoden YY1 pick and place machine. This package contains a script that reads CPL (centroid position) files and modifies their contents to be readable by the [Neoden YY1](https://www.neodensmt.com/pick-and-place-machine/neoden-yy1-pick-and-place-machine.html) small pick and place machine.

## Installation

On a modern linux distribution, try the following:

```shell
pipx install neoden_kicad
```

If you're unfortunate enough to be stuck with windows, try contacting your system administrator.

## Usage

If you have exported a CPL file from kicad (Component Placement file) called CPL-mypos.csv, then you can convert it to neoden-readable format using:

```shell
neoden_kicad --pos CPL-mypos.csv --out neoden_pos.csv
```

arguments:
- --pos: The path to the CPL file to convert.
- --out: The path to the output file.
- --feeder_map: The path to the feeder map file.
- --xlen: The length of the X axis of the Neoden YY1 in mm.

## Footprint Conversions

The Neoden YY1 needs to be told what footprints that it is using. Some common conversions are done by this package. These are contained in the converter.py file. This is done using a list of regular expressions:

```python
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
```


The converter will leave footprints alone that it does not recognize. If you find one conversions that you'd like added to the list, please file an issue on github (https://github.com/elec-otago/neoden-yy1-kicad)

## Feeder Map

The Neoden YY1 has a number of feeders that are used to place components. The feeder map is a csv file that maps the feeder number to the component type. The default feeder map is contained in the feeder_map.csv file. This file should be copied to the same directory as the neoden_kicad script. 

The feeder map file should contain the following columns:
- value_regex: A regular expression that matches the value of the component.
- package_regex: A regular expression that matches the package of the component.
- feederNo: The feeder number to use for components that match the value and package regex.

For example:
```csv
value_regex,package_regex,feederNo
10uF?,C_0603_1608Metric,1
100nF?|0\.1uF?,C_0402_1005Metric,2
```

Use this command to convert the CPL file to neoden-readable format:
```
neoden_kicad --pos CPL-mypos.csv --out neoden_pos.csv --feeder_map data/feeder_map.csv
```

## Double-sided Mount Position Conversion Support

The PosX and PosY columns in the CPL file should be set to the center of the component. But when mount bottom side, the PosX should be set to `xlen - PosX`, where xlen is the distance from zero point to the right edge of the PCB.

You can use this function by `--xlen` option. For example, if your PCB is 100mm wide, and you have set the zero point to the lower left corner of the PCB in kicad.
```shell
neoden_kicad --pos CPL-mypos.csv --out neoden_pos.csv --xlen 100
```

Function `comp_pos_top` and `comp_pos_bottom` in `neoden_kicad/converter.py` are used to convert the position of the component to the top and bottom side respectively.

### Author

Written by Tim Molteno tim@elec.ac.nz
