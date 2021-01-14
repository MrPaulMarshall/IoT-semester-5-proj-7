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
        """Initialize configuration
        """
        self.cloud = None
        self.citiesComponents = []
        self.districtsComponents = []
        self.connectionsSet = set()
        self.nodeIdxDict = dict()
        self.edgeIdxDict = dict()
        self.devices = dict()
        self.cameras = set()
        self.taskChance = 1

    def add_connection(self, idx1: int, idx2: int):
        """Add connection between devices representet by idx1 and idx2\n
        Parameters: idx1 (int): First node\n
        idx2 (int): Second node\n
        Returns False if connection already exist otherwise returns edge_id 

        """
        # Szudzik's function
        edge_id = self.get_edge_id(idx1, idx2)
        if edge_id in self.connectionsSet:
            return False
        else:
            self.connectionsSet.add(edge_id)
            return edge_id

    def add_node_to_idx(self, deviceId: int, idx: int):
        """Adds node to idx deictionary\n
        Parameters: deviceId (int) Id of the device\n
        idx (int) idx of the node"""
        self.nodeIdxDict[deviceId] = idx

    def add_edge_to_idx(self, edgeId: int, idx: int):
        """Adds edge to idx deictionary\n
        Parameters: edgeId (int) Id of the edge\n
        idx (int) idx of the edge"""
        self.edgeIdxDict[edgeId] = idx

    def get_node_idx(self, deviceId: int):
        """Parameters: deviceId (int)\n
        Returns (int) idx of the node"""
        # return self.nodeIdxDict[deviceId]
        return self.nodeIdxDict.get(deviceId)

    def get_edge_idx(self, edgeId: int):
        """Parameters: edgeId (int)\n
        Returns (int) idx of the edge"""
        # return self.edgeIdxDict[edgeId]
        return self.edgeIdxDict.get(edgeId)

    def get_edge_id(self, idx1: int, idx2: int):
        """Returns id of the edge
        Parameters: idx1 (int) idx of the first node\n
        idx1 (int) idx of the second node\n
        Returns (int) id of the edge"""
        if idx1 >= idx2:
            v = idx1 * idx1 + idx2
        else:
            v = idx1 + idx2 * idx2
        return v
