#!/usr/bin/env python3

# IMPORT NECESSARY LIBRARIES
import os
import getpass
import re
import math

def install_dependencies():
    print("Installing dependencies...\n")
    if not(bool(os.popen("pacman -Q | grep 'python-colorama'").read().strip())):
        os.system("sudo pacman -S python-colorama")

install_dependencies()
from colorama import init, Fore, Back, Style
init()

# removes temp dir if already there
notfirstrun = os.path.isdir("/tmp/arch-post-install-script/")
if notfirstrun:
    os.system("sudo rm -rf /tmp/arch-post-install-script/")
    os.mkdir("/tmp/arch-post-install-script/")
else:
    os.mkdir("/tmp/arch-post-install-script/")

# check what and how many other users there are
os.system("cut -d: -f1,3 /etc/passwd | egrep ':[0-9]{4}$' | cut -d: -f1 > /tmp/arch-post-install-script/users.xnqs")
with open("/tmp/arch-post-install-script/users.xnqs") as file_userlist:
    file_userlist_linecount = file_userlist.readlines()
    user_count = len(file_userlist_linecount)
if user_count > 1:
    print("\nMultiple users detected. Type your username below.\n")
    os.system("cat /tmp/arch-post-install-script/users.xnqs")
    other_user = input(f"\n{Fore.BLUE}> {Style.RESET_ALL}")
else:
    other_user = open("/tmp/arch-post-install-script/users.xnqs", "r").read().strip()

# check ram size
with open('/proc/meminfo') as f:
    meminfo = f.read()
matched = re.search(r'^MemTotal:\s+(\d+)', meminfo)
if matched:
    mem_total_gB = math.floor(int(matched.groups()[0])/1024/1024)

# DICTIONARIES
user_info = {
    "user": getpass.getuser(),
    "yay_installed": bool(os.popen("pacman -Q | grep 'yay'").read().strip()),
    "uid": os.popen("id -u " + other_user).read().strip(),
    "amdgpu": bool(os.popen("lspci | grep VGA | grep AMD").read().strip()),
    "freegpu": bool(os.popen("lspci | grep VGA | grep AMD").read().strip() or os.popen("lspci | grep VGA | grep Intel").read().strip() or os.popen("lspci | grep VGA | grep QXL").read().strip()),
    "amdcpu": bool(os.popen("cat /proc/cpuinfo | grep Ryzen").read().strip()),
    "is_on_manjaro": bool(os.popen("cat /etc/lsb-release | grep Manjaro").read().strip()),
    "chaotic_installed": bool(os.popen("cat /etc/pacman.conf | grep chaotic").read().strip()),
    "multilib": bool(os.popen("pacman -Syy | grep multilib").read().strip()),
    "mesa-git": bool(os.popen("pacman -Q mesa | grep mesa-git").read().strip()),
    "colorama_installed": bool(os.popen("pacman -Q | grep 'python-colorama'").read().strip()),
    "pwd": os.popen("pwd").read().strip()
}

user_optin = {
    "chaoticaur": "bleh",
    "de": "bleh",
    "software": "bleh",
    "goverlay": "bleh",
    "amf": "bleh",
    "kernel": "bleh",
    "kernelsure": "bleh",
    "pipewire": "bleh",
    "performance": "bleh",
    "mesa-git": "bleh",
    "zram": "bleh",
    "otherstartuptweaks": "bleh",
    "vfio": "bleh",
    "de_option": "bleh",
    "kerneloption": "bleh"
}

