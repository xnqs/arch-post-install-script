# arch-post-install-script
WARNING: might hurt to look at the code.

Arch Post-Installation script for gamers. This script installs everything a gamer needs: Steam, Lutris, Discord, OBS, and it even configures your computer for the highest performance in gaming. (up to ~50% boost in some games, ~80% less performance hit when recording with OBS):

- OBS configured with zero-copy game capture (obs-vkcapture, might trigger some anti-cheats) and hardware acceleration for AMD
- Garuda's Performance Tweaks
- Feral Gamemode
- Custom kernel of the user's choice (Zen, Xanmod, TKG PDS, or user-specified kernel)
- Installs latest Mesa for AMD/Intel users (offers significant boost on RX 6000 series, and modest boost for the rest)
- Tuned CPU and IO scheduler for interactivity (as a part of the custom kernel)
- High Performance CPU governor

# Dependencies
Most dependencies auto-install with the script, but right now you have to install git and colorama manually:

`sudo pacman -S git python python-colorama`

# Installation
Clone the git repository:
```
mkdir ~/gitrepos && cd ~/gitrepos
git clone https://github.com/xnqs/arch-post-install-script/
```
Finally, execute the script as root:
```
sudo python arch-post-install-script.py
```

# How you can increase performance further
## For Ryzen 5000 series CPUs
The performance governor can actually be detrimental to performance when it comes to Ryzen 5000 series CPUs, as performance mode runs the CPU at full frequency, and doesn't take advantage of Ryzen 5000's turbo boost. You can remove the line in /etc/startupscript.sh that sets the CPU governor to performance. (cpupower frequency-set -g performance)
## Overclocking
This one applies to every OS, not just Linux, but is still worth it and can bring up to 25% higher performance, and even higher in some cases.
### With zenstates (Ryzen CPUs)
Zenstates is automatically installed by this script if it detects that you're running a Ryzen CPU. It can be accessed via the `zenstates` command.
More information can be found here: https://forum.level1techs.com/t/overclock-your-ryzen-cpu-from-linux/126025. It can also be added to /etc/startupscript.sh to take advantage of overclocking on boot.
### From BIOS
You can also just change frequency in the BIOS, but that will disable pstates/governors, and will always run at that higher frequency and voltage, even when not in load.

## Note
This script might still behave a bit weirdly, but nothing bad should happen.
