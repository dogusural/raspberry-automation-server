## Remote Development
### SCP to Raspberry

```$rsync -av -e 'ssh -p 6931' --exclude='.git/' --exclude='*.md*' ../raspberry-automation-server  pi@10.0.0.24:/home/pi```