
Hyspecppt
==========

Tool that enables users to analyze polarized neutron experiments on powder and single crystal samples using the HYSPEC instrument.

## Installation Process

Create and activate a virtual environment with [Pixi](https://pixi.sh/).Prerequisites: Pixi installation e.g. for Linux:

`curl -fsSL https://pixi.sh/install.sh | sh`

Download the repository. Setup/Update the environment

`pixi install`

Enter the environment

`pixi shell`

Start the tool

`hyspecppt`

## For Contributors

**Development/Deployment**


---

Any change to pyproject.toml, e.g. new dependencies, requires updating the pixi.lock file and including it in the commit.

```bash

pixi.lock

```


## Documentation Build locally

Enter the documentation directory

`cd docs\`

Build the doc locally into "build/html" folder:

`pixi run sphinx-build -T -b html docs/source build/html`

Documentation [hyspecppt.readthedocs.io](https://hyspecppt.readthedocs.io/)


[![CI](https://github.com/neutrons/hyspecppt/actions/workflows/test_and_deploy.yml/badge.svg?branch=next)](https://github.com/neutrons/hyspecppt/actions/workflows/test_and_deploy.yml)
[![codecov](https://codecov.io/gh/neutrons/hyspecppt/graph/badge.svg?token=GAQE3SS0HJ)](https://codecov.io/gh/neutrons/hyspecppt)
