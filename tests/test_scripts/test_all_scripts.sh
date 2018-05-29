#!/usr/bin/env bash
python scripts/parser.py examples/errors/file_error.yaml > out.log
DIFF=$(diff out.log examples/errors/file_error.out)
if [ "$DIFF" != "" ]
then
    echo Difference between file_error
    exit 1
fi
python scripts/parser.py examples/errors/header_error.yaml > out.log
DIFF=$(diff out.log examples/errors/header_error.out)
if [ "$DIFF" != "" ]
then
    echo Difference between header_error
    exit 1
fi
python scripts/parser.py examples/errors/inherit_error.yaml > out.log
DIFF=$(diff out.log examples/errors/inherit_error.out)
if [ "$DIFF" != "" ]
then
    echo Difference between inherit_error
    exit 1
fi

python scripts/parser.py examples/errors/solvent_error.yaml > out.log
DIFF=$(diff out.log examples/errors/solvent_error.out)
if [ "$DIFF" != "" ]
then
    echo Difference between solvent_error
    exit 1
fi

python scripts/parser.py examples/errors/trough_error.yaml > out.log
DIFF=$(diff out.log examples/errors/trough_error.out)
if [ "$DIFF" != "" ]
then
    echo Difference between trough_error
    exit 1
fi