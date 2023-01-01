 #!/bin/sh
 # auth-user-pass login.conf
 
 # update system time for crypto
 sudo date -s "$(wget --method=HEAD -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f4-10)"
 
 # run vpn
 sudo openvpn --config us9436.nordvpn.com.tcp443.ovpn --tls-exit --socks-proxy 127.0.0.1 4080
 
