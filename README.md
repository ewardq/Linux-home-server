# Ubuntu home server 🐧
This physical Ubuntu home server covers my family’s data backup needs in a local private network using Syncthing and custom Bash scripts for system monitoring, and network security policies configuration.

- Sharing of local network files with Samba (Windows <--> Ubuntu <--> Fedora).
- Reverse proxy setup for Syncthing using Nginx.
- Virtual Private Network set up using WireGuard.
- Server ”Wake on LAN” from main computer and smartphone.
- Automated backups using Timeshift and server file logging using Cron jobs.


## Setup

### \#1. SSH access from home network
- [x] Home server should be accessible from the main computer.
```bash
ssh <user>@<ip>
```
<details>
<summary><i>Click here to see result screenshot</i></summary>
  
![image](https://github.com/user-attachments/assets/3c4c4520-d841-4c45-bfcc-ef068463f432)
</details>
<!-- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->

---

### \#2. Install Samba
- [x] Install Samba.
`sudo apt install samba`

- [x] Make a shared folder.
`sudo mkdir /media/myfiles`

- [x] Make main user owner of shared folder.
`sudo chown $USER: /media/myfiles`

- [x] Create a user and password for shared folder.
`sudo smbpasswd -a <user>`

- [x] Configure folder location in Samba config file at the end of the file.
`sudo nano /etc/samba/smb.conf`
  - ![Image](https://github.com/user-attachments/assets/ac71b842-df74-4ae7-927c-44ee83c71076)

- [x] Add shared folder on Windows
  - <details>
    <summary><i>Click here to see result screenshot</i></summary>
  
    ![Image](https://github.com/user-attachments/assets/b5e4c3ba-0d39-4053-b698-c1731e4935a9)
    </details>

- [x] Shared files ready to use!

<!-- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->

---

### \#3. Network files backup
- [x] Selected files should be sent automatically to central hard drive each week.
  - <details>
    <summary><i>Click here to see result screenshot</i></summary>
  
    ![Image](https://github.com/user-attachments/assets/848d8fff-ab2f-4cd1-b68e-c8b7c171a7a6)
    </details>

![Image](https://github.com/user-attachments/assets/236793ed-6d3d-489a-b751-fc18dbf16180)

- [x] Selected files should be sent to central hard drive when prompted.
  - <details>
    <summary><i>Click here to see result screenshot</i></summary>
  
    ![Image](https://github.com/user-attachments/assets/13209c54-7bef-4d44-a64b-867fe91521f1)
    </details>

<!-- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->

---

### \#4. Wake on LAN
- [x] Network adapter supports Wake-on-LAN 
```bash
sudo ethtool <network_adapter>
```
  - <details>
    <summary><i>Click here to see result screenshot</i></summary>
  
    ![image](https://github.com/user-attachments/assets/0c91aed1-2800-43ea-bc56-442592c9a3d0)
    where: 
      - g = Wake on LAN is enabled for Magic packets.
      - p = Wake on LAN is enabled for unicast packets.
    </details>


- [x] Enable Wake-on-LAN
```bash
sudo ethtool <network_adapter> | grep "Wake-on"
sudo ethtool -s <network_adapter> wol g
```
  - <details>
    <summary><i>Click here to see result screenshot</i></summary>
  
    ![Image](https://github.com/ewardq/Linux-home-server-automated-backup-and-monitoring/assets/72580785/bffb5653-5231-4250-a21b-345e7246d5f2)
    where: 
      - d = Disabled.
      - g  = Wake on LAN is enabled for unicast packets.
    </details>


- [x] Make configuration persistent. For Ubuntu, we have to configure the network adapter on the "netplan" folder:
```bash
sudo chmod u+w /etc/netplan/00-installer-config.yaml
nano /etc/netplan/00-installer-config.yaml
```
  - <details>
    <summary><i>Click here to see result screenshot</i></summary>
  
    ![Image](https://github.com/ewardq/Linux-home-server-automated-backup-and-monitoring/assets/72580785/d96ec6b3-659f-49d9-ad26-afda1087725a)
    </details>
<!-- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->

---

### \#5. Network monitoring
- [x] The user should be able to see which devices are connected to the network.

  - To monitor the local network, you can use the built-in internet service provider tool. To access this tool, search in the back of your home router and search for the modem IP, user and password.
![Image](https://github.com/user-attachments/assets/5e51ba13-852e-401b-b461-e280840dd73f)

  - To monitor the local network on Windows, install `WakeMeOnLan`.
    - <details>
      <summary><i>Click here to see result screenshot</i></summary>
  
      ![Image](https://github.com/user-attachments/assets/37f6b6d5-66fb-4390-83b7-cdd8945f22a7)
      </details>

  - To monitor the local network on the server side (Ubuntu), use `ip addr` to discover the server's network adapter
    - <details>
      <summary><i>Click here to see result screenshot</i></summary>
  
      ![Image](https://github.com/user-attachments/assets/799ee7a6-6dac-4280-9b13-6c6899846503)
      </details>

  - `npmap <ip>/<mask>`
    - <details>
      <summary><i>Click here to see result screenshot</i></summary>
  
      ![Image](https://github.com/user-attachments/assets/9a5f48f0-6091-417b-b192-700175c41a25)
      </details>

- [x] The user should be able to blacklist selected users.
  - Use the network provider built-in tool.
    - <details>
      <summary><i>Click here to see result screenshot</i></summary>
  
      ![Image](https://github.com/user-attachments/assets/54ba8cf0-2fcf-4dc5-b486-76c0e86e41f8)
      </details>
<!-- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->

---

### \#6. Files backed up log and notification
- [x] System should keep track of files backed up.
  - [5.1] Create a script to log size, date of modification and number of files
  - ```bash
    #!/bin/bash
    echo "=======================" >> /media/shared_folder_backup.log
    ls -lh /media/myfiles/ >> /media/shared_folder_backup.log
    ```


  - [5.2] Change permissions to execute file
  - ```bash
    sudo chmod +x /custom_scripts/record_shared_files.sh
    ```

  - [5.3] Schedule task to execute each day
     1. Verify if the user has a crontab
    ```bash
     crontab -l
    ```
     ![Image](https://github.com/user-attachments/assets/05755d18-a1a0-4155-9779-b263e238d8bf)

     2. Create or edit said user crontab
    ```bash
     crontab -e
    ```
    ![Image](https://github.com/user-attachments/assets/3f4a0773-f4e9-46e8-a058-6aa20dcaa58b)

     3. Schedule task to execute every hour
    ```bash
     crontab -e
    ```
      - <details>
        <summary><i>Click here to see result screenshot</i></summary>
  
        ![Image](https://github.com/user-attachments/assets/f0008c71-a74d-4c3e-807c-1827638e348f)
        </details>
    

<details>
<summary><i>Click Here to see the result on the log file</i></summary>
  
![Image](https://github.com/user-attachments/assets/0f581032-54f2-4626-9343-8a354810ef5b)
</details>
<!-- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -->

---

### \#7. Automated backup every day
- [x] Files should be backed up every day without user input.
  - To back up files daily, configure "Recovery" settings.
    - <details>
      <summary><i>Click Here to see result screenshot</i></summary>
  
      ![image](https://github.com/user-attachments/assets/2bdc2599-bf07-434d-ab54-7ee4787dd3ba)
      </details>
