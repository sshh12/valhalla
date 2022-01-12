#!/bin/bash
# sudo systemctl disable dnsmasq
# sudo systemctl mask dnsmasq
sudo killall dnsmasq
sudo dnsmasq -R -d