import math
from itertools import product
import json


def distance_miles(lat1, long1, lat2, long2):

    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc * 3960

def main():
    of = open('code_lat_lon.txt', 'w')
    code_lat_lon = []
    for line in open('airports.dat'):
        line = line.replace(', ', '/ ')
        aid, name, city, country, code, fcode, lat, lon, alt, tz, dst, tzdt = line.split(',')
        code = code.strip('"')
        if len(code) != 3:
            continue
        code_lat_lon.append(
            (code, float(lat), float(lon)))
        of.write('\t'.join([code, lat, lon]) + '\n')
    of.close()
    # get dists
    of = open('code_code_dist.tsv', 'w')
    i = 0
    expected_i = len(code_lat_lon) ** 2
    p = -1
    for (code1, lat1, lon1), (code2, lat2, lon2) in product(code_lat_lon, code_lat_lon):
        if code1 == code2:
            continue
        dist = distance_miles(lat1, lon1, lat2, lon2)
        of.write('%s\t%s\t%f\n' % (code1, code2, dist))
        op = int(100* float(i) / float(expected_i))
        if op != p:
            print str(op) + "%"
        p = op
        i += 1
    of.close()


def main2(g_top_codes):
    assert g_top_codes
    code2top_codes = dict()
    last_code = ''
    for line in open('code_code_dist.tsv'):
        code1, code2, dist = line.strip().split('\t')
        dist = float(dist)
        if code1 != last_code:
            if last_code:
                top_codes = []
                for dist, code in sorted(dist_codes):
                    if code not in g_top_codes:
                        continue
                    if dist >= 1000:
                        top_codes.append(code)
                        if len(top_codes) >= 20:
                            break
                assert len(top_codes) == 20, last_code + ' '.join(top_codes)
                code2top_codes[last_code] = top_codes
            last_code = code1
            dist_codes = []
        dist_codes.append((dist, code2))
    of = open('code_nearcodes.tsv', 'w')
    for code, close_codes in code2top_codes.iteritems():
        of.write(code + '\t')
        of.write(','.join(close_codes) + '\n')
    of.close()


def get_top_codes():
    code2city = json.load(open('code_city.json'))
    top_text = open('top1000_cities.txt').read().decode('utf-8').strip().lower()
    top_codes = set()
    for code, city in code2city.items():
        city = city.split(',')[0].lower()
        if city in top_text:
            top_codes.add(code)
    return top_codes


if __name__ == '__main__':
    top_codes = get_top_codes()
    #main()
    main2(top_codes)
