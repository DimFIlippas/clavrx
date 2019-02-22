# -*- coding: utf-8 -*-

import os
import sys
import argparse
import numpy as np
import stat

class clavrxBash(object):

    def createScript(self,):
        runvcm = ['#!/bin/bash','# Runs Clavrx from CSPP']
        runvcm.append('')
        runvcm.append('export CSPP_CLAVRX_HOME=$HOME/bin/CSPP/CLAVRx_2_0')
        runvcm.append('source $CSPP_CLAVRX_HOME/env/set_clavrx_env.sh')
        runvcm.append('CLAVRX=%s'%'$CSPP_CLAVRX_HOME/scripts/')
        runvcm.append('INPUT=%s'%self.InputPath)
        runvcm.append('WORKPATH=%s'%self.WorkPath)
        runvcm.append('OUTPATH=%s'%self.OutPath)
        runvcm.append('')
        runvcm.append('$CLAVRX/run_clavrx.sh ' + self.satellite + ' $INPUT $WORKPATH $OUTPATH')

        runvcm = [ l + '\n' for l in runvcm]

        if not os.path.exists(self.WorkPath):
            os.makedirs(self.WorkPath)
        f = open(self.scriptPath, "w")
        f.writelines(runvcm)
        f.close()

        st = os.stat(self.scriptPath)
        os.chmod(self.scriptPath, st.st_mode | stat.S_IEXEC)
        os.system(self.scriptPath)

    def __init__(self,satellite,InputPath,WorkPath,OutPath):
        self.satellite  = satellite
        self.InputPath  = InputPath
        self.WorkPath   = WorkPath
        self.OutPath    = OutPath

def main(argv):
    argparser  = argparse.ArgumentParser()
    argparser.add_argument("-s", "--satellite", type=str,required=True, default=None, help="INSTRUMENT_ID is 1 (AVHRR), 2 (MODIS) or 3 (VIIRS)")
    argparser.add_argument("-i", "--inputpath", type=str,required=True, default=None, help="input path")
    argparser.add_argument("-w", "--workpath", type=str,required=True, default=None, help="workpath folder")
    argparser.add_argument("-o", "--output"  , type=str,required=True, default=None, help="output path folder")
    args  = argparser.parse_args(argv[1:])

    satellite = args.satellite
    InputPath = args.inputpath
    WorkPath  = args.workpath
    OutPath   = args.output

    ClavrxB = clavrxBash(satellite,InputPath,WorkPath,OutPath)
    ClavrxB.createScript()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
