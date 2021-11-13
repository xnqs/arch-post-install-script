#!/usr/bin/env python3

# IMPORT NECESSARY LIBRARIES
import os
import getpass
import re
import math
from colorama import init, Fore, Back, Style
init()

# VARIABLES
user = getpass.getuser() 
yes = ("y", "")
no = ("n")
nodefault = ("n", "")
yes2 = ("y")
yes_or_no = ("y", "", "n")
lutrisdeps = ("wine-tkg-staging-fsync-git giflib lib32-giflib libpng lib32-libpng libldap lib32-libldap gnutls lib32-gnutls mpg123 lib32-mpg123 openal lib32-openal v4l-utils lib32-v4l-utils libpulse lib32-libpulse libgpg-error lib32-libgpg-error alsa-plugins lib32-alsa-plugins alsa-lib lib32-alsa-lib libjpeg-turbo lib32-libjpeg-turbo sqlite lib32-sqlite libxcomposite lib32-libxcomposite libxinerama lib32-libgcrypt libgcrypt lib32-libxinerama ncurses lib32-ncurses opencl-icd-loader lib32-opencl-icd-loader libxslt lib32-libxslt libva lib32-libva gtk3 lib32-gtk3 gst-plugins-base-libs lib32-gst-plugins-base-libs vulkan-icd-loader lib32-vulkan-icd-loader", "wine-staging giflib lib32-giflib libpng lib32-libpng libldap lib32-libldap gnutls lib32-gnutls mpg123 lib32-mpg123 openal lib32-openal v4l-utils lib32-v4l-utils libpulse lib32-libpulse libgpg-error lib32-libgpg-error alsa-plugins lib32-alsa-plugins alsa-lib lib32-alsa-lib libjpeg-turbo lib32-libjpeg-turbo sqlite lib32-sqlite libxcomposite lib32-libxcomposite libxinerama lib32-libgcrypt libgcrypt lib32-libxinerama ncurses lib32-ncurses opencl-icd-loader lib32-opencl-icd-loader libxslt lib32-libxslt libva lib32-libva gtk3 lib32-gtk3 gst-plugins-base-libs lib32-gst-plugins-base-libs vulkan-icd-loader lib32-vulkan-icd-loader")
gaming_stuff = "yay neovim cpupower lutris vkd3d lib32-vkd3d steam proton-ge-custom heroic-games-launcher-bin lib32-gamemode gamemode mangohud obs-streamfx obs-studio-browser retroarch discord_arch_electron"
chaoticaur = "\n[chaotic-aur]\nInclude = /etc/pacman.d/chaotic-mirrorlist\n"
software = "chromium vlc spotify qbittorrent yuzu kdenlive olive noisetorch grapejuice-git"
pulse = (
        "pulseaudio",
        "pulseaudio-alsa",
        "pulseaudio-bluetooth",
        "pulseaudio-jack",
        "pulseaudio-zeroconf",
        "pulseaudio-equalizer"
        )
pipewire = "pipewire pipewire-alsa pipewire-media-session pipewire-pulse pipewire-jack pipewire-zeroconf"
manjaro_zen_mirrorlist = "Server=https://archive.archlinux.org/repos/last/$repo/os/$arch"
startup_script = ("#!/bin/bash\n# overclock\n# zenstates -p 0 -f 98 -d 8 -v 20\ncpupower frequency-set -g performance\n\n# disable multi-generational lru, linux-zen runs awfully because of this\necho 0 | tee /sys/kernel/mm/lru_gen/enabled", "[Unit]\nAfter=hibernate.target\nAfter=hybrid-sleep.target\nAfter=suspend.target\nAfter=suspend-then-hibernate.target\nDescription=Startup Script\n\n[Service]\nExecStart=/etc/startupscript.sh\n\n[Install]\nWantedBy=multi-user.target\nWantedBy=hibernate.target\nWantedBy=hybrid-sleep.target\nWantedBy=suspend.target\nWantedBy=suspend-then-hibernate.target")
original_pwd = os.popen("pwd").read().strip()

