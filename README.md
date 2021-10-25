# arch-post-install-script
WARNING: might hurt to look at the code.

Arch Post-Installation script for gamers. This script installs everything a gamer needs: Steam, Lutris, Discord, OBS, and it even configures your computer for the highest performance in gaming. (up to ~35% boost in some games, way less performance hit when recording with OBS):

- OBS configured with zero-copy game capture (obs-vkcapture, might trigger some anti-cheats) and hardware acceleration for AMD
- Garuda's Performance Tweaks
- Feral Gamemode
- Custom kernel of the user's choice (Zen, Xanmod or TKG PDS)
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

## Note
This script assumes there is only one user other than root, with the user ID of 1000.
