# GDSII-2-ASCII Dumper Utility

This is an utility for convert GDSII HEX stream data to readable ASCII format. GDSII is a data format used in semi-conductor mask layout.

### Prerequisite & Install:

* Windows, macOS, Linux
* [Python 3](https://www.python.org/)

### Run:

Open Terminal and run this command:

```
python3 gds2ascii.py <input.gds> <output.json>
```

### Test:

```
python3 -m unittest tests.test_gds2ascii -v
```

### GDSII Format Reference

* https://boolean.klaasholwerda.nl/interface/bnf/gdsformat.html
* http://bitsavers.informatik.uni-stuttgart.de/pdf/calma/GDS_II_Stream_Format_Manual_6.0_Feb87.pdf
