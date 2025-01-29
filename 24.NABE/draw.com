#!/bin/bash
/isilon/BL32XU/BLsoft/PPPP/24.NABE/pymol/pymol -cpqk < $PWD/draw_map.pml
