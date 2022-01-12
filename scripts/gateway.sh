#!/bin/sh
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD ACCEPT
sudo iptables -P OUTPUT ACCEPT
sudo iptables -t nat -F
sudo iptables -t mangle -F
sudo iptables -F
sudo iptables -X

sudo iptables -t nat -N REDSOCKS
sudo iptables -t nat -F REDSOCKS

sudo iptables -t nat -A REDSOCKS -d 0.0.0.0/8 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 10.0.0.0/8 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 100.64.0.0/10 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 127.0.0.0/8 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 169.254.0.0/16 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 172.16.0.0/12 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 192.168.0.0/16 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 198.18.0.0/15 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 224.0.0.0/4 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 240.0.0.0/4 -j RETURN

sudo iptables -t nat -A REDSOCKS -p tcp -j REDIRECT --to-ports 12345

sudo iptables -t nat -A OUTPUT -p tcp -j REDSOCKS

sudo iptables -t nat -A PREROUTING -p tcp -s 10.0.0.50 -j REDSOCKS
sudo iptables -t nat -A PREROUTING -p tcp -s 10.0.0.51 -j REDSOCKS
sudo iptables -t nat -A PREROUTING -p tcp -s 10.0.0.52 -j REDSOCKS
sudo iptables -t nat -A PREROUTING -p tcp -s 10.0.0.53 -j REDSOCKS
sudo iptables -t nat -A PREROUTING -p tcp -s 10.0.0.54 -j REDSOCKS
sudo iptables -t nat -A PREROUTING -p tcp -s 10.0.0.55 -j REDSOCKS

sudo /usr/bin/glider -listen redir://:12345 -forward socks5://127.0.0.1:4080 -dns=:53 -dnsserver=8.8.8.8:53 -verbose