# removes temp dir if already there
notfirstrun = os.path.isdir("/tmp/arch-post-install-script/")
if notfirstrun == True:
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
user_id = os.popen("id -u " + other_user).read().strip()

# check if user is on AMD GPU
os.system('lspci | grep VGA | grep AMD > /tmp/arch-post-install-script/gpu.xnqs') 
user_amdgpu = bool(os.stat("/tmp/arch-post-install-script/gpu.xnqs").st_size)

# check if user is on free GPU
os.system('lspci | grep VGA | grep Intel >> /tmp/arch-post-install-script/gpu.xnqs')
os.system('lspci | grep VGA | grep QXL >> /tmp/arch-post-install-script/gpu.xnqs')
user_freegpu = bool(os.stat("/tmp/arch-post-install-script/gpu.xnqs").st_size)

# check if user is on Ryzen CPU
os.system("cat /proc/cpuinfo | grep Ryzen > /tmp/arch-post-install-script/cpu.xnqs")
user_amdcpu = bool(os.stat("/tmp/arch-post-install-script/cpu.xnqs").st_size)

# check if user is on Manjaro
os.system("cat /etc/lsb-release | grep Manjaro > /tmp/arch-post-install-script/distro.xnqs")
user_is_on_manjaro = bool(os.stat("/tmp/arch-post-install-script/distro.xnqs").st_size)

# check if user already installed chaotic
os.system("cat /etc/pacman.conf | grep chaotic > /tmp/arch-post-install-script/chaotic_installed.xnqs")

# check if user already installed multilib
print(f"\n{Fore.BLUE}==> Updating repos, might take a while depending on your internet connection...{Style.RESET_ALL}")
os.system("pacman -Syy | grep multilib > /tmp/arch-post-install-script/user_installed_multilib.xnqs")

# check if user already installed mesa-git
os.system("pacman -Q mesa | grep mesa-git > /tmp/arch-post-install-script/mesa-git.xnqs")

# declare user_optin_x variables for while loop to work
user_optin_chaoticaur = "bleh"
user_optin_de = "bleh"
user_optin_software = "bleh"
user_optin_amf = "bleh"
user_optin_kernel = "bleh"
user_optin_kernelsure = "bleh"
user_optin_pipewire = "bleh"
user_optin_performance = "bleh"
user_optin_mesagit = "bleh"
user_optin_zram = "bleh"
user_optin_otherstartuptweaks = "bleh"
user_optin_vfio = "bleh"
user_optin_de_option = "bleh"
user_optin_kerneloption = "bleh"

# SCRIPT

