# PlatformIO platform package for Open Sourced Radio MCUs

```LICENSE
Copyright [2024] [Amo Xu BD4VOW <amo@git.ltd>]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

### Installation:
1. Click "PlatformIO Core CLI" from VSCode PlatformIO Panel -> Quick Access -> Miscellaneous.
2. Enter below install commands:
``` 
pio pkg install -g -p https://github.com/amoxu/platform-openradiox
```

### When you are using under Linux, before using, you need to install the udev rules for OpenOCD
1. Copy the 60-openocd.rules file under tool-openocd-at32 package to /etc/udev/rules.d/ directory.
```
sudo cp ~/.platformio/packages/tool-openocd-at32/contrib/60-openocd.rules  /etc/udev/rules.d/
```
2. Refresh the udev rules.
```
sudo udevadm control --reload-rules && sudo udevadm trigger
```