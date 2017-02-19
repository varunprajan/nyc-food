
def geocoding_from_location(location, delay=0.05):
    # lat, long are in parentheses at end of string
    coords = location.rpartition('(')[2].partition(')')

    def post_process_coord(coord):
        coord = coord.strip()
        coord = int(coord)
        return coord

    latitude, longitude = coords.split(',').map(post_process_coord)
    return latitude, longitude
