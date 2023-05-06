# sanwei

[![PyPI - Version](https://img.shields.io/pypi/v/sanwei.svg)](https://pypi.org/project/sanwei)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sanwei.svg)](https://pypi.org/project/sanwei)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```nix
nix shell git+https://github.com/fetsorn/sanwei

```

```console
pip install sanwei
```

## Usage

``` nix
# render a random chinese character with WenQuanYi Zen Hei font
nix build git+https://github.com/fetsorn/sanwei#image
```

``` console
sanwei --binary /path/to/blender \
       --font-path "/path/to/font" \
       --font-name "Font Name Regular"
```

## Docs

 - "--binary", required, path to Blender binary executable, e.g. "/Applications/Blender.app/Contents/MacOS/Blender"
 
 - "--font-path", required, path to chinese font, e.g. "./path/to/chinese.ttc"
 
 - "--font-name", required, name of the font in bpy.data.fonts, e.g. "Chinese Font Regular"
 
 - "--output", optional, name for output file without the .png extension, defaults to "/tmp/sanwei" and creates a "/tmp/sanwei.png" file
 
 - "--input", optional, arbitrary text to render, defaults to a random chinese character
 
 - "--resolution", optional, percentage scale for render resolution, int in [1, 32767], default 100
 
 - "--samples", optional, number of samples for the Cycles render engine, default 128

## License

`sanwei` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
