
def geocoding_from_location(location, delay=0.05):
    # lat, long are in parentheses at end of string
    coords = location.rpartition('(')[2].partition(')')[0]

    def post_process_coord(coord):
        coord = coord.strip()
        coord = float(coord)
        return coord

    latitude, longitude = map(post_process_coord, coords.split(','))
    return latitude, longitude
