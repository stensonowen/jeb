# jeb.cam

Local pi-based media server


## components

* [srv](/srv): pi flask server that controls omxplayer via dbus
* [site](/site): js frontend with ajax for sending keypresses
* [fwd](/fwd): c utility to forward text to tv tty (must be suid root)
* [torr](/torr): torrent vm rust server that reports and controls vpn status


## why

TODO?

If I'm going to use shitty software I might as well use my own.
But it doesn't sneak in ads or sneak out personal data so I guess this is better.

Also controlling everything instead of using something generic that works slightly better means it's easier to add stuff like controlling my ac or displaying weather or notifications or something.


## setup

Python3, Omxplayer

(Optional) Rust, Virtualbox

```
apt install libdbus-1-3 python3-dbus
```
```
pip3 install flask request dbus-python
```
```
cd fwd
make
sudo make install
```


## addons

* [PIAracy](https://github.com/stensonowen/PIAracy) for a torrent box vm base
* [lirc](http://www.lirc.org/) for ir signals on a pi
* [SimpleProtocolPlayer](https://github.com/kaytat/SimpleProtocolPlayer) to use phone as pulseaudio client
* deluge


## problems
* pi chokes on 4k / high bitrate (TODO eventually replace pi)
* omxplayer (and pi hardware) doesn't support certain codecs (TODO replace pi)
* media files unstructured, e.g. poorly organized, no rating/links (TODO database?)
* filenames are a mess (TODO FileBot? imdb-rename?)
* python is slow,  dbus is dumb, javascript is really dumb (TODO maybe someday RIIR if I can't control myself)


## license

AGPL

