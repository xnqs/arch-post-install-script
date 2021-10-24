# IMPORT NECESSARY LIBRARIES
import os
import getpass
from colorama import init, Fore, Back, Style
init()

# VARIABLES
user = getpass.getuser()
lutrisdeps = "wine-tkg-staging-fsync-git giflib lib32-giflib libpng lib32-libpng libldap lib32-libldap gnutls lib32-gnutls mpg123 lib32-mpg123 openal lib32-openal v4l-utils lib32-v4l-utils libpulse lib32-libpulse libgpg-error lib32-libgpg-error alsa-plugins lib32-alsa-plugins alsa-lib lib32-alsa-lib libjpeg-turbo lib32-libjpeg-turbo sqlite lib32-sqlite libxcomposite lib32-libxcomposite libxinerama lib32-libgcrypt libgcrypt lib32-libxinerama ncurses lib32-ncurses opencl-icd-loader lib32-opencl-icd-loader libxslt lib32-libxslt libva lib32-libva gtk3 lib32-gtk3 gst-plugins-base-libs lib32-gst-plugins-base-libs vulkan-icd-loader lib32-vulkan-icd-loader"
gaming_stuff = "yay lutris steam lib32-gamemode gamemode mangohud obs-streamfx obs-studio-browser retroarch discord_arch_electron"
chaoticaur = """
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist
"""
pulse = "pulseaudio pulseaudio-alsa pulseaudio-bluetooth pulseaudio-jack pulseaudio-zeroconf pulseaudio-equalizer"
pipewire = "pipewire pipewire-alsa pipewire-media-session pipewire-pulse pipewire-jack pipewire-zeroconf"
manjaro_zen = "'https://archive.archlinux.org/packages/l/linux-zen/linux-zen-5.14.14.zen1-1-x86_64.pkg.tar.zst'"
manjaro_zen_headers = "'https://archive.archlinux.org/packages/l/linux-zen-headers/linux-zen-headers-5.14.14.zen1-1-x86_64.pkg.tar.zst'"
manjaro_zen_mirrorlist = """##                                                                              
## Arch Linux repository mirrorlist                                             
## Generated on 2042-01-01                                                      
##
Server=https://archive.archlinux.org/repos/last/$repo/os/$arch"""
startup_script = """#!/bin/bash

# overclock
# zenstates -p 0 -f 98 -d 8 -v 20
cpupower frequency-set -g performance

# disable multi-generational lru, linux-zen runs awfully because of this
echo 0 | tee /sys/kernel/mm/lru_gen/enabled"""

# removes temp dir if already there
notfirstrun = os.path.isdir("/tmp/arch-post-install-script/")
if notfirstrun == True:
    os.system("sudo rm -rf /tmp/arch-post-install-script/")
    os.mkdir("/tmp/arch-post-install-script/")
else:
    os.mkdir("/tmp/arch-post-install-script/")

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
print(f"\n{Fore.BLUE}### Updating repos, might take a while depending on your internet connection...{Style.RESET_ALL}")
os.system("pacman -Syy | grep multilib > /tmp/arch-post-install-script/user_installed_multilib.xnqs")

# check if user already installed mesa-git
os.system("pacman -Q mesa | grep mesa-git > /tmp/arch-post-install-script/mesa-git.xnqs")

# SCRIPT

