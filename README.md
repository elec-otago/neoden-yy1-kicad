# neoden_kicad

Post-processor to allow Kicad centroid files to work on the Neoden YY1 pick and place machine. This package contains a script that reads CPL (centroid position) files and modifies their contents to be readable by the [Neoden YY1](https://www.neodensmt.com/pick-and-place-machine/neoden-yy1-pick-and-place-machine.html) small pick and place machine.

## Installation

On a modern linux distribution, try the following:

    pipx install neoden_kicad

If you're  unfortunate enough to be stuck with windows, try contacting your system administrator.

## Usage

If you have exported a CPL file from kicad (Component Placement file) called CPL-mypos.csv, then you can convert it to neoden-readable format using:

    neoden_kicad --pos CPL-mypos.csv --out neoden_pos.csv

## Footprint conversions

The Neoden YY1 needs to be told what footprints that it is using. Some common conversions are done by this package. These are contained in the converter.py file. This is done using a list of regular expressions:

    converters = [ 
                ("[RCLD]_([0-9]+)_[0-9]+Metric\Z", "\g<1>D"), # C_0603_1608Metric -> 0603D
                ("D_SOD-([0-9]+)\Z", "SOD_\g<1>"), # D_SOD_XXX -> SODXXX
                ("SOT-([0-9]+)-([0-9]+)\Z", "SOT-\g<1>-\g<2>"), # SOT-YY-XX -> SOT-23-5
                ("SOT-([0-9]+)\Z", "SOT_\g<1>"), # SOT-23 -> SOT-23
             ]

The converter will leave footprints alone that it does not recognize. If you find one conversions that you'd like added to the list, please file an issue on github (https://github.com/elec-otago/neoden-yy1-kicad)

### Author

Written by Tim Molteno tim@elec.ac.nz
