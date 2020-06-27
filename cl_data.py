def get_file(file_name: str) -> list:
    """
    Takes a file name (string), reads the file line by line and saves it to a list,
    which it then returns.
    """
    with open(file_name, "r", encoding="utf-8") as my_file:
        return my_file.read().split("\n")


# Dictionary of ship types and sizes, 0 being smallest, 3 being largest
ship_types = {
    "argosy": 1,
    "barque": 3,
    "barquentine": 2,
    "bergantina": 2,
    "bilander": 0,
    "brig": 2,
    "brigantine": 2,
    "carrack": 3,
    "cog": 2,
    "corvette": 0,
    "Dutch clipper": 2,
    "East Indiaman": 2,
    "fluyt": 3,
    "fly-boat": 3,
    "frigate": 2,
    "galleon": 3,
    "gallivat": 0,
    "howker": 0,
    "lorcha": 0,
    "lugger": 0,
    "man o’ war": 3,
    "pinnace": 0,
    "polacre": 0,
    "schooner": 1,
    "ship of the line": 3,
    "xebec": 0,
}

# List of ship weapons, corresponds to the different ship sizes (1, 0, 3, 2)
ship_weapons = [
    "a single cannon",
    "a handful of cannon",
    "a dozen cannon",
    "dozens of cannon",
]

# List of flags
flags = get_file("data/names-flags.txt")

# List of ship names
ship_names = get_file("data/names-ship.txt")

# Lists of things to describe small enemies
enemy_small_verb = [
    "running for their very lives",
    "fleeing as fast as their sails could carry them",
    "making fast for open water",
]
enemy_small_adj = [
    "diminutive",
    "feeble",
    "homuncular",
    "insignificant",
    "laughable",
    "pint-sized",
    "puny",
    "trifling",
    "small",
    "yapping",
]

# Lists of things to describe large enemies
enemy_large_verb = [
    "bearing down on us",
    "coming fast at us",
    "seeming to fly towards us",
]
enemy_large_adj = [
    "awesome," "daunting",
    "fearsome",
    "forbidding",
    "formidable",
    "imposing",
    "intimidating",
    "menacing",
    "threatening",
]

# Lists of things to describe equally-matched enemies
enemy_equal_adj = [
    "approximate",
    "comparable",
    "equivalent",
    "evenly matched",
    "similarly sized",
]

# List of captain names
captain_names = get_file("data/names-captain.txt")