packages = {
    "manjaro_zen_mirrorlist": "Server=https://archive.archlinux.org/repos/last/$repo/os/$arch",
    "chaoticaur": "\n[chaotic-aur]\nInclude = /etc/pacman.d/chaotic-mirrorlist\n",
    "lutrisdeps": ("wine-tkg-staging-fsync-git giflib lib32-giflib libpng lib32-libpng libldap lib32-libldap gnutls lib32-gnutls mpg123 lib32-mpg123 openal lib32-openal v4l-utils lib32-v4l-utils libpulse lib32-libpulse libgpg-error lib32-libgpg-error alsa-plugins lib32-alsa-plugins alsa-lib lib32-alsa-lib libjpeg-turbo lib32-libjpeg-turbo sqlite lib32-sqlite libxcomposite lib32-libxcomposite libxinerama lib32-libgcrypt libgcrypt lib32-libxinerama ncurses lib32-ncurses opencl-icd-loader lib32-opencl-icd-loader libxslt lib32-libxslt libva lib32-libva gtk3 lib32-gtk3 gst-plugins-base-libs lib32-gst-plugins-base-libs vulkan-icd-loader lib32-vulkan-icd-loader", "wine-staging giflib lib32-giflib libpng lib32-libpng libldap lib32-libldap gnutls lib32-gnutls mpg123 lib32-mpg123 openal lib32-openal v4l-utils lib32-v4l-utils libpulse lib32-libpulse libgpg-error lib32-libgpg-error alsa-plugins lib32-alsa-plugins alsa-lib lib32-alsa-lib libjpeg-turbo lib32-libjpeg-turbo sqlite lib32-sqlite libxcomposite lib32-libxcomposite libxinerama lib32-libgcrypt libgcrypt lib32-libxinerama ncurses lib32-ncurses opencl-icd-loader lib32-opencl-icd-loader libxslt lib32-libxslt libva lib32-libva gtk3 lib32-gtk3 gst-plugins-base-libs lib32-gst-plugins-base-libs vulkan-icd-loader lib32-vulkan-icd-loader"), 
    "gaming_stuff": "yay neovim cpupower lutris vkd3d lib32-vkd3d steam proton-ge-custom heroic-games-launcher-bin lib32-gamemode gamemode mangohud obs-streamfx obs-studio-browser retroarch discord_arch_electron",
    "software": "chromium vlc spotify qbittorrent yuzu kdenlive olive noisetorch grapejuice-git onlyoffice-bin",
    "pulse": (
        "pulseaudio",
        "pulseaudio-alsa",
        "pulseaudio-bluetooth",
        "pulseaudio-jack",
        "pulseaudio-zeroconf",
        "pulseaudio-equalizer"
    ),
    "pipewire": "alsa-card-profiles pipewire pipewire-alsa pipewire-media-session pipewire-pulse pipewire-jack pipewire-zeroconf",
    "zram": (
        "modprobe zram",
        "echo lz4 > /sys/block/zram0/comp_algorithm",
        "echo " + str(mem_total_gB) + "G > /sys/block/zram0/disksize",
        "mkswap --label zram0 /dev/zram0",
        "swapon --priority 100 /dev/zram0"
    )
}

startup_script = {    
    "startup_script": ("#!/bin/bash\n# overclock\n# zenstates -p 0 -f 98 -d 8 -v 20\ncpupower frequency-set -g performance\n\n# disable multi-generational lru, linux-zen runs awfully because of this\necho 0 | tee /sys/kernel/mm/lru_gen/enabled", "[Unit]\nAfter=hibernate.target\nAfter=hybrid-sleep.target\nAfter=suspend.target\nAfter=suspend-then-hibernate.target\nDescription=Startup Script\n\n[Service]\nExecStart=/etc/startupscript.sh\n\n[Install]\nWantedBy=multi-user.target\nWantedBy=hibernate.target\nWantedBy=hybrid-sleep.target\nWantedBy=suspend.target\nWantedBy=suspend-then-hibernate.target"),
}

# VARIABLES
yes = ("y", "")
no = ("n")
nodefault = ("n", "")
yes_or_no = ("y", "", "n")

# CORE FUNCTIONS
def disclaimer():
    os.system("clear")
    input(f"""{Fore.BLUE}Disclaimer: This script is still being tested, and you might encounter some weird or out of place behaviour, such as some prompts not registering properly, or incompatibility with some Arch-based distros. If you do so, please report it on GitHub so I can fix it.\nJust don't close the script in the middle of execution, and you'll be fine. You can, however, safely Ctrl+C it at a Yes or No prompt.\n\nIf you understand the risks, press Enter. Otherwise, press Ctrl+C.{Style.RESET_ALL}""")
    print(f"\nArch Post-Installation Script b0.97 - {Fore.BLUE}sqnx.{Style.RESET_ALL}")
    print("\nHey there! You probably just finished installing Arch, and you want to get straight into the meat and potatoes. I'll install everything you need so you don't have to!")
    print("So basically, what this script will do is it will set up your Arch for high-performance gaming, as the default settings are absolutely abysmal for gaming. I will also install some software that is nice to have for gamers, or literally anyone else, such as OBS configured with DMA-BUF capture for games and Discord with enabled OpenH264. It also installs NVFBC if you're on NVIDIA, which does the same thing as obs-vkcapture, but for NVIDIA GPUs. This script also installs Feral Gamemode, which automatically maxes out your CPU frequency when in a game, resulting in significantly better performance (up to 50% increase in some especially demanding titles). Among other things, you also have a choice to install a graphical environment if you haven't already. With that said, let's get right into it!") 

