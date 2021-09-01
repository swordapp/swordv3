# SWORD 3.0

This repository contains the source files for the SWORD 3.0 specification.

To see the published specification go to https://swordapp.github.io/swordv3/swordv3.html


## Building from source

To compile the documentation in this repo:

1. Obtain the `compost` documentation builder:

```
git clone git@github.com:CottageLabs/compost.git
cd compost
pip install -r requirements.txt
```

2. Compile the source

```
cd [swordv3 source]
compost build config.json
```

This will compile the source for release on the swordv3 github pages.

If you wish to compile it for local use, you will need to make your own copy of `config.json` and adjust the settings
accordingly.