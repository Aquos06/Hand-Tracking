import numpy as np
import statistics as stat
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()


class Volume(object):
    def inilization(self, hand_coordinate):
        self.coordinatey = []
        for coordinate in hand_coordinate:
            self.coordinatey.append(coordinate[2])
                
        # print("statdev :" , stat.stdev(self.coordinatey))
        # print("mean : ",stat.mean(self.coordinatey))
        return stat.stdev(self.coordinatey), stat.mean(self.coordinatey)
        
    def setVolume (self, standardeviation, mean):
        if standardeviation <= 20:
            #highest : 203, lowest = 371
            #after round up : (highest = 200, lowest : 310)
            mean = 380 - mean
            computer_volume = np.interp(mean,[0,180],[volRange[0],volRange[1]]) 
            volume.SetMasterVolumeLevel(computer_volume, None)
        else :
            return
        