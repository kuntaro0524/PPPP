#!/bin/csh
rsync -auv kuntaro@kunfin.harima.riken.jp:/data/04.Prog/150518-Centering/ .
