[![MSVC Conan](https://github.com/sintef-ocean/conan-miniconda/workflows/MSVC%20Conan/badge.svg)](https://github.com/sintef-ocean/conan-miniconda/actions?query=workflow%3A"MSVC+Conan")
[![Download](https://api.bintray.com/packages/sintef-ocean/conan/miniconda%3Asintef/images/download.svg)](https://bintray.com/sintef-ocean/conan/miniconda%3Asintef/_latestVersion)

[Conan.io](https://conan.io) recipe for [miniconda](https://docs.conda.io/).

The recipe helps to install miniconda on windows, setup channels and install packages. The package is usually consumed as a build requirement.
The default options is configured to allow unattended installation to get `flang`, `clang-cl` on windows. 

## How to use this package

1. Add remote to conan's package [remotes](https://docs.conan.io/en/latest/reference/commands/misc/remote.html?highlight=remotes):

   ```bash
   $ conan remote add sintef https://api.bintray.com/conan/sintef-ocean/conan
   ```

2. Use the conda environment

   ```bash
   $ conan install miniconda/4.9.2@sintef/testing `
       -g virtualenv `
       -o miniconda:packages=flang `
       -o miniconda:channels=conda-forge `
       --build missing
   $ activate.bat
   $ conda activate
   $ flang --version
   ```

## Package options

Option | Default | Domain
---|---|---
channels | conda-forge | Comma separated list
packages | flang,clangdev,perl,libflang | Comma separated list

## Known recipe issues

- The conda virtual environment is not activated by default. To use in a conan recipe, you need an active `RunEnvironment` and then call `conda activate && <your command>` in a `self.run`
- The installation interferes with other conda installations. It uses default (global) locations for some settings (see `conda config --show`)

