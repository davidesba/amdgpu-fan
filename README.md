[![CircleCI](https://circleci.com/gh/chestm007/amdgpu-fan.svg?style=svg)](https://circleci.com/gh/chestm007/amdgpu-fan)  

# Fan controller for amdgpus [python3 only]

If you experience problems please create an issue.

## installation:
### pip
`sudo pip3 install amdgpu-fan`

### Arch linux
Available in the aur as `amdgpu-fan`

## usage:  
`sudo amdgpu-fan`  

## configuration:
```
# /etc/amdgpu-fan.yml
# eg:

speed_matrix:  # -[temp(*C), speed(0-100%)]
  gpu:
    - [0, 0]
    - [40, 30]
    - [60, 50]
    - [80, 100]
  juction:
    - [0, 0]
    - [60, 30]
    - [70, 50]
    - [110, 100]
  mem:
    - [0, 0]
    - [80, 40]
    - [95, 80]
    - [100, 100]

# optional
# cards:  # can be any card returned from 
#         # ls /sys/class/drm | grep "^card[[:digit:]]$"
# - card0
```


