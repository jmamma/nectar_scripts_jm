sudo killall tar
wait 1
sudo umount /mnt/vdd/compromised_vms/e2bf97cc-b34f-4f1d-b15a-eb3c347d7e75/ephemeral
wait 1
sudo umount /mnt/vdd/compromised_vms/e2bf97cc-b34f-4f1d-b15a-eb3c347d7e75/root
wait 1
sudo killall qemu-nbd
sudo rm /mnt/vdd/compromised_vms/e2bf97cc-b34f-4f1d-b15a-eb3c347d7e75/root.tar.gz 

