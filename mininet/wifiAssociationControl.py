from mininet.wifiPropagationModels import propagationModel
from mininet.wifiChannel import setChannelParams

class associationControl (object):

    changeAP = False

    def __init__(self, sta, ap, wlan, ac):
        self.customAssociationControl(sta, ap, wlan, ac)

    def customAssociationControl(self, sta, ap, wlan, ac):
        """Mechanisms that optimize the use of the APs
        llf: Least-loaded-first
        ssf: Strongest-signal-first"""
        if ac == "llf":
            apref = sta.params['associatedTo'][wlan]
            if apref != 'NoAssociated':
                ref_llf = len(apref.params['associatedStations'])
                if len(ap.params['associatedStations']) + 2 < ref_llf:
                    self.changeAP = True
            else:
                self.changeAP = True
        elif ac == "ssf":
            refDistance = setChannelParams.getDistance(sta, ap)
            refValue = propagationModel(sta, ap, refDistance, wlan)
            if refValue.rssi > float(sta.params['rssi'][wlan] + 1):
                self.changeAP = True
        return self.changeAP