os.system("clear")
input(f"""{Fore.BLUE}Disclaimer: This script is still being tested, and you might encounter some weird or out of place behaviour, such as some prompts not registering properly, or incompatibility with some Arch-based distros. If you do so, please report it on GitHub so I can fix it.\nJust don't close the script in the middle of execution, and you'll be fine. You can, however, safely Ctrl+C it at a Yes or No prompt.\n\nIf you understand the risks, press Enter. Otherwise, press Ctrl+C.{Style.RESET_ALL}""")
print(f"\nArch Post-Installation Script b0.90 - {Fore.BLUE}sqnx.{Style.RESET_ALL}")
print("\nHey there! You probably just finished installing Arch, and you want to get straight into the meat and potatoes. I'll install everything you need so you don't have to!")
print("So basically, what this script will do is it will set up your Arch for high-performance gaming, as the default settings are absolutely abysmal for gaming. I will also install some software that is nice to have for gamers, or literally anyone else, such as OBS configured with DMA-BUF capture for games and Discord with enabled OpenH264. It also installs NVFBC if you're on NVIDIA, which does the same thing as obs-vkcapture, but for NVIDIA GPUs. This script also installs Feral Gamemode, which automatically maxes out your CPU frequency when in a game, resulting in significantly better performance (up to 50% increase in some especially demanding titles). Among other things, you also have a choice to install a graphical environment if you haven't already. With that said, let's get right into it!") 
if user == "root":
    input("\nPress enter to continue.")
    print("")
    print(f"You're running this as {Fore.GREEN}" + user + f"{Style.RESET_ALL}, which is exactly what we need in order to continue with the installation process. :D")
    if user_is_on_manjaro == True:
        print(f"\n{Fore.BLUE}==> Manjaro detected. Switching to Unstable branch, which is actually more stable...{Style.RESET_ALL}")
        os.system("pacman-mirrors --api --set-branch unstable")
        os.system("pacman-mirrors --fasttrack 5 && pacman -Syyu")
    print(f"\n{Fore.BLUE}==> So first, let's start off with the Chaotic AUR!")
    while user_optin_chaoticaur not in yes_or_no:
        user_optin_chaoticaur = input(f"\n{Fore.BLUE}==> Do you wish to add the Chaotic AUR to your repository list? (Highly recommended, makes running this script a lot easier and faster) (Y/n): {Style.RESET_ALL}").lower()
        if user_optin_chaoticaur in yes:
            user_optin_chaoticaur = True
            if os.stat("/tmp/arch-post-install-script/chaotic_installed.xnqs").st_size == 0:
                print(f"\n{Fore.BLUE}==> Adding Chaotic AUR...{Style.RESET_ALL}")
                os.system("pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com")
                os.system("pacman-key --lsign-key 3056513887B78AEB")
                os.system("pacman -U --noconfirm 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst' 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'")
                file_pacman = open("/etc/pacman.conf", "a")
                file_pacman.write(chaoticaur)
                file_pacman.close()
                os.system("pacman -Syy")
            else:
                print(f"\n{Fore.BLUE}==> Skipping Chaotic AUR because it is already installed...{Style.RESET_ALL}")
            break
        elif user_optin_chaoticaur in no:
            user_optin_chaoticaur = False
            print(f"\n{Fore.BLUE}==> Skipping Chaotic AUR... {Style.RESET_ALL}")
            break
        else:
            print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
    while user_optin_de not in yes_or_no:
        user_optin_de = input(f"\n{Fore.BLUE}==> Do you want to install a desktop environment? (Y/n) {Style.RESET_ALL}").lower()
        if user_optin_de in yes:
            while user_optin_de_option not in ("1", "", "2", "3", "4", "5"):
                print(f"\n{Fore.BLUE}==> Which desktop environment do you want to install?{Style.RESET_ALL}\n1. KDE (Default)\n2. GNOME\n3. Xfce\n4. i3wm\n5. Nevermind.")
                user_optin_de_option = input(f"\n{Fore.BLUE}> {Style.RESET_ALL}")
                if user_optin_de_option in ("1", ""):
                    os.system("pacman -S --needed plasma papirus-icon-theme adobe-source-sans-fonts materia-kde")
                    break
                elif user_optin_de_option == "2":
                    os.system("pacman -S --needed gnome papirus-icon-theme adobe-source-sans-fonts materia-gtk-theme")
                    break
                elif user_optin_de_option == "3":
                    os.system("pacman -S --needed xfce4 papirus-icon-theme adobe-source-sans-fonts materia-gtk-theme")
                    break
                elif user_optin_de_option == "4":
                    os.system("pacman -S --needed i3 i3blocks adobe-source-sans-fonts otf-font-awesome")
                    break
                elif user_optin_de_option == "5":
                    print(f"\n{Fore.BLUE}==> Skipping Desktop Environment...{Style.RESET_ALL}")
                    break
                else:
                    print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
            break
        elif user_optin_de in no:
            print(f"\n{Fore.BLUE}==> Skipping Desktop Environment...{Style.RESET_ALL}")
            break
        else:
            print(f"\n{Fore.BLUE}==> Invalid choice.{Style.RESET_ALL}")
    print(f"\n{Fore.BLUE}==> Adding multilib repo for Wine and other gaming tools...{Style.RESET_ALL}")
    if os.stat("/tmp/arch-post-install-script/user_installed_multilib.xnqs").st_size == 0:
        file_multilib = open("/etc/pacman.conf", "a")
        file_multilib.write("""[multilib]
Include = /etc/pacman.d/mirrorlist""")
        file_multilib.close()
    else:
        print(f"\n{Fore.BLUE}==> Skipping multilib because it is already installed...{Style.RESET_ALL}")
    print(f"\n{Fore.BLUE}==> Installing Lutris Dependencies...{Style.RESET_ALL}")
    os.system("pacman -S --needed --noconfirm base-devel")
    if user_optin_chaoticaur == True:
        os.system("pacman -S --needed --noconfirm " + lutrisdeps[0])
    else:
        os.system("pacman -S --needed --noconfirm " + lutrisdeps[1])
    print(f"\n{Fore.BLUE}==> Installing Lutris, Steam, and other gaming-related stuff...{Style.RESET_ALL}")
    if user_optin_chaoticaur == True:
        if user_freegpu == True:
            os.system("pacman -S --needed --noconfirm " + gaming_stuff + " corectrl obs-vkcapture-git lib32-obs-vkcapture-git")
        else:
            os.system("pacman -S --needed --noconfirm " + gaming_stuff + " gwe obs-nvfbc")
    else:
        os.system("sudo -u " + str(other_user) + " git clone https://aur.archlinux.org/yay.git /tmp/yay/")
        os.chdir("/tmp/yay/")
        os.system("sudo -u " + str(other_user) + " makepkg -scif")
        os.chdir(original_pwd)
        if user_freegpu == True:
            os.system("sudo -u " + str(other_user) + " yay -S " + gaming_stuff + " corectrl obs-vkcapture-git lib32-obs-vkcapture-git")
        else:
            os.system("sudo -u " + str(other_user) + " yay -S " + gaming_stuff + " gwe obs-nvfbc")
    while user_optin_software not in yes_or_no:
        user_optin_software = input(f"\n{Fore.BLUE}==> Do you want to install some extra software? (e.g Spotify, QBitTorrent, VLC, Olive, Kdenlive, Yuzu (switch emulator), etc. (Y/n): {Style.RESET_ALL}").lower()
        if user_optin_software in yes:
            print(f"{Fore.BLUE}==> Installing extra software... {Style.RESET_ALL}")
            os.system("sudo -u " + str(other_user) + " yay -S " + software)
            break
        elif user_optin_software in no:
            print(f"{Fore.BLUE}==> Skipping extra software... {Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
    if user_amdgpu == True:
        if user_optin_chaoticaur == True:
            print(f"\n{Fore.BLUE}==> Installing AMF for OBS hardware-accelerated encoding...{Style.RESET_ALL}")
            if os.stat("/tmp/arch-post-install-script/mesa-git.xnqs").st_size == 0:
                os.system("pacman -S --needed --noconfirm vulkan-amdgpu-pro amf-amdgpu-pro vulkan-radeon lib32-vulkan-radeon")
            else:
                os.system("pacman -S --needed --noconfirm vulkan-amdgpu-pro amf-amdgpu-pro")
        else:
            while user_optin_amf not in yes_or_no:
                user_optin_amf = input(f"\n{Fore.BLUE}==> I see you haven't added Chaotic AUR so this is gonna take a while... Do you actually want to install AMF? (Y/n) {Style.RESET_ALL}").lower()
                if user_optin_amf in yes:
                    if os.stat("/tmp/arch-post-install-script/mesa-git.xnqs").st_size == 0:
                        print(f"\n{Fore.BLUE}==> Installing AMF for OBS hardware-accelerated encoding...{Style.RESET_ALL}")
                        os.system("sudo -u " + str(other_user) + " yay -S vulkan-amdgpu-pro amf-amdgpu-pro vulkan-radeon lib32-vulkan-radeon")
                    else:
                        print(f"\n{Fore.BLUE}==> Installing AMF for OBS hardware-accelerated encoding...{Style.RESET_ALL}")
                        os.system("sudo -u " + str(other_user) + " yay -S vulkan-amdgpu-pro amf-amdgpu-pro")
                    break
                elif user_optin_amf in no:
                    print(f"\n{Fore.BLUE}==> Skipping AMF for OBS hardware-accelerated encoding...{Style.RESET_ALL}")
                    break
                else:
                    print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
    while user_optin_kernel not in yes_or_no:
        user_optin_kernel = input(f"\n{Fore.BLUE}==> Do you want to install a custom kernel? (Y/n) {Style.RESET_ALL}").lower()
        if user_optin_kernel in yes:
            while user_optin_kerneloption not in ("1", "", "2", "3", "4", "5"):
                print(f"\n{Fore.BLUE}==> Which custom kernel suits your needs best? (If in doubt, just choose 1.)\n{Style.RESET_ALL}1. Zen Kernel (default, also my personal favourite)\n2. Clear Kernel (Intel's performance-oriented kernel, might perform really well on Zen 3 or newer Intel chips)\n3. Xanmod (Raw performance-oriented kernel, might behave weirdly at 100% load, needs Chaotic AUR or regular AUR)\n4. Linux TKG (mileage may vary on some hardware as opposed to the Zen kernel, like mine for example, needs Chaotic)\n5. Custom kernel specified by user\n6. Nevermind.")
                user_optin_kerneloption = input(f"\n{Fore.BLUE}> {Style.RESET_ALL}")
                if user_optin_kerneloption in ("1", ""):
                    if user_is_on_manjaro == True:
                        print(f"\n{Fore.BLUE}==> User is on Manjaro, which doesn't have Zen in its repos, so installing latest Zen kernel from the Arch Linux Archive. Update this every now and then.{Style.RESET_ALL}")
                        os.system("cat /etc/pacman.d/mirrorlist > /tmp/arch-post-install-script/mirrorlist.xnqs")
                        file_manjaro_mirrorlist = open("/etc/pacman.d/mirrorlist", "w")
                        file_manjaro_mirrorlist.write(manjaro_zen_mirrorlist)
                        file_manjaro_mirrorlist.close()
                        os.system("pacman -Syy linux-zen linux-zen-headers")
                        os.system("cat /tmp/arch-post-install-script/mirrorlist.xnqs > /etc/pacman.d/mirrorlist")
                        os.system("pacman -Syy")
                    else:
                        os.system("pacman -S --noconfirm linux-zen linux-zen-headers")
                    break
                elif user_optin_kerneloption == "2":
                    while user_optin_kernelsure not in yes_or_no:
                        user_optin_kernelsure = input(f"\n{Fore.BLUE}==> Are you sure you want to install a custom kernel from the AUR? This will take from a couple of minutes, up to a few hours, depending on your hardware. (Y/n) {Style.RESET_ALL}").lower()
                        if user_optin_kernelsure in yes:
                            os.system("sudo -u " + str(other_user) + " yay -S --editmenu linux-xanmod-cacule linux-xanmod-cacule-headers")
                            break
                        elif user_optin_kernelsure in no:
                            print(f"\n{Fore.BLUE}==> Skipping Custom Kernel... {Style.RESET_ALL}")
                            break
                        else:
                            print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
                    break
                elif user_optin_kerneloption == "3":
                    if user_optin_chaoticaur == True:
                        os.system("pacman -S --noconfirm linux-xanmod-cacule linux-xanmod-cacule-headers")
                    else:
                        while user_optin_kernelsure not in yes_or_no:
                            user_optin_kernelsure = input(f"\n{Fore.BLUE}==> Are you sure you want to install a custom kernel from the AUR? This will take from a couple of minutes, up to a few hours, depending on your hardware. (Y/n) {Style.RESET_ALL}").lower()
                            if user_optin_kernelsure in yes:
                                os.system("sudo -u " + str(other_user) + " yay -S --editmenu linux-xanmod-cacule linux-xanmod-cacule-headers")
                                break
                            elif user_optin_kernelsure in no:
                                print(f"\n{Fore.BLUE}==> Skipping Custom Kernel... {Style.RESET_ALL}")
                                break
                            else:
                                print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
                    break
                elif user_optin_kerneloption == "4":
                    if user_optin_chaoticaur == True:
                        os.system("pacman -S --noconfirm linux-tkg-pds linux-tkg-pds-headers")
                    else:     
                        print(f"\n{Fore.BLUE}==> Skipping Selected Custom Kernel because it's only available in the Chaotic AUR... {Style.RESET_ALL}")
                    break
                elif user_optin_kerneloption == "5":
                    user_optin_customkerneloption = input(f"\nType custom kernel package name below. (e.g linux-zen-git installs linux-zen-git and linux-zen-git-headers):\n{Fore.BLUE}> {Style.RESET_ALL}").lower()
                    os.system("sudo -u " + str(other_user) + " yay -S --editmenu" + user_optin_customkerneloption + " " + user_optin_customkerneloption + "-headers")
                    break
                elif user_optin_kerneloption == "6":
                    print(f"\n{Fore.BLUE}==> Skipping Custom Kernel... {Style.RESET_ALL}")
                    break
                else:
                    print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
            break
        elif user_optin_kernel in no:
            print(f"\n{Fore.BLUE}==> Skipping Custom Kernel... {Style.RESET_ALL}")
            break
        else:
            print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
    while user_optin_pipewire not in yes_or_no:
        user_optin_pipewire = input(f"\n{Fore.BLUE}==> Do you want to replace legacy PulseAudio with Pipewire (a newer and better low latency audio server)? (Y/n) {Style.RESET_ALL}").lower()
        if user_optin_pipewire in yes:
            print(f"\n{Fore.BLUE}==> Installing Pipewire... {Style.RESET_ALL}")
            for i in range(6):
                os.system("pacman -Rdd " + pulse[i])
            os.system("pacman -S " + pipewire)
            os.system("killall -s SIGKILL pulseaudio")
            os.system("sudo -u " + other_user + " DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/" + str(user_id) + "/bus XDG_RUNTIME_DIR=/run/user/" + str(user_id) + " systemctl --user enable --now pipewire pipewire-pulse pipewire-media-session")
            break
        elif user_optin_pipewire in no:
            print(f"\n{Fore.BLUE}==> Leaving PulseAudio as it is... {Style.RESET_ALL}")
            break
        else:
            print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
    while user_optin_performance not in yes_or_no:
        user_optin_performance = input(f"\n{Fore.BLUE}==> Do you want to install some performance tweaks while you're at it? (Y/n) {Style.RESET_ALL}").lower()
        if user_optin_performance in yes:
            if user_optin_chaoticaur == True:
                os.system("pacman -S performance-tweaks")
            else:
                print(f"\n{Fore.BLUE}==> Chaotic AUR not added, so skipping Garuda Performance Tweaks...{Style.RESET_ALL}")
            if user_amdgpu == True:
                while user_optin_mesagit not in yes_or_no:
                    user_optin_mesagit = input(f"\n{Fore.BLUE}==> Install Experimental Mesa? (typically gives a performance boost compared to Mesa, especially on RX 6000 series) (Y/n) {Style.RESET_ALL}").lower()
                    if user_optin_mesagit in yes:
                        if os.stat("/tmp/arch-post-install-script/mesa-git.xnqs").st_size == 0:
                            print(f"\n{Fore.BLUE}==> Installing Experimental Mesa... {Style.RESET_ALL}")
                            if user_optin_chaoticaur == True:
                                os.system("pacman -S --noconfirm mesa-git lib32-mesa-git")
                            else:
                                os.system("sudo -u " + str(other_user) + " yay -S mesa-git lib32-mesa-git")
                            break
                        else:
                            print(f"\n{Fore.BLUE}==> mesa-git package already installed. Skipping... {Style.RESET_ALL}")
                            break
                    elif user_optin_mesagit in no:
                        print(f"\n{Fore.BLUE}==> Skipping Experimental Mesa... {Style.RESET_ALL}")
                        break
                    else:
                        print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
            print(f"\n{Fore.BLUE}==> Enabling FSync in bashrc for Wine games to run better... {Style.RESET_ALL}")
            file_bashrc = open("/etc/bash.bashrc", "a")
            file_bashrc.write("\nexport WINEESYNC=1\nexport WINEFSYNC=1")
            file_bashrc.close()
            if user_amdcpu == True:
                print(f"\n{Fore.BLUE}==> Installing Zenstates for Ryzen Overclocking... {Style.RESET_ALL}")
                os.system("sudo -u " + str(other_user) + " yay -S --noconfirm zenstates-git")
            else:
                print(f"\n{Fore.BLUE}==> Skipping Experimental Mesa... {Style.RESET_ALL}")
        elif user_optin_performance in no:
            print(f"\n{Fore.BLUE}==> Skipping performance tweaks... {Style.RESET_ALL}")
            break
        else:
            print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
    while user_optin_zram not in yes_or_no:
        user_optin_zram = input(f"\n{Fore.BLUE}==> Do you want to add RAM compression (zram, really good for users with low ram or using SSDs)? (Y/n) {Style.RESET_ALL}").lower()
        if user_optin_zram in yes:
            print(f"\n{Fore.BLUE}==> Setting up zram... {Style.RESET_ALL}")
            with open('/proc/meminfo') as f:
                meminfo = f.read()
            matched = re.search(r'^MemTotal:\s+(\d+)', meminfo)
            if matched: 
                mem_total_gB = math.floor(int(matched.groups()[0])/1024/1024)
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
            os.system("swapon /dev/zram0")
            break
        elif user_optin_zram in no:
            print(f"\n{Fore.BLUE}==> Skipping zram... {Style.RESET_ALL}")
            break
        else:
            print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
    while user_optin_otherstartuptweaks not in yes_or_no:
        user_optin_otherstartuptweaks = input(f"\n{Fore.BLUE}==> Do you want to add a startup script that automatically sets your PC to high performance mode? (don't use on laptops, it kills battery life as a result of increased power consumption) (Y/n) {Style.RESET_ALL}").lower()
        if user_optin_otherstartuptweaks in yes:
            print(f"\n{Fore.BLUE}==> Adding startup script... {Style.RESET_ALL}")    
            file_startup = open("/etc/startupscript.sh", "w")
            file_startup.write(startup_script[0])
            file_startup.close()
            file_startup = open("/etc/systemd/system/startup-script.service", "w")
            file_startup.write(startup_script[1])
            file_startup.close()
            os.system("systemctl enable --now startup-script.service")
            break
        elif user_optin_otherstartuptweaks in no:
            print(f"\n{Fore.BLUE}==> Skipping startup script... {Style.RESET_ALL}")
            break
        else:
            print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
    while user_optin_vfio not in yes_or_no:
        user_optin_vfio = input(f"\n{Fore.BLUE}==> Do you also want to install some VFIO QEMU/KVM stuff? (for people who want to do GPU passthrough VMs) (y/N) {Style.RESET_ALL}").lower()
        if user_optin_vfio in nodefault:
            print(f"\n{Fore.BLUE}==> Skipping VFIO stuff...{Style.RESET_ALL}")
            break
        elif user_optin_vfio in yes2:
            os.system("pacman -S --needed qemu libvirt edk2-ovmf virt-manager ebtables dnsmasq")
            os.system("systemctl enable --now libvirtd.service virtlogd.socket")
            os.system("virsh net-autostart default")
            os.system("virsh net-start default")
            os.system("wget 'https://raw.githubusercontent.com/PassthroughPOST/VFIO-Tools/master/libvirt_hooks/qemu' -O /etc/libvirt/hooks/qemu")
            os.system("chmod +x /etc/libvirt/hooks/qemu")
            os.system("systemctl restart libvirtd")
            break
        else:
            print(f"\n{Fore.BLUE}==> Invalid option.{Style.RESET_ALL}")
    print(f"\n{Fore.BLUE}==> Concluding... {Style.RESET_ALL}")
    os.system("rm -rf /tmp/arch-post-install-script/")
    print(f"""\nThank you for choosing this post-installation script! May your system run marvelously! {Fore.BLUE}sqnx.{Style.RESET_ALL}
Also, check out some more of my stuff on GitHub: {Fore.BLUE}https://github.com/xnqs{Style.RESET_ALL}\n""")
else:    
    print("")
    print(f"You're running this as {Fore.RED}" + user + f"""{Style.RESET_ALL}, so this installation script will cease to work.
Please run this script as {Fore.GREEN}root{Style.RESET_ALL}, either by adding {Fore.GREEN}sudo{Style.RESET_ALL} before the installation script, or by simply running it while logged into the {Fore.GREEN}root{Style.RESET_ALL} account.\n""")
