# Dependencies
* Python 3.6+
* Tautulli

# Script Setup
Edit `rtorrent_throttle.py` and set rTorrent username, password and RPC2 url.  

# Tautulli Setup
**Commum Scripts Settings in Tautulli:**   
Taultulli > Settings > Notification Agents > Add a Notification Agent > Script  
**Set** `Script Folder`  
**Select** `rtorrent_throttle.py`  
**Script Timeout** `0`  

### Throttle only on wan connections
**Notification conditions**:
- **Condition {1}**: Stream Local is 0
- **Condition {2}**: Action is play
- **Condition {3}**: Streams is 0

**Condition logic**: `{1} and {2} or {3}`

###  Throttle Download/Upload Speed
**Triggers:** 
- Playback Start
- Playback Stop

**Arguments:**
Set Download/Upload limit in KB/s. Set `-1` for unlimited
- Playback Start:  `-D 1024 -U 1024`
- Playback Stop:  `-D -1 -U -1`

###  Verify this setting is enabled
`Settings -> Notifications & Newsletters -> (Show Advanced) Allow Playback Stop Notifications Exceeding Watched Percent.`


# Usage
    -U		- Set max upload speed [KBs], use "-1" to set unlimited
    -D		- Set max download speed [KBs], use "-1" to set unlimited
    -h | --help	- Help

# Credits
https://gist.github.com/Generator/67da7dc859634046165320ef061769e0
https://gist.github.com/Tinynja/2169be3f20b8656f67dbc89129d57598
