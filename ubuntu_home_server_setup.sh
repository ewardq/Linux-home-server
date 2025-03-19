#!/bin/bash
apt update

sudo -i

# Install and configure Samba for NAS  -----------------------------------------------------------------
apt install samba
# Make a shared folder.
mkdir /media/myfiles
# Make main user owner of shared folder.
chown $USER: /media/myfiles
# Create a user and password for shared folder.
smbpasswd -a <user>
# Configure folder location in Samba config file at the end of the file.
echo "path = /media/myfiles
writeable = yes
public = no" > /etc/samba/smb.conf

# Enable and configure Wake on LAN  --------------------------------------------------------------------
# Make sure hardware supports Wake on LAN
ethtool <network_adapter>
# Get network adapter name
ethtool <network_adapter> | grep "Wake-on"
# Enable wake on LAN
ethtool -s <network_adapter> wol g
# Make configuration persistent
chmod u+w /etc/netplan/00-installer-config.yaml
sed -c -i "s/\(wakeonlan *: *\).*/\1true/" /etc/netplan/00-installer-config.yaml

# Files backed up log and notification  ------------------------------------------------------------------
# Create a script to log size, date of modification and number of files
echo "#!/bin/bash" > ~/scripts/record_shared_files.sh
echo "echo \"=======================\" >> /media/shared_folder_backup.log" >> ~/scripts/record_shared_files.sh
echo "ls -lh /media/myfiles/ >> /media/shared_folder_backup.log" >> ~/scripts/record_shared_files.sh
# Change permissions to execute file
sudo chmod +x /scripts/record_shared_files.sh
# Schedule task to execute each day
crontab -l | { cat; echo "*\59 * * * * /scripts/record_shared_files.sh some entry"; } | crontab -

