
/isilon/BL32XU/BLsoft/Other/RADDOSE/bin/raddose-03-01-08-distribute/raddose_ubuntu << EOF
ENERGY 12.398400
CELL 78 36 36 90 90 90
NRES 129
NMON 8
BEAM  0.010000 0.010000
PATM Fe 2 Cu 2 
CRYST 0.1000 0.1000 0.1000
SOLVENT 0.380000
PHOSEC 4.000000e+12
EXPO 1.000000
IMAGE 1
SATM Na 1500 Cl 1500 
EOF
