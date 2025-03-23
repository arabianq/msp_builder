[New tool](https://github.com/arabianq/build_msp)

---

# Small script to build .msp mod file
Tested on linux only

### Requirements
- _build_pfs0_ and _build_romfs_ from [switch-tools](https://github.com/switchbrew/switch-tools)

### Usage

```
usage: build_msp [-h] [-i INPUT] [-o OUTPUT] [-m MANIFEST]

options:
  -h, --help            show this help message and exit
  -i, --input INPUT     Input directory
  -o, --output OUTPUT   Output file
  -m, --manifest MANIFEST
                        Manifest file
```

### Manifest file example
```
titleid=0100D3F008746000
version=65536
patchset=kpnp_russ
```
- _titleid_ - title_id of a game (required)
- _version_ - recommended game version (optional)
- _patchset_- name for the .ips patches directory (optional)
