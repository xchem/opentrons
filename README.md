[![Build Status](https://travis-ci.org/xchem/opentrons.svg?branch=master)](https://travis-ci.org/xchem/opentrons)
[![experimental](http://badges.github.io/stability-badges/dist/experimental.svg)](http://github.com/xchem/opentrons)
[![Version](http://img.shields.io/badge/version-0.0.16-blue.svg?style=flat)](https://github.com/xchem/opentrons)
[![License](http://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat)](https://github.com/xchem/opentrons/blob/master/LICENSE.txt)

# Opentrons repo for parallel chemistry reactions

## Usage

Requirements - RDKit
### Install
```bash
pip install xchem-ot
xchem_ot /path/to/file.yaml
```
OR
```bash
git clone https://github.com/xchem/opentrons
cd opentrons
python setup.py install 
cd examples 
xchem_ot --yaml_path acylation.yaml
# one with inheritance
xchem_ot --yaml_path coupling.yaml
```
