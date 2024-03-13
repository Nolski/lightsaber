# Install workarounds for the Displaylink driver on
# the newest version of Fedora (including Rawhide)
# December 7th, 2023

# Download the most recent Displaylink rpm for Fedora (currently 38).

wget https://github.com/displaylink-rpm/displaylink-rpm/releases/download/v5.8.0-1/fedora-39-displaylink-1.14.1-2.x86_64.rpm

#If the driver was already installed but quit working after kernel update, remove it.

sudo dnf remove displaylink


# If you're on a fresh install, you may need these build dependencies.
# There's no harm installing these. Some may already be installed.

sudo dnf groupinstall 'Development Tools'
sudo dnf install gcc-g++
sudo dnf install python-devel
sudo dnf install pybind11-devel
sudo dnf install libdrm-devel

# Built and install the edvi modules.

git clone https://github.com/DisplayLink/evdi
cd evdi
export CPLUS_INCLUDE_PATH="/usr/include/python3.12:$CPLUS_INCLUDE_PATH"
make
sudo make install

reboot

# Install Displaylink driver from previously downloaded rpm

sudo dnf install './fedora-39-displaylink-1.14.1-2.x86_64.rpm'

# At this point you may have locked up, or you may get kicked out of your X session
# and end up at the login screen in which case the driver will have loaded.
# One way or another, reboot the system. You'll probably see a 'dkms didn't start error'.
# Don't worry. It's harmless.
# Save the rpm because you'll need to repeat this for every
# kernel update until an rpm for the most current version of Fedora is built.
