# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 21:16:04 2016

@author: enoble
"""

import io


def get_file(file_name):
    """Takes a file name (string), reads the file line by line and saves it to a list, which it then returns."""

    with io.open(file_name, 'r', encoding='utf-8') as my_file:
        return my_file.read().split('\n')


# Dictionary of ship types and sizes, 0 being smallest, 3 being largest
ship_types = {
    'argosy': 1,
    'barque': 3,
    'barquentine': 2,
    'bergantina': 2,
    'bilander': 0,
    'brig': 2,
    'brigantine': 2,
    'carrack': 3,
    'cog': 2,
    'corvette': 0,
    'Dutch clipper': 2,
    'East Indiaman': 2,
    'fluyt': 3,
    'fly-boat': 3,
    'frigate': 2,
    'galleon': 3,
    'gallivat': 0,
    'howker': 0,
    'lorcha': 0,
    'lugger': 0,
    'man o‘ war': 3,
    'pinnace': 0,
    'polacre': 0,
    'schooner': 1,
    'ship of the line': 3,
    'xebec': 0
}

# List of ship weapons, corresponds to the different ship sizes (0, 1, 2, 3)
ship_weapons = ['a single cannon', 'a handful of cannon', 'a dozen cannon', 'dozens of cannon']

# List of flags
flags = get_file('data/names-flags.txt')

# List of ship names
ship_names = get_file('data/names-ship.txt')
    
# Lists of things to describe small enemies
enemy_small_verb = ['running for their lives', 'fleeing as fast as their sails could carry them']
enemy_small_adj = ['puny', 'trifling', 'small', 'yapping', 'laughable', 'insignificant']

# Lists of things to describe large enemies
enemy_large_verb = ['bearing down on us', 'coming fast at us', 'seeming to fly towards us']
enemy_large_adj = ['formidable', 'imposing', 'fearsome', 'threatening']

# Lists of things to describe equally-matched enemies
enemy_equal_adj = ['evenly matched', 'comparable', 'similarly sized']

# List of captain names
captain_names = get_file('data/names-captain.txt')

# List of place names
place_names = get_file('data/names-places.txt')

# List of places and longlat coords
place_coords = {
    'Tainan': (120.1848844, 22.9912479),
    'Manila': (120.9799696, 14.5906216),
    'Sulu': (121.0, 6.0),
    'Thanlyin': (96.3475503338991, 16.8221824),
    'Ingeli': (29.6856822, -30.5375789),
    'Mrauk U': (93.4351555832934, 20.5413409),
    'Lintin Island': (113.803002666564, 22.41289295),
    'Pisang': (103.902222, 0.869444),
    'Balambangan': (119.0, 1.783333),
    'Aden': (44.9166065, 12.8331607),
    'Muscat': (58.5451305, 23.5997857),
    'Esfahan': (51.6650002, 32.6707877),
    'Fort St. David': (-79.9964843223297, 40.44569305),
    'Diamond Harbour': (88.1904741, 22.1910091),
    'Hội An': (108.3273966, 15.8793816),
    'Machilipatnam': (81.1351299, 16.1819393),
    'Mew Bay': (18.6539583102918, -34.04945475),
    'Fort St. George': (80.287794, 13.07946),
    'Rogues River': (3.5720156, 43.8883549),
    'Mana': (-68.85902, 45.709097),
    'Thoothukudi': (78.1452688, 8.8053535),
    'Parangipettai': (79.7568983, 11.4905673),
    'Batavia': (13.4606445, 48.5740136),
    'Hirado': (129.492997, 33.3200842),
    'Wang-an': (119.516596, 23.611895),
    'Pulicat': (80.3166702, 13.4176606),
    'Cox’s Island': (-58.0414458, 49.0946277),
    'Diu': (70.9106124, 20.7161177),
    'Cape of Good Hope': (18.4723393, -34.3579412),
    'Nizampatnam': (80.6390477, 15.8828715),
    'Basara': (22.677829, 43.157574),
    'Santiago': (-70.650445, -33.4377967),
    'St Helena': (-5.6999093, -15.991955),
    'Madras': (80.2829533, 13.0796914),
    'Nagapattinam': (79.8430779, 10.7647952),
    'Cochin': (76.2536614, 9.9633864),
    'Tapian Nauli': (99.041847, 1.2347992),
    'North Island': (175.957852608357, -38.00353035),
    'Madura Island': (113.284317389341, -7.0590762),
    'Travancore': (144.935503, -37.7807552),
    'Kharg': (73.0565386, 34.8310187),
    'Pattani': (101.671549885412, 7.25053155),
    'Bandar Abbas': (56.2766447, 27.1781213),
    'Pring': (148.092443, -20.0394843),
    'Porto Novo': (2.6253361, 6.4990718),
    'Pallippuram': (76.2251991, 10.0200245),
    'Kundapura': (74.6915722, 13.6250993),
    'Mahé': (55.4823125, -4.6803696),
    'Maio': (-23.1563012971624, 15.22721825),
    'Jambi': (102.779699, -1.6115719),
    'Padang': (100.3632419, -0.9524784),
    'Rajshahi': (88.5921038, 24.3715513),
    'Samarang': (84.1332075739494, 28.26063545),
    'Anping': (120.16681, 23.000763),
    'Calicut': (75.7759372, 11.2446144),
    'Nagulavancha': (80.2139976, 17.0683181),
    'Tristan de Cunha': (-11.1750009, -38.9031887),
    'Angra Pequeña': (15.1589946, -26.627978),
    'Condore': (106.5857637, 8.6931938),
    'Daman': (85.0997014279562, 27.60772085),
    'Moco Moco': (-68.9986653, -15.4563071),
    'Lombok': (6.14343, 52.8736),
    'Keelung': (121.7446489, 25.1317051),
    'Sangora': (-0.1739616, 51.4607104),
    'Delagoa Bay': (32.7, -25.9833332),
    'Crooe': (8.6809288, 44.4246419),
    'Palakol': (120.4802966, 14.9643271),
    'Banjarmasin': (114.5925828, -3.3187495),
    'Point de Galle': (9.338323, 47.1561047),
    'St Augustine’s Bay': (-3.16908492261633, 51.44154235),
    'Golkonda': (78.4057336, 17.3873294),
    'Cape Colony': (-76.5816088, 36.0196055),
    'Qeshm': (55.8966628146079, 26.7687897),
    'Coringa': (-45.8709524, -12.0995479),
    'Whampoa': (114.1896461, 22.304901),
    'Al Mukha': (43.427981, 13.519984),
    'Visakhapatnam': (83.3012842, 17.7231276),
    'Thǎng Long': (105.85247, 21.0292095),
    'New Anchorage': (-74.1426397, 40.0015065),
    'Rio de Janeiro': (-43.2093726, -22.9110136),
    'Nicobar Islands': (93.0962503, 8.6531065),
    'Sadras': (80.16324, 12.5240067),
    'Thiruppapuliyur': (79.7472617, 11.747309),
    'Port Cornwallis': (93.08336, 13.28333),
    'Perates': (20.7280342, 39.6453762),
    'Penang': (100.2559077, 5.4065013),
    'Bushire': (-96.8334919, 32.897107),
    'Pondicherry': (79.9752370356183, 10.90253775),
    'Mangalore': (147.2415779, -42.6538941),
    'Kanpur': (80.0, 26.5),
    'Teneriffe': (153.0464425, -27.455924),
    'Simon’s Bay': (-84.3382491, 48.9798012),
    'Ponnani': (75.9189338, 10.7800691),
    'Rangoon': (96.1609916, 16.7967129),
    'Santa Cruz': (-122.0260569, 36.9735903),
    'Ascension Island': (-14.362056, -7.9461394),
    'Chusan': (-6.2073111, 53.29907905),
    'Vengurla': (73.6353, 15.8563),
    'Kedah': (100.6660103, 5.9682875),
    'Benguela': (13.4037117, -12.5790047),
    'Bantal': (114.2254808, -7.8400997),
    'Surabaya': (112.7378266, -7.2459716),
    'Burhanpur': (76.2291992, 21.3118839),
    'Bangka Island': (125.153, 1.7968),
    'Calcutta': (88.3476023, 22.5677459),
    'Bengkulu': (102.5359834, -3.5186762),
    'Matavai': (-173.7926303, -15.9630352),
    'Swally': (72.6399578, 21.1693102),
    'Balasore': (86.9216712, 21.5017098),
    'Mauritius': (57.5703566, -20.275945),
    'Karwar': (74.1319229, 14.8120931),
    'Saldanha Bay': (18.0097222, -33.0347221),
    'Nagore': (79.8403641, 10.8166979),
    'Sukadana': (106.0375435, -6.2188784),
    'Fernando de Noronha': (-32.4248188, -3.8561011),
    'Bengkunat': (104.2942256, -5.5420423),
    'Rat Island': (-79.9127706334747, 43.27588985),
    'Sindh': (69.0, 25.5),
    'Dutch Ceylon': (79.8593907, 6.8970619),
    'Agra': (78.0925527, 27.02317485),
    'Ahmadabad': (72.5797068, 23.0216238),
    'Ipuh': (101.4862597, -3.0040493),
    'Trincomalee': (81.2344952, 8.576425),
    'Kedgeree': (-0.5890265, 53.1831757),
    'Ayutthaya': (100.5722073, 14.3560372),
    'Nakhon Si Thammarat': (99.7309635, 8.6772337),
    'Kodungallur': (76.1977706, 10.2239618),
    'Goa': (74.0855134, 15.3004543),
    'Amoy': (-82.5532266, 40.8286674),
    'Diamond Point': (-111.1929105, 34.287535),
    'Hong Kong': (114.1628131, 22.2793278),
    'Billiton': (-69.2614836, -22.7961053),
    'Kayamkulam': (76.5014559, 9.1666915),
    'Bankshall': (88.3469786, 22.5722401),
    'Hugli': (88.012627930889, 22.91028045),
    'Cuddalore': (79.7503064417193, 11.74269375),
    'Tranquebar': (79.852196, 11.029929),
    'Timor': (124.637279937916, -9.346017),
    'Surat': (72.8081281, 21.1864607),
    'Second Bar': (121.0937034, 14.6353335),
    'Fulta': (44.496106, 36.696092),
    'Pulo Bay': (120.7217614, 15.0262319),
    'Kidderpore': (88.3206094, 22.53538),
    'Ganjam': (84.5, 19.5),
    'Tellicherry': (151.2247002, -33.8308765),
    'Kakinada': (82.2350607, 16.9437385),
    'Anjengo': (76.7645123, 8.6627144),
    'False Bay': (137.644840065361, -32.94507115),
    'Cape Comorin': (77.5513761, 8.0772932),
    'Bantam': (-73.2362261, 41.7245409),
    'Dhaka': (90.3788136, 23.7593572),
    'Onore': (10.010757, 45.891589),
    'San Salvadore': (-101.1482298, 22.4400324),
    'St Paul’s Island': (14.4014271663517, 35.96567675),
    'Tamsui': (121.4531477, 25.1813044),
    'Mokha': (76.7997183, 21.5477281),
    'Anjere': (105.9380976, -6.030167),
    'Porto Praya': (-23.6698654, 15.245555),
    'Bombay': (72.8308337, 18.9321862),
    'Car Nicobar': (92.8215167, 9.156225),
    'Cannanore': (75.3738043, 11.8762254),
    'Pariaman': (104.8244732, -5.5480823),
    'Johanna': (44.4106912587226, -12.2262432),
    'Deshima': (4.8860437, 52.3615878),
    'Bharuch': (72.9956936, 21.7080427),
    'Ava': (-92.6604456, 36.951999),
    'Trinidade': (-44.7255806, -23.3516702),
    'Bandar-e Kong': (8.52851163887305, 50.02294935),
    'Perim': (43.4277634299776, 12.6518053),
    'Acheh': (104.228, 23.2362),
    'Rendezvous Island': (-71.2378746, 42.3660276),
    'Malacca': (102.2507207, 2.2001524),
    'Kinsale': (-8.5229822, 51.705737),
    'Resolution Bay': (174.2236458, -41.1240937),
    'Martaban': (40.1865648806179, 15.9090123),
    'Amboina': (-68.2581823, 12.1549272),
    'Quilon': (76.5906837, 8.8870941),
    'Tiku': (82.4427018, 54.9944056)
}

# Make a copy of these coords so we can come back to them if we run out
# of locations to visit
canonical_place_coords = place_coords.copy()

# Descriptions of unfavourable winds
wind_bad = get_file('data/wind-bad.txt')

# Descriptions of favourable winds
wind_good = get_file('data/wind-good.txt')

# Negative adjectives applicable to people
personality_bad = get_file('data/personality-bad.txt')

# Positive adjectives applicable to people
personality_good = get_file('data/personality-good.txt')

# Phrases synonymous with 'known for'
known_for = get_file('data/known-for.txt')

# Negative adjectives applicable to objects/things
objects_bad = get_file('data/objects-bad.txt')

# Positive adjectives applicable to objects/things
objects_good = get_file('data/objects-good.txt')

# List of objects
objects = get_file('data/objects.txt')

# List of purchaseable items
items = get_file('data/items.txt')

# List of phrases about running low on provisions
provisions_low = get_file('data/provisions-low.txt')

# List of phrases about running low on rum
rum_low = get_file('data/rum-low.txt')

# List of phrases about naval vicotry
victory = get_file('data/victory.txt')
