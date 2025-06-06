
Hyspecppt
==========

Tool that enables users to analyze polarized neutron experiments on powder and single crystal samples using the HYSPEC instrument.

## Installation Process

Create the development conda environment

`conda env create`

Activate the environment

`conda activate hyspecppt_dev`

Install the application in editable mode

`pip install -e .`

Start the tool

`hyspecppt`


## Documentation Build locally

Enter the documentation directory

`cd docs\`

Clean current build files, if they exist

`make clean`

Build the html files

`make html`

Documentation [hyspecppt.readthedocs.io](https://hyspecppt.readthedocs.io/)


[![CI](https://github.com/neutrons/hyspecppt/actions/workflows/unittest.yml/badge.svg?branch=next)](https://github.com/neutrons/hyspecppt/actions/workflows/unittest.yml)
[![codecov](https://codecov.io/gh/neutrons/hyspecppt/graph/badge.svg?token=GAQE3SS0HJ)](https://codecov.io/gh/neutrons/hyspecppt)
