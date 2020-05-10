### Docker commands for Linux Deepin 15.11 (Debian 9.0)

Docker service running:
```shell
# start
sudo service docker start
# stop
sudo service docker stop
# restart
sudo /etc/init.d/docker restart
```

## Unzip something 
> sudo tar -zxvf file.tar.gz

## Mount external folder (from the computer) to the internal system of the virtual machine in VMWare

```shell
cd /mnt
sudo vmhgfs-fuse .host:/ /mnt/hgfs/ -o allow_other -o uid=1000
sudo mkdir /mnt/hgfs
sudo /usr/bin/vmhgfs-fuse .host:/ /mnt/hgfs -o subtype=vmhgfs-fuse,allow_other
cd /mnt/hgfs
```