os.system("clear")
input(f"""{Fore.RED}WARNING: THIS SCRIPT IS EXPERIMENTAL AND STILL BEING DEVELOPED. AS SUCH, IN THIS STATE IT IS EXTREMELY DANGEROUS TO EXECUTE IT AND YOU MAY CAUSE PERMAMENT DAMAGE TO YOUR COMPUTER BY GOING FORWARD WITH THIS. ONLY TEST THIS IN A VM RIGHT NOW AS THIS IS STILL BEING DEVELOPED. BY EXECUTING THIS ON YOUR REAL MACHINE, YOU MAKE YOURSELF RESPONSIBLE FOR ANY AND ALL DAMAGE CAUSED BY THIS SCRIPT.

IF YOU UNDERSTAND THE RISKS AND YOU WANT TO CONTINUE, PRESS ENTER.
OTHERWISE, PRESS CTRL+C.{Style.RESET_ALL}""")
print(f"\nArch Post-Installation Script x.yz - {Fore.BLUE}sqnx.{Style.RESET_ALL}")
print("Hey there! You probably just finished installing Arch, and you want to get straight into the meat and potatoes. I'll install everything you need so you don't have to!")
print("So basically, what this script will do is it will set up your Arch for high-performance gaming, as the default settings are absolutely abysmal for gaming. I will also install some software that is nice to have for gamers, or literally anyone else, such as OBS configured with DMA-BUF capture for games and Discord with enabled OpenH264. It also installs NVFBC if you're on NVIDIA, which does the same thing as obs-vkcapture, but for NVIDIA GPUs. This script also installs Feral Gamemode, which automatically maxes out your CPU frequency when in a game, resulting in significantly better performance (up to 50% increase in some especially demanding titles). Among other things, you also have a choice to install a graphical environment if you haven't already. With that said, let's get right into it!") 
if user == "root":
    print("")
    print(f"You're running this as {Fore.GREEN}" + user + f"{Style.RESET_ALL}, which is exactly what we need in order to continue with the installation process. :D")
    if user_is_on_manjaro == True:
        print(f"\n{Fore.BLUE}### Manjaro detected. Switching to Unstable branch, which is actually more stable...{Style.RESET_ALL}")
        os.system("pacman-mirrors --api --set-branch unstable")
        os.system("pacman-mirrors --fasttrack 5 && pacman -Syyu")
    print(f"\n{Fore.BLUE}### So first, let's start off with the Chaotic AUR!")
    user_optin_chaoticaur = input(f"### Do you wish to add the Chaotic AUR to your repository list? (Highly recommended, makes running this script a lot easier and faster) (Y/n): {Style.RESET_ALL}")
    if user_optin_chaoticaur in ("y", "Y", ""):
        user_optin_chaoticaur = True
        if os.stat("/tmp/arch-post-install-script/chaotic_installed.xnqs").st_size == 0:
            print(f"\n{Fore.BLUE}### Adding Chaotic AUR...{Style.RESET_ALL}")
            os.system("pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com")
            os.system("pacman-key --lsign-key 3056513887B78AEB")
            os.system("pacman -U --noconfirm 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst' 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'")
            file_pacman = open("/etc/pacman.conf", "a")
            file_pacman.write(chaoticaur)
            file_pacman.close()
        else:
            print(f"\n{Fore.BLUE}### Skipping Chaotic AUR because it is already installed...{Style.RESET_ALL}")
    else:
        user_optin_chaoticaur = False
        print(f"\n{Fore.BLUE}### Skipping Chaotic AUR...")
    user_optin_de = input(f"\n{Fore.BLUE}### Do you want to install a desktop environment? (Y/n) {Style.RESET_ALL}")
    if user_optin_de in ("y", "Y", ""):
        print(f"""\n{Fore.BLUE}### Which desktop environment do you want to install?{Style.RESET_ALL}
1. KDE (Default)
2. GNOME
3. Xfce
4. i3wm
5. Nevermind.""")
        user_optin_de_option = input(f"\n{Fore.BLUE}> {Style.RESET_ALL}")
        if user_optin_de_option in ("1", ""):
            os.system("pacman -S --needed plasma papirus-icon-theme adobe-source-sans-fonts materia-kde")
        elif user_optin_de_option == "2":
            os.system("pacman -S --needed gnome papirus-icon-theme adobe-source-sans-fonts materia-gtk-theme")
        elif user_optin_de_option == "3":
            os.system("pacman -S --needed xfce4 papirus-icon-theme adobe-source-sans-fonts materia-gtk-theme")
        elif user_optin_de_option == "4":
            os.system("pacman -S --needed i3 i3blocks adobe-source-sans-fonts otf-font-awesome")
        else:
            print(f"\n{Fore.BLUE}### Skipping Desktop Environment...{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.BLUE}### Skipping Desktop Environment...{Style.RESET_ALL}")
    print(f"\n{Fore.BLUE}### Adding multilib repo for Wine and other gaming tools...{Style.RESET_ALL}")
    if os.stat("/tmp/arch-post-install-script/user_installed_multilib.xnqs").st_size == 0:
        file_multilib = open("/etc/pacman.conf", "a")
        file_multilib.write("""[multilib]
Include = /etc/pacman.d/mirrorlist""")
        file_multilib.close()
    else:
        print(f"\n{Fore.BLUE}### Skipping multilib because it is already installed...{Style.RESET_ALL}")
    print(f"\n{Fore.BLUE}### Installing Lutris Dependencies...{Style.RESET_ALL}")
    os.system("pacman -S --needed --noconfirm base-devel")
    os.system("pacman -S --needed --noconfirm " + lutrisdeps)
    print(f"\n{Fore.BLUE}### Installing Lutris, Steam, and other gaming-related stuff...{Style.RESET_ALL}")
    if user_optin_chaoticaur == True:
        if user_freegpu == True:
            os.system("pacman -S --needed --noconfirm " + gaming_stuff + " obs-vkcapture-git lib32-obs-vkcapture-git")
        else:
            os.system("pacman -S --needed --noconfirm " + gaming_stuff + " obs-nvfbc")
    else:
        os.system("sudo -u \#1000 git clone https://aur.archlinux.org/yay.git /tmp/arch-post-install-script/yay/")
        os.system("cd /tmp/arch-post-install-script/yay/")
        os.system("sudo -u \#1000 makepkg -scif --noconfirm")
        if user_freegpu == True:
            os.system("sudo -u \#1000 yay -S " + gaming_stuff + " obs-vkcapture-git lib32-obs-vkcapture-git")
        else:
            os.system("sudo -u \#1000 yay -S " + gaming_stuff + " obs-nvfbc")
    if user_amdgpu == True:
        if user_optin_chaoticaur == True:
            print(f"\n{Fore.BLUE}### Installing AMF for OBS hardware-accelerated encoding...{Style.RESET_ALL}")
            if os.stat("/tmp/arch-post-install-script/mesa-git.xnqs").st_size == 0:
                os.system("pacman -S --needed --noconfirm vulkan-amdgpu-pro amf-amdgpu-pro vulkan-radeon lib32-vulkan-radeon")
            else:
                os.system("pacman -S --needed --noconfirm vulkan-amdgpu-pro amf-amdgpu-pro")
        else:
            user_optin_amf = input(f"\n{Fore.BLUE}### I see you haven't added Chaotic AUR so this is gonna take a while... Do you actually want to install AMF? (Y/n) {Style.RESET_ALL}")
            if user_optin_amf in ("y", "Y", ""):
                if os.stat("/tmp/arch-post-install-script/mesa-git.xnqs").st_size == 0:
                    print(f"\n{Fore.BLUE}### Installing AMF for OBS hardware-accelerated encoding...{Style.RESET_ALL}")
                    os.system("sudo -u \#1000 yay -S vulkan-amdgpu-pro amf-amdgpu-pro vulkan-radeon lib32-vulkan-radeon")
                else:
                    print(f"\n{Fore.BLUE}### Installing AMF for OBS hardware-accelerated encoding...{Style.RESET_ALL}")
                    os.system("sudo -u \#1000 yay -S vulkan-amdgpu-pro amf-amdgpu-pro")
            else:
                print(f"\n{Fore.BLUE}### Skipping AMF for OBS hardware-accelerated encoding...{Style.RESET_ALL}")
    user_optin_kernel = input(f"\n{Fore.BLUE}### Do you want to install a custom kernel? (If you're on Manjaro, choose N) (Y/n) {Style.RESET_ALL}")
    if user_optin_kernel in ("y", "Y", ""):
        print(f"""\n{Fore.BLUE}### Which custom kernel suits your needs best? (If in doubt, just choose 1.)
{Style.RESET_ALL}1. Linux Zen (default, also my personal favourite)
2. Xanmod (Raw performance-oriented kernel, might behave weirdly at 100% load, needs Chaotic AUR or regular AUR)
3. Linux TKG (might run badly on some hardware as opposed to the Zen kernel, like mine for example, needs Chaotic)
4. Nevermind.""")
        user_optin_kerneloption = input(f"\n{Fore.BLUE}> {Style.RESET_ALL}")
        if user_optin_kerneloption in ("1", ""):
            if user_is_on_manjaro == True:
                print(f"\n{Fore.BLUE}### User is on Manjaro, which doesn't have Zen in its repos, so installing latest Zen kernel from the Arch Linux Archive. Update this every now and then.{Style.RESET_ALL}")
                os.system("cat /etc/pacman.d/mirrorlist > /tmp/arch-post-install-script/mirrorlist.xnqs")
                file_manjaro_mirrorlist = open("/etc/pacman.d/mirrorlist", "w")
                file_manjaro_mirrorlist.write(manjaro_zen_mirrorlist)
                file_manjaro_mirrorlist.close()
                os.system("pacman -Syy linux-zen linux-zen-headers")
                os.system("cat /tmp/arch-post-install-script/mirrorlist.xnqs > /etc/pacman.d/mirrorlist")
                os.system("pacman -Syy")
            else:
                os.system("pacman -S --noconfirm linux-zen linux-zen-headers")
        elif user_optin_kerneloption == "2":
            if user_optin_chaoticaur == True:
                os.system("pacman -S --noconfirm linux-xanmod-cacule linux-xanmod-cacule-headers")
            else:
                user_optin_kernelsure = input(f"\n{Fore.BLUE}### Are you sure you want to install a custom kernel from the AUR? This will take up to hours, depending on your hardware. (Y/n) {Style.RESET_ALL}")
                if user_option_kernelsure in ("y", "Y", ""):
                    os.system("sudo -u \#1000 yay -S linux-xanmod-cacule linux-xanmod-cacule-headers")
                else:
                    print(f"\n{Fore.BLUE}### Skipping Custom Kernel... {Style.RESET_ALL}")
        elif user_optin_kerneloption == "3":
            if user_optin_chaoticaur == True:
                os.system("pacman -S --noconfirm linux-tkg-pds linux-tkg-pds-headers")
            else:     
                print(f"\n{Fore.BLUE}### Skipping Custom Kernel because it's only available in the Chaotic AUR... {Style.RESET_ALL}")
        else:
            print(f"\n{Fore.BLUE}### Skipping Custom Kernel... {Style.RESET_ALL}")
    else:
        print(f"\n{Fore.BLUE}### Skipping Custom Kernel... {Style.RESET_ALL}")
    user_optin_pipewire = input(f"\n{Fore.BLUE}### Do you want to replace legacy PulseAudio with Pipewire (a newer and better low latency audio server)? (Y/n) {Style.RESET_ALL}")
    if user_optin_pipewire in ("y", "Y", ""):
        print(f"\n{Fore.BLUE}### Installing Pipewire... {Style.RESET_ALL}")
        os.system("pacman -Rdd " + pulse)
        os.system("pacman -S " + pipewire)
        os.system("killall -s SIGKILL pulseaudio")
        os.system("sudo -U \#1000 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus XDG_RUNTIME_DIR=/run/user/1000 systemctl --user enable --now pipewire pipewire-pulse pipewire-media-session")
    else:
        print(f"\n{Fore.BLUE}### Leaving PulseAudio as it is... {Style.RESET_ALL}")
    user_optin_performance = input(f"\n{Fore.BLUE}### Do you want to install some performance tweaks while you're at it? (Needs Chaotic AUR) (Y/n) {Style.RESET_ALL}")
    if user_optin_performance in ("y", "Y", ""):
        if user_optin_chaoticaur == True:
            os.system("pacman -S --noconfirm performance-tweaks")
        else:
            print(f"\n{Fore.BLUE}### Chaotic AUR not added, so skipping Garuda Performance Tweaks...{Style.RESET_ALL}")
        if user_amdgpu == True:
            user_optin_mesagit = input(f"\n{Fore.BLUE}### Install Experimental Mesa? (typically gives a performance boost compared to Mesa, especially on RX 6000 series) (Y/n) {Style.RESET_ALL}")
            if user_optin_mesagit in ("y", "Y", ""):
                if os.stat("/tmp/arch-post-install-script/mesa-git.xnqs").st_size == 0:
                    print(f"\n{Fore.BLUE}### Installing Experimental Mesa... {Style.RESET_ALL}")
                    if user_optin_chaoticaur == True:
                        os.system("pacman -S --noconfirm mesa-git lib32-mesa-git")
                    else:
                        os.system("sudo -u \#1000 yay -S mesa-git lib32-mesa-git")
                else:
                    print(f"\n{Fore.BLUE}### mesa-git package already installed. Skipping... {Style.RESET_ALL}")
            else:
                print(f"\n{Fore.BLUE}### Skipping Experimental Mesa... {Style.RESET_ALL}")
        print(f"\n{Fore.BLUE}### Enabling FSync in bashrc for Wine games to run better... {Style.RESET_ALL}")
        file_bashrc = open("/etc/bash.bashrc", "a")
        file_bashrc.write("export WINEFSYNC=1")
        file_bashrc.close()
        if user_amdcpu == True:
            print(f"\n{Fore.BLUE}### Installing Zenstates for Ryzen Overclocking... {Style.RESET_ALL}")
            os.system("sudo -u \#1000 yay -S --noconfirm zenstates-git")
        else:
            print(f"\n{Fore.BLUE}### Skipping Zenstates for Ryzen Overclocking since user is not on Ryzen CPU... {Style.RESET_ALL}")
    else:
        print(f"\n{Fore.BLUE}### Skipping performance tweaks... {Style.RESET_ALL}")
    user_optin_otherstartuptweaks = input(f"\n{Fore.BLUE}### Do you want to add a startup script that automatically sets your PC to high performance mode? (Y/n) {Style.RESET_ALL}")
    if user_optin_otherstartuptweaks in ("y", "Y", ""):
        print(f"\n{Fore.BLUE}### Adding startup script... {Style.RESET_ALL}")    
        file_startup = open("/etc/startupscript.sh", "w")
        file_startup.write(startup_script)
        file_startup.close()
    else:
        print(f"\n{Fore.BLUE}### Skipping startup script... {Style.RESET_ALL}")
    user_optin_vfio = input(f"\n{Fore.BLUE}### Do you also want to install some VFIO QEMU/KVM stuff? (for people who want to do GPU passthrough VMs) (y/N) {Style.RESET_ALL}")
    if user_optin_vfio in ("y", "Y", ""):
        os.system("pacman -S --needed qemu libvirt edk2-ovmf virt-manager ebtables dnsmasq")
        os.system("systemctl enable --now libvirtd.service virtlogd.socket")
        os.system("virsh net-autostart default")
        os.system("virsh net-start default")
        os.system("wget 'https://raw.githubusercontent.com/PassthroughPOST/VFIO-Tools/master/libvirt_hooks/qemu' -O /etc/libvirt/hooks/qemu")
        os.system("chmod +x /etc/libvirt/hooks/qemu")
        os.system("systemctl restart libvirtd")
    else:
        print(f"\n{Fore.BLUE}### Skipping VFIO stuff...{Style.RESET_ALL}")
    print(f"\n{Fore.BLUE}### Concluding... {Style.RESET_ALL}")
    os.system("rm -rf /tmp/arch-post-install-script/")
    print(f"""\nThank you for choosing this post-installation script! May your system run marvelously! {Fore.BLUE}sqnx.{Style.RESET_ALL}
Also, check out some more of my stuff on GitHub: https://github.com/thepoke32""")
else:    
    print("")
    print(f"You're running this as {Fore.RED}" + user + f"""{Style.RESET_ALL}, so this installation script will cease to work.
Please run this script as {Fore.GREEN}root{Style.RESET_ALL}, either by adding {Fore.GREEN}sudo{Style.RESET_ALL} before the installation script, or by simply running it while logged into the {Fore.GREEN}root{Style.RESET_ALL} account.\n""")