# List of places and longlat coords
place_coords = {
    "Tainan": (22.9912479, 120.1848844),
    "Manila": (14.5906216, 120.9799696),
    "Sulu": (6.0, 121.0),
    "Thanlyin": (16.8221824, 96.3475503338991),
    "Ingeli": (-30.5375789, 29.6856822),
    "Mrauk U": (20.5413409, 93.4351555832934),
    "Lintin Island": (22.41289295, 113.803002666564),
    "Pisang": (0.869444, 103.902222),
    "Balambangan": (1.783333, 119.0),
    "Aden": (12.8331607, 44.9166065),
    "Muscat": (23.5997857, 58.5451305),
    "Esfahan": (32.6707877, 51.6650002),
    "Fort St. David": (40.44569305, -79.9964843223297),
    "Diamond Harbour": (22.1910091, 88.1904741),
    "Hội An": (15.8793816, 108.3273966),
    "Machilipatnam": (16.1819393, 81.1351299),
    "Mew Bay": (-34.04945475, 18.6539583102918),
    "Fort St. George": (13.07946, 80.287794),
    "Rogues River": (43.8883549, 3.5720156),
    "Mana": (45.709097, -68.85902),
    "Thoothukudi": (8.8053535, 78.1452688),
    "Parangipettai": (11.4905673, 79.7568983),
    "Batavia": (48.5740136, 13.4606445),
    "Hirado": (33.3200842, 129.492997),
    "Wang-an": (23.611895, 119.516596),
    "Pulicat": (13.4176606, 80.3166702),
    "Cox’s Island": (49.0946277, -58.0414458),
    "Diu": (20.7161177, 70.9106124),
    "Cape of Good Hope": (-34.3579412, 18.4723393),
    "Nizampatnam": (15.8828715, 80.6390477),
    "Basara": (43.157574, 22.677829),
    "Santiago": (-33.4377967, -70.650445),
    "St Helena": (-15.991955, -5.6999093),
    "Madras": (13.0796914, 80.2829533),
    "Nagapattinam": (10.7647952, 79.8430779),
    "Cochin": (9.9633864, 76.2536614),
    "Tapian Nauli": (1.2347992, 99.041847),
    "North Island": (-38.00353035, 175.957852608357),
    "Madura Island": (-7.0590762, 113.284317389341),
    "Travancore": (-37.7807552, 144.935503),
    "Kharg": (34.8310187, 73.0565386),
    "Pattani": (7.25053155, 101.671549885412),
    "Bandar Abbas": (27.1781213, 56.2766447),
    "Pring": (-20.0394843, 148.092443),
    "Porto Novo": (6.4990718, 2.6253361),
    "Pallippuram": (10.0200245, 76.2251991),
    "Kundapura": (13.6250993, 74.6915722),
    "Mahé": (-4.6803696, 55.4823125),
    "Maio": (15.22721825, -23.1563012971624),
    "Jambi": (-1.6115719, 102.779699),
    "Padang": (-0.9524784, 100.3632419),
    "Rajshahi": (24.3715513, 88.5921038),
    "Samarang": (28.26063545, 84.1332075739494),
    "Anping": (23.000763, 120.16681),
    "Calicut": (11.2446144, 75.7759372),
    "Nagulavancha": (17.0683181, 80.2139976),
    "Tristan de Cunha": (-38.9031887, -11.1750009),
    "Angra Pequeña": (-26.627978, 15.1589946),
    "Condore": (8.6931938, 106.5857637),
    "Daman": (27.60772085, 85.0997014279562),
    "Moco Moco": (-15.4563071, -68.9986653),
    "Lombok": (52.8736, 6.14343),
    "Keelung": (25.1317051, 121.7446489),
    "Sangora": (51.4607104, -0.1739616),
    "Delagoa Bay": (-25.9833332, 32.7),
    "Crooe": (44.4246419, 8.6809288),
    "Palakol": (14.9643271, 120.4802966),
    "Banjarmasin": (-3.3187495, 114.5925828),
    "Point de Galle": (47.1561047, 9.338323),
    "St Augustine’s Bay": (51.44154235, -3.16908492261633),
    "Golkonda": (17.3873294, 78.4057336),
    "Cape Colony": (36.0196055, -76.5816088),
    "Qeshm": (26.7687897, 55.8966628146079),
    "Coringa": (-12.0995479, -45.8709524),
    "Whampoa": (22.304901, 114.1896461),
    "Al Mukha": (13.519984, 43.427981),
    "Visakhapatnam": (17.7231276, 83.3012842),
    "Thǎng Long": (21.0292095, 105.85247),
    "New Anchorage": (40.0015065, -74.1426397),
    "Rio de Janeiro": (-22.9110136, -43.2093726),
    "Nicobar Islands": (8.6531065, 93.0962503),
    "Sadras": (12.5240067, 80.16324),
    "Thiruppapuliyur": (11.747309, 79.7472617),
    "Port Cornwallis": (13.28333, 93.08336),
    "Perates": (39.6453762, 20.7280342),
    "Penang": (5.4065013, 100.2559077),
    "Bushire": (32.897107, -96.8334919),
    "Pondicherry": (10.90253775, 79.9752370356183),
    "Mangalore": (-42.6538941, 147.2415779),
    "Kanpur": (26.5, 80.0),
    "Teneriffe": (-27.455924, 153.0464425),
    "Simon’s Bay": (48.9798012, -84.3382491),
    "Ponnani": (10.7800691, 75.9189338),
    "Rangoon": (16.7967129, 96.1609916),
    "Santa Cruz": (36.9735903, -122.0260569),
    "Ascension Island": (-7.9461394, -14.362056),
    "Chusan": (53.29907905, -6.2073111),
    "Vengurla": (15.8563, 73.6353),
    "Kedah": (5.9682875, 100.6660103),
    "Benguela": (-12.5790047, 13.4037117),
    "Bantal": (-7.8400997, 114.2254808),
    "Surabaya": (-7.2459716, 112.7378266),
    "Burhanpur": (21.3118839, 76.2291992),
    "Bangka Island": (1.7968, 125.153),
    "Calcutta": (22.5677459, 88.3476023),
    "Bengkulu": (-3.5186762, 102.5359834),
    "Matavai": (-15.9630352, -173.7926303),
    "Swally": (21.1693102, 72.6399578),
    "Balasore": (21.5017098, 86.9216712),
    "Mauritius": (-20.275945, 57.5703566),
    "Karwar": (14.8120931, 74.1319229),
    "Saldanha Bay": (-33.0347221, 18.0097222),
    "Nagore": (10.8166979, 79.8403641),
    "Sukadana": (-6.2188784, 106.0375435),
    "Fernando de Noronha": (-3.8561011, -32.4248188),
    "Bengkunat": (-5.5420423, 104.2942256),
    "Rat Island": (43.27588985, -79.9127706334747),
    "Sindh": (25.5, 69.0),
    "Dutch Ceylon": (6.8970619, 79.8593907),
    "Agra": (27.02317485, 78.0925527),
    "Ahmadabad": (23.0216238, 72.5797068),
    "Ipuh": (-3.0040493, 101.4862597),
    "Trincomalee": (8.576425, 81.2344952),
    "Kedgeree": (53.1831757, -0.5890265),
    "Ayutthaya": (14.3560372, 100.5722073),
    "Nakhon Si Thammarat": (8.6772337, 99.7309635),
    "Kodungallur": (10.2239618, 76.1977706),
    "Goa": (15.3004543, 74.0855134),
    "Amoy": (40.8286674, -82.5532266),
    "Diamond Point": (34.287535, -111.1929105),
    "Hong Kong": (22.2793278, 114.1628131),
    "Billiton": (-22.7961053, -69.2614836),
    "Kayamkulam": (9.1666915, 76.5014559),
    "Bankshall": (22.5722401, 88.3469786),
    "Hugli": (22.91028045, 88.012627930889),
    "Cuddalore": (11.74269375, 79.7503064417193),
    "Tranquebar": (11.029929, 79.852196),
    "Timor": (-9.346017, 124.637279937916),
    "Surat": (21.1864607, 72.8081281),
    "Second Bar": (14.6353335, 121.0937034),
    "Fulta": (36.696092, 44.496106),
    "Pulo Bay": (15.0262319, 120.7217614),
    "Kidderpore": (22.53538, 88.3206094),
    "Ganjam": (19.5, 84.5),
    "Tellicherry": (-33.8308765, 151.2247002),
    "Kakinada": (16.9437385, 82.2350607),
    "Anjengo": (8.6627144, 76.7645123),
    "False Bay": (-32.94507115, 137.644840065361),
    "Cape Comorin": (8.0772932, 77.5513761),
    "Bantam": (41.7245409, -73.2362261),
    "Dhaka": (23.7593572, 90.3788136),
    "Onore": (45.891589, 10.010757),
    "San Salvadore": (22.4400324, -101.1482298),
    "St Paul’s Island": (35.96567675, 14.4014271663517),
    "Tamsui": (25.1813044, 121.4531477),
    "Mokha": (21.5477281, 76.7997183),
    "Anjere": (-6.030167, 105.9380976),
    "Porto Praya": (15.245555, -23.6698654),
    "Bombay": (18.9321862, 72.8308337),
    "Car Nicobar": (9.156225, 92.8215167),
    "Cannanore": (11.8762254, 75.3738043),
    "Pariaman": (-5.5480823, 104.8244732),
    "Johanna": (-12.2262432, 44.4106912587226),
    "Deshima": (52.3615878, 4.8860437),
    "Bharuch": (21.7080427, 72.9956936),
    "Ava": (36.951999, -92.6604456),
    "Trinidade": (-23.3516702, -44.7255806),
    "Bandar-e Kong": (50.02294935, 8.52851163887305),
    "Perim": (12.6518053, 43.4277634299776),
    "Acheh": (23.2362, 104.228),
    "Rendezvous Island": (42.3660276, -71.2378746),
    "Malacca": (2.2001524, 102.2507207),
    "Kinsale": (51.705737, -8.5229822),
    "Resolution Bay": (-41.1240937, 174.2236458),
    "Martaban": (15.9090123, 40.1865648806179),
    "Amboina": (12.1549272, -68.2581823),
    "Quilon": (8.8870941, 76.5906837),
    "Tiku": (54.9944056, 82.4427018),
}

# List of place names
place_names = list(place_coords.keys())

# Make a copy of these coords so we can come back to them if we run out
# of locations to visit
canonical_place_coords = place_coords.copy()

# Descriptions of unfavourable winds
wind_bad = get_file("data/wind-bad.txt")

# Descriptions of favourable winds
wind_good = get_file("data/wind-good.txt")

# Negative adjectives applicable to people
personality_bad = get_file("data/personality-bad.txt")

# Positive adjectives applicable to people
personality_good = get_file("data/personality-good.txt")

# Phrases synonymous with 'known for'
known_for = get_file("data/known-for.txt")

# Negative adjectives applicable to objects/things
objects_bad = get_file("data/objects-bad.txt")

# Positive adjectives applicable to objects/things
objects_good = get_file("data/objects-good.txt")

# List of objects
objects = get_file("data/objects.txt")

# List of purchaseable items
items = get_file("data/items.txt")

# List of phrases about running low on provisions
provisions_low = get_file("data/provisions-low.txt")

# List of phrases about running low on rum
rum_low = get_file("data/rum-low.txt")

# List of phrases about naval vicotry
victory = get_file("data/victory.txt")
