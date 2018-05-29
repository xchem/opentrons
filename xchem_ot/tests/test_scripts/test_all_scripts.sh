#!/usr/bin/env bash
xchem_ot --yaml_path examples/errors/file_error.yaml > out.log
DIFF=$(diff out.log examples/errors/file_error.out)
if [ "$DIFF" != "" ]
then
    echo Difference between file_error
    exit 1
fi
xchem_ot --yaml_path examples/errors/header_error.yaml > out.log
DIFF=$(diff out.log examples/errors/header_error.out)
if [ "$DIFF" != "" ]
then
    echo Difference between header_error
    exit 1
fi
rm -r acylation_*
xchem_ot --yaml_path examples/errors/inherit_error.yaml > out.log
DIFF=$(diff out.log examples/errors/inherit_error.out)
if [ "$DIFF" != "" ]
then
    echo Difference between inherit_error
    exit 1
fi
xchem_ot --yaml_path examples/errors/solvent_error.yaml > out.log
DIFF=$(diff out.log examples/errors/solvent_error.out)
if [ "$DIFF" != "" ]
then
    echo Difference between solvent_error
    exit 1
fi
rm -r acylation_*
xchem_ot --yaml_path examples/errors/trough_error.yaml > out.log
DIFF=$(diff out.log examples/errors/trough_error.out)
if [ "$DIFF" != "" ]
then
    echo Difference between trough_error
    exit 1
fi