def user_is_not_root():
    print(f"\nYou're running this as {Fore.RED}" + user_info["user"] + f"""{Style.RESET_ALL}, so this post-installation script will cease to work.\nPlease run this script as {Fore.GREEN}root{Style.RESET_ALL}, either by adding {Fore.GREEN}sudo{Style.RESET_ALL} before the installation script, or by simply running it while logged into the {Fore.GREEN}root{Style.RESET_ALL} account.\n""")

def confirm():
    input("\nPress enter to continue.")
    print(f"\nYou're running this as {Fore.GREEN}" + user_info["user"] + f"{Style.RESET_ALL}, which is exactly what we need in order to continue with the installation process. :D")

def manjaro_switch_to_unstable():
    if user_info["is_on_manjaro"]:
        print(f"\n{Fore.BLUE}==> Manjaro detected. Switching to Unstable branch, which is actually more stable...{Style.RESET_ALL}")
        os.system("pacman-mirrors --api --set-branch unstable")
        os.system("pacman-mirrors --fasttrack 5 && pacman -Syyu")

def install_yay():
    print(f"\n{Fore.BLUE}==> Installing yay AUR helper, as it is necessary to continue.{Style.RESET_ALL}")
    if not user_info["yay_installed"]:
        os.system("sudo -u " + str(other_user) + " git clone https://aur.archlinux.org/yay.git /tmp/yay/")
        os.chdir("/tmp/yay/")
        os.system("sudo -u " + str(other_user) + " makepkg -scif")
        os.chdir(user_info["pwd"])
    else:
        print(f"{Fore.BLUE}==> Yay is already installed, so skipping...{Style.RESET_ALL}")

def install_other_deps():
    print(f"\n{Fore.BLUE}==> Installing other dependencies...{Style.RESET_ALL}")
    os.system("pacman -S --needed base-devel")
    if user_info["amdgpu"] and not(user_info["mesa-git"]):
        os.system("pacman -S --needed mesa lib32-mesa vulkan-radeon lib32-vulkan-radeon mesa-vdpau lib32-mesa-vdpau libva-mesa-driver lib32-libva-mesa-driver xf86-video-amdgpu")

def install_chaotic():
    print(f"\n{Fore.BLUE}==> So first, let's start off with the Chaotic AUR!{Style.RESET_ALL}")
    while user_optin["chaoticaur"] not in yes_or_no:
        user_optin["chaoticaur"] = input(f"\n{Fore.BLUE}==> Do you wish to add the Chaotic AUR to your repository list? (Highly recommended, makes running this script a lot easier and faster) (Y/n): {Style.RESET_ALL}").lower()
        if user_optin["chaoticaur"] in yes:
            user_optin["chaoticaur"] = True
            if not user_info["chaotic_installed"]:
                print(f"{Fore.BLUE}==> Adding Chaotic AUR...{Style.RESET_ALL}")
                os.system("pacman-key --recv-key FBA220DFC880C036 --keyserver keyserver.ubuntu.com")
                os.system("pacman-key --lsign-key FBA220DFC880C036")
                os.system("pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst' 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'")
                file_pacman = open("/etc/pacman.conf", "a")
                file_pacman.write(packages["chaoticaur"])
                file_pacman.close()
                os.system("pacman -Syy")
            else:
                print(f"{Fore.BLUE}==> Skipping Chaotic AUR because it is already installed...{Style.RESET_ALL}")
            break
        elif user_optin["chaoticaur"] in no:
            user_optin["chaoticaur"] = False
            print(f"\n{Fore.BLUE}==> Skipping Chaotic AUR... {Style.RESET_ALL}")
            break
        else:
            print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")

