# neoden-yy1-kicad

Post-processor to allow Kicad centroid files to work on the Neoden YY1 pick and place machine. This package contains a script that reads CPL (centroid position) files and modifies their contents to be readable by the [Neoden YY1](https://www.neodensmt.com/pick-and-place-machine/neoden-yy1-pick-and-place-machine.html) small pick and place machine.

## Usage

    neoden_kicad --pos my_pos.csv --out neoden_pos.csv
