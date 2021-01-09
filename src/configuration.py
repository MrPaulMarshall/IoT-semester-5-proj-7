# Konfiguracja calej topologii.
# districtsComponents - lista spojnych skladowych wezlow dzielnicowych
#   (pojedynczy element jest lista dzielnic nalezacych do spojnej skladowej)
#   (oznacza to, ze districtsComponents jest lista list districtNode)
#
# citiesComponents - analogicznie - lista spojnych skladowych wezlow miejskich
#   (pojedynczy element jest lista miast nalezacych do spojnej skladowej)
#   (oznacza to, ze citiesComponents jest lista list cityNode)
#       (pojedynycz cityNode zawiera districtsComponents, co odpowiada dzielnicom nalezacym do danego miasta)
#
# powyzsze elementy moga stanowic calosc topologii bez istnienia chmury (nie sa poloczone z chmura)
#
# cloud - analogicznie do konfiguracji posiada citiesComponents oraz districtsComponents
# jesli urzadzenie jest umieszczone w drzewie chmury to oznacza, ze ma polaczenie z chmura
# przeciwnie do urzadzen wpisanych bezposrednio w konfiguracji)
#
# connectionSet - zbior identyfikatorow krawedzi
# krawedz jest jednoznacznie okreslona przez INDEKSY wezlow (a nie identyfikatory urzadzen)
#
# nodeIdxDict - mapa identyfikatorow urzaden w indeksy wezlow
# edgeIdxDict - mapa identyfikatorow krawedzi w ich indeksy
#
# devices - mapa identyfikatorow urzadzen w obiekty je posiadajace
# (pole jest redundantne ale ulatwia dostep do danego urzadzenia)


class Configuration:
    def __init__(self):
        self.cloud = None
        self.citiesComponents = []
        self.districtsComponents = []
        self.connectionsSet = set()
        self.nodeIdxDict = dict()
        self.edgeIdxDict = dict()
        self.devices = dict()

    def add_connection(self, idx1: int, idx2: int) -> bool:
        # Szudzik's function
        v = self.get_edge_id(idx1, idx2)
        if v in self.connectionsSet:
            return False
        else:
            self.connectionsSet.add(v)
            return True

    def add_node_to_idx(self, deviceId: int, idx: int):
        self.nodeIdxDict[deviceId] = idx

    def add_edge_to_idx(self, edgeId: int, idx: int):
        self.edgeIdxDict[edgeId] = idx

    def get_node_idx(self, deviceId: int):
        return self.nodeIdxDict[deviceId]

    def get_edge_idx(self, edgeId: int):
        return self.edgeIdxDict[edgeId]

    def get_edge_id(self, idx1: int, idx2: int):
        if idx1 >= idx2:
            v = idx1 * idx1 + idx2
        else:
            v = idx1 + idx2 * idx2
        return v