def install_desktop_environment():
    while user_optin["de"] not in yes_or_no:
        user_optin["de"] = input(f"\n{Fore.BLUE}==> Do you want to install a desktop environment? (Y/n) {Style.RESET_ALL}").lower()
        if user_optin["de"] in yes:
            while user_optin["de_option"] not in ("1", "", "2", "3", "4", "5"):
                print(f"{Fore.BLUE}==> Which desktop environment do you want to install?{Style.RESET_ALL}\n1. KDE (Default)\n2. GNOME\n3. Xfce\n4. i3wm\n5. Nevermind.")
                user_optin["de_option"] = input(f"\n{Fore.BLUE}> {Style.RESET_ALL}")
                if user_optin["de_option"] in ("1", ""):
                    os.system("pacman -S --needed plasma papirus-icon-theme adobe-source-sans-fonts materia-kde")
                    break
                elif user_optin["de_option"] == "2":
                    os.system("pacman -S --needed gnome papirus-icon-theme adobe-source-sans-fonts materia-gtk-theme")
                    break
                elif user_optin["de_option"] == "3":
                    os.system("pacman -S --needed xfce4 papirus-icon-theme adobe-source-sans-fonts materia-gtk-theme")
                    break
                elif user_optin["de_option"] == "4":
                    os.system("pacman -S --needed i3 i3blocks adobe-source-sans-fonts otf-font-awesome")
                    break
                elif user_optin["de_option"] == "5":
                    print(f"{Fore.BLUE}==> Skipping Desktop Environment...{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
            break
        elif user_optin["de"] in no:
            print(f"{Fore.BLUE}==> Skipping Desktop Environment...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.BLUE}==> Invalid choice.{Style.RESET_ALL}")

def add_multilib_repo():
    print(f"\n{Fore.BLUE}==> Adding multilib repo for Wine and other gaming tools...{Style.RESET_ALL}")
    if not user_info["multilib"]:
        with open("/etc/pacman.conf", "a") as file_multilib:
            file_multilib.write("[multilib]\nInclude = /etc/pacman.d/mirrorlist")
    else:
        print(f"{Fore.BLUE}==> Skipping multilib because it is already installed...{Style.RESET_ALL}")

def install_lutris_deps():
    print(f"\n{Fore.BLUE}==> Installing Lutris Dependencies...{Style.RESET_ALL}")
    if user_optin["chaoticaur"]:
        os.system("pacman -S --needed " + packages["lutrisdeps"][0])
    else:
        os.system("pacman -S --needed " + packages["lutrisdeps"][1])

def install_lutris_and_other_gaming_tools():
    print(f"\n{Fore.BLUE}==> Installing Lutris, Steam, and other gaming-related stuff...{Style.RESET_ALL}")
    if user_optin["chaoticaur"]:
        if user_info["freegpu"] or user_info["amdgpu"]:
            os.system("pacman -S --needed " + packages["gaming_stuff"] + " corectrl obs-vkcapture-git lib32-obs-vkcapture-git")
        else:
            os.system("pacman -S --needed " + packages["gaming_stuff"] + " gwe obs-nvfbc")
    else:
        if user_info["freegpu"] or user_info["amdgpu"]:
            os.system("sudo -u " + str(other_user) + " yay -S " + packages["gaming_stuff"] + " corectrl obs-vkcapture-git lib32-obs-vkcapture-git")
        else:
            os.system("sudo -u " + str(other_user) + " yay -S " + packages["gaming_stuff"] + " gwe obs-nvfbc")

def install_other_software():
    while user_optin["software"] not in yes_or_no:
        user_optin["software"] = input(f"\n{Fore.BLUE}==> Do you want to install some extra software? (e.g Spotify, QBitTorrent, VLC, Olive, Kdenlive, Yuzu (switch emulator), etc. (Y/n): {Style.RESET_ALL}").lower()
        if user_optin["software"] in yes:
            print(f"{Fore.BLUE}==> Installing extra software... {Style.RESET_ALL}")
            os.system("sudo -u " + str(other_user) + " yay -S " + packages["software"])
            break
        elif user_optin["software"] in no:
            print(f"{Fore.BLUE}==> Skipping extra software... {Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")

def install_amf():
    if user_info["amdgpu"]:
        if user_optin["chaoticaur"]:
            print(f"\n{Fore.BLUE}==> Installing AMF for OBS hardware-accelerated encoding...{Style.RESET_ALL}")
            if not user_info["mesa-git"]:
                os.system("pacman -S --needed vulkan-amdgpu-pro amf-amdgpu-pro vulkan-radeon lib32-vulkan-radeon")
            else:
                os.system("pacman -S --needed vulkan-amdgpu-pro amf-amdgpu-pro")
        else:
            while user_optin["amf"] not in yes_or_no:
                user_optin["amf"] = input(f"{Fore.BLUE}==> I see you haven't added Chaotic AUR so this is gonna take a while... Do you actually want to install AMF? (Y/n) {Style.RESET_ALL}").lower()
                if user_optin["amf"] in yes:
                    if not user_info["mesa-git"]:
                        print(f"{Fore.BLUE}==> Installing AMF for OBS hardware-accelerated encoding...{Style.RESET_ALL}")
                        os.system("sudo -u " + str(other_user) + " yay -S vulkan-amdgpu-pro amf-amdgpu-pro vulkan-radeon lib32-vulkan-radeon")
                    else:
                        print(f"{Fore.BLUE}==> Installing AMF for OBS hardware-accelerated encoding...{Style.RESET_ALL}")
                        os.system("sudo -u " + str(other_user) + " yay -S vulkan-amdgpu-pro amf-amdgpu-pro")
                    break
                elif user_optin["amf"] in no:
                    print(f"{Fore.BLUE}==> Skipping AMF for OBS hardware-accelerated encoding...{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")

def install_goverlay():
    while user_optin["goverlay"] not in yes_or_no:
        user_optin["goverlay"] = input(f"\n{Fore.BLUE}==> Do you want to install GOverlay? (instant replay + fps hud solution) (Y/n) {Style.RESET_ALL}").lower()
        if user_optin["goverlay"] in yes:
            print(f"{Fore.BLUE}==> Installing GOverlay... {Style.RESET_ALL}")
            os.system("sudo -u " + str(other_user) + " yay -S goverlay-git")
            print(f"{Fore.BLUE}==> Setting up zero-copy instant-replay capture for ReplaySorcery... {Style.RESET_ALL}")
            os.system("cp /usr/etc/replay-sorcery.conf /home/" + str(other_user) + "/.config/replay-sorcery.conf")
            with open("/home/" + str(other_user) + "/.config/replay-sorcery.conf","r") as f:
                f_lines = f.readlines() 
            with open("/home/" + str(other_user) + "/.config/replay-sorcery.conf","w") as f:
                for i, line in enumerate(f_lines):
                    if "videoInput" in line:
                        f_lines[i] = "videoInput = hwaccel\n"
                    if "videoFramerate" in line:
                        f_lines[i] = "videoFramerate = 60\n"
                    if "audioProfile" in line:
                        f_lines[i] = "audioProfile = main\n"
                f.writelines(f_lines)
            os.system("systemctl enable --now replay-sorcery-kms")
            os.system("sudo -u " + other_user + " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(user_info["uid"]) + "/bus XDG_RUNTIME_DIR=/run/user/" + str(user_info["uid"]) + " systemctl --user enable --now replay-sorcery")
            break
        elif user_optin["goverlay"] in no: 
            print(f"{Fore.BLUE}==> Skipping GOverlay... {Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")

def kernel_install_zen():
    if user_info["is_on_manjaro"]:
        print(f"{Fore.BLUE}==> User is on Manjaro, which doesn't have Zen in its repos, so installing latest Zen kernel from the Arch Linux Archive. Update this every now and then.{Style.RESET_ALL}")
        os.system("cat /etc/pacman.d/mirrorlist > /tmp/arch-post-install-script/mirrorlist.xnqs")
        with open("/etc/pacman.d/mirrorlist", "w") as file_manjaro_mirrorlist:
            file_manjaro_mirrorlist.write(packages["manjaro_zen_mirrorlist"])
        os.system("pacman -Syy linux-zen linux-zen-headers")
        os.system("cat /tmp/arch-post-install-script/mirrorlist.xnqs > /etc/pacman.d/mirrorlist")
        os.system("pacman -Syy")
    else:
        os.system("pacman -S linux-zen linux-zen-headers")

def kernel_install_clear():
    while user_optin["kernelsure"] not in yes_or_no:
        user_optin["kernelsure"] = input(f"\n{Fore.BLUE}==> Are you sure you want to install a custom kernel from the AUR? This will take from a couple of minutes, up to a few hours, depending on your hardware. (Y/n) {Style.RESET_ALL}").lower()
        if user_optin["kernelsure"] in yes:
            os.system("sudo -u " + str(other_user) + " yay -S --editmenu linux-clear linux-clear-headers")
            break
        elif user_optin["kernelsure"] in no:
            print(f"{Fore.BLUE}==> Skipping Custom Kernel... {Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")

def kernel_install_xanmod():
    if user_optin["chaoticaur"]:
        os.system("pacman -S linux-xanmod-cacule linux-xanmod-cacule-headers")
    else:
        while user_optin["kernelsure"] not in yes_or_no:
            user_optin["kernelsure"] = input(f"\n{Fore.BLUE}==> Are you sure you want to install a custom kernel from the AUR? This will take from a couple of minutes, up to a few hours, depending on your hardware. (Y/n) {Style.RESET_ALL}").lower()
            if user_optin["kernelsure"] in yes:
                os.system("sudo -u " + str(other_user) + " yay -S --editmenu linux-xanmod-cacule linux-xanmod-cacule-headers")
                break
            elif user_optin["kernelsure"] in no:
                print(f"{Fore.BLUE}==> Skipping Custom Kernel... {Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")

def kernel_install_tkg_pds():
    if user_optin["chaoticaur"]:
        os.system("pacman -S linux-tkg-pds linux-tkg-pds-headers")
    else:     
        print(f"\n{Fore.BLUE}==> Skipping Selected Custom Kernel because it's only available in the Chaotic AUR... {Style.RESET_ALL}")

def kernel_install_custom():
    user_optin["customkerneloption"] = input(f"\nType custom kernel package name below. (e.g linux-zen-git installs linux-zen-git and linux-zen-git-headers):\n{Fore.BLUE}> {Style.RESET_ALL}").lower()
    os.system("sudo -u " + str(other_user) + " yay -S --editmenu" + user_optin["customkerneloption"] + " " + user_optin["customkerneloption"] + "-headers")

def install_kernel():
    while user_optin["kernel"] not in yes_or_no:
        user_optin["kernel"] = input(f"\n{Fore.BLUE}==> Do you want to install a custom kernel? (Y/n) {Style.RESET_ALL}").lower()
        if user_optin["kernel"] in yes:
            while user_optin["kerneloption"] not in ("1", "", "2", "3", "4", "5"):
                print(f"\n{Fore.BLUE}==> Which custom kernel suits your needs best? (If in doubt, just choose 1.)\n{Style.RESET_ALL}1. Zen Kernel (default, also my personal favourite)\n2. Clear Kernel (Intel's performance-oriented kernel, might perform really well on Zen 3 or newer Intel chips)\n3. Xanmod (Raw performance-oriented kernel, might behave weirdly at 100% load, needs Chaotic AUR or regular AUR)\n4. Linux TKG (mileage may vary on some hardware as opposed to the Zen kernel, like mine for example, needs Chaotic)\n5. Custom kernel specified by user\n6. Nevermind.")
                user_optin["kerneloption"] = input(f"\n{Fore.BLUE}> {Style.RESET_ALL}")
                if user_optin["kerneloption"] in ("1", ""):
                    kernel_install_zen()
                    break
                elif user_optin["kerneloption"] == "2":
                    kernel_install_clear()
                    break
                elif user_optin["kerneloption"] == "3":
                    kernel_install_xanmod()
                    break
                elif user_optin["kerneloption"] == "4":
                    kernel_install_tkg_pds()
                    break
                elif user_optin["kerneloption"] == "5":
                    kernel_install_custom()
                    break
                elif user_optin["kerneloption"] == "6":
                    print(f"\n{Fore.BLUE}==> Skipping Custom Kernel... {Style.RESET_ALL}")
                    break
                else:
                    print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
            break
        elif user_optin["kernel"] in no:
            print(f"{Fore.BLUE}==> Skipping Custom Kernel... {Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")

def install_pipewire():
    while user_optin["pipewire"] not in yes_or_no:
        user_optin["pipewire"] = input(f"\n{Fore.BLUE}==> Do you want to replace legacy PulseAudio with Pipewire (a newer and better low latency audio server)? (Y/n) {Style.RESET_ALL}").lower()
        if user_optin["pipewire"] in yes:
            print(f"{Fore.BLUE}==> Installing Pipewire... {Style.RESET_ALL}")
            for i in range(len(packages["pulse"])):
                os.system("pacman -Rdd " + packages["pulse"][i])
            os.system("pacman -S " + packages["pipewire"])
            os.system("killall -s SIGKILL pulseaudio")
            os.system("sudo -u " + other_user + " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(user_info["uid"]) + "/bus XDG_RUNTIME_DIR=/run/user/" + str(user_info["uid"]) + " systemctl --user enable --now pipewire pipewire-pulse pipewire-media-session")
            break
        elif user_optin["pipewire"] in no:
            print(f"{Fore.BLUE}==> Leaving PulseAudio as it is... {Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")

def install_garuda_performance_tweaks():
    if user_optin["chaoticaur"]:
        os.system("pacman -S performance-tweaks")
    else:
        print(f"{Fore.BLUE}==> Chaotic AUR not added, so skipping Garuda Performance Tweaks...{Style.RESET_ALL}")

def install_mesa_git():
    if user_info["amdgpu"]:
        while user_optin["mesa-git"] not in yes_or_no:
            user_optin["mesa-git"] = input(f"\n{Fore.BLUE}==> Install Experimental Mesa? (typically gives a performance boost compared to Mesa, especially on RX 6000 series) (Y/n) {Style.RESET_ALL}").lower()
            if user_optin["mesa-git"] in yes:
                if not user_info["mesa-git"]:
                    print(f"{Fore.BLUE}==> Installing Experimental Mesa... {Style.RESET_ALL}")
                    if user_optin["chaoticaur"]:
                        os.system("pacman -S mesa-git lib32-mesa-git")
                    else:
                        os.system("sudo -u " + str(other_user) + " yay -S mesa-git lib32-mesa-git")
                    break
                else:
                    print(f"{Fore.BLUE}==> mesa-git package already installed. Skipping... {Style.RESET_ALL}")
                    break
            elif user_optin["mesa-git"] in no:
                print(f"{Fore.BLUE}==> Skipping Experimental Mesa... {Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")

def enable_fsync():
    print(f"\n{Fore.BLUE}==> Enabling FSync in bashrc for Wine games to run better... {Style.RESET_ALL}")
    with open("/etc/bash.bashrc", "a") as file_bashrc:
        file_bashrc.write("\nexport WINEESYNC=1\nexport WINEFSYNC=1")

def install_zenstates():
    if user_info["amdcpu"]:
        print(f"\n{Fore.BLUE}==> Installing Zenstates for Ryzen Overclocking... {Style.RESET_ALL}")
        os.system("sudo -u " + str(other_user) + " yay -S zenstates-git")
    else:
        print(f"{Fore.BLUE}==> Skipping Zenstates, since user is not on a Ryzen CPU... {Style.RESET_ALL}")

def overall_performance_setup():
    while user_optin["performance"] not in yes_or_no:
        user_optin["performance"] = input(f"\n{Fore.BLUE}==> Do you want to install some performance tweaks while you're at it? (Y/n) {Style.RESET_ALL}").lower()
        if user_optin["performance"] in yes:
            install_garuda_performance_tweaks()
            install_mesa_git()
            enable_fsync()
            install_zenstates()
        elif user_optin["performance"] in no:
            print(f"{Fore.BLUE}==> Skipping performance tweaks... {Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")

def enable_zram():
    while user_optin["zram"] not in yes_or_no:
        user_optin["zram"] = input(f"\n{Fore.BLUE}==> Do you want to add RAM compression (zram, really good for users with low ram or using SSDs)? (Y/n) {Style.RESET_ALL}").lower()
        if user_optin["zram"] in yes:
            print(f"{Fore.BLUE}==> Setting up zram... {Style.RESET_ALL}")
            with open('/etc/modules-load.d/zram.conf', 'w') as f:
                f.write("zram\n")
            with open('/etc/modprobe.d/zram.conf', 'w') as f:
                f.write("options zram num_devices=1\n")
            with open('/etc/udev/rules.d/99-zram.rules', 'w') as f:
                f.write("KERNEL==\"zram0\", ATTR{disksize}=\"" + str(mem_total_gB) + "G\" RUN=\"/usr/bin/mkswap /dev/zram0\", TAG+=\"systemd\"\n")
            with open('/etc/fstab', 'a') as f:
                f.write("\n/dev/zram0 none swap defaults 0 0\n")
            with open('/etc/sysctl.d/99-swappiness.conf', 'w') as f:
                f.write("vm.swappiness=100\n")
            for i in range(len(packages[zram])):
                os.system(packages["zram"][i])
            break
        elif user_optin["zram"] in no:
            print(f"{Fore.BLUE}==> Skipping zram... {Style.RESET_ALL}")
            break
        else:
            print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")

def add_startup_tweaks():
    while user_optin["otherstartuptweaks"] not in yes_or_no:
        user_optin["otherstartuptweaks"] = input(f"\n{Fore.BLUE}==> Do you want to add a startup script that automatically sets your PC to high performance mode? (don't use on laptops, it kills battery life as a result of increased power consumption) (Y/n) {Style.RESET_ALL}").lower()
        if user_optin["otherstartuptweaks"] in yes:
            print(f"{Fore.BLUE}==> Adding startup script... {Style.RESET_ALL}")    
            with open("/etc/startupscript.sh", "w") as file_startup:
                file_startup.write(startup_script["startup_script"][0])
            with open("/etc/systemd/system/startup-script.service", "w") as file_startup:
                file_startup.write(startup_script["startup_script"][1])
            os.system("systemctl enable --now startup-script.service")
            break
        elif user_optin["otherstartuptweaks"] in no:
            print(f"{Fore.BLUE}==> Skipping startup script... {Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")

def install_vfio_stuff():
    while user_optin["vfio"] not in yes_or_no:
        user_optin["vfio"] = input(f"\n{Fore.BLUE}==> Do you also want to install some VFIO QEMU/KVM stuff? (for people who want to do GPU passthrough VMs) (y/N) {Style.RESET_ALL}").lower()
        if user_optin["vfio"] in nodefault:
            print(f"{Fore.BLUE}==> Skipping VFIO stuff...{Style.RESET_ALL}")
            break
        elif user_optin["vfio"] in yes:
            os.system("pacman -S --needed qemu libvirt edk2-ovmf virt-manager ebtables dnsmasq")
            os.system("systemctl enable --now libvirtd.service virtlogd.socket")
            os.system("virsh net-autostart default")
            os.system("virsh net-start default")
            os.system("wget 'https://raw.githubusercontent.com/PassthroughPOST/VFIO-Tools/master/libvirt_hooks/qemu' -O /etc/libvirt/hooks/qemu")
            os.system("chmod +x /etc/libvirt/hooks/qemu")
            os.system("systemctl restart libvirtd")
            break
        else:
            print(f"{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")

def conclude():
    print(f"\n{Fore.BLUE}==> Concluding... {Style.RESET_ALL}")
    os.system("rm -rf /tmp/arch-post-install-script/")
    print(f"\nThank you for choosing this post-installation script! May your system run marvelously! {Fore.BLUE}sqnx.{Style.RESET_ALL}\nAlso, check out some more of my stuff on GitHub: {Fore.BLUE}https://github.com/xnqs{Style.RESET_ALL}\n")

def main():
    disclaimer()
    if user_info["user"] == "root":
        confirm()
        manjaro_switch_to_unstable()
        install_yay()
        install_other_deps()
        install_chaotic()
        install_desktop_environment()
        add_multilib_repo()
        install_lutris_deps()
        install_lutris_and_other_gaming_tools()
        install_other_software()
        install_amf()
        install_goverlay()
        install_kernel()
        install_pipewire()
        overall_performance_setup()
        enable_zram()
        add_startup_tweaks()
        install_vfio_stuff()
        conclude()
    else:
        user_is_not_root()

# MAIN SCRIPT
main()
