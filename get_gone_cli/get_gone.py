import datetime
import json
import requests
import copy

from collections import namedtuple

FlightList = namedtuple('FlightList',
    ['dest', 'min_price', 'response'])
api_url = 'https://www.googleapis.com/qpxExpress/v1/trips/search'


NUM_DESTINATION_QUERIES = 5
JSON_TEMPLATE = {
  "request": {
    "slice": [
      {
        "origin": None,
        "destination": None,
        "date": None,
      }
    ],
    "passengers": {
      "adultCount": 1,
      "infantInLapCount": 0,
      "infantInSeatCount": 0,
      "childCount": 0,
      "seniorCount": 0
    },
    "solutions": 20,
    "refundable": False
  }
}


def calc_price(json_dump):
    # generate request
    # submit request
    # wait for request
    # unwrap request
    pass


def get_candidates(home_airport):
    for line in open('/Users/alexrson/software/thousand_escape/GetGone/calc_inter_airport_dists/code_nearcodes.tsv'):
        if not line.startswith(home_airport):
            continue
        return line.strip().split()[1].split(',')
    raise ValueError('Airport not found: %s' % home_airport)

def main():
    today_date = datetime.datetime.now().isoformat().split('T')[0]
    tomorrow_date = (datetime.datetime.now() + datetime.timedelta(days=1)
        ).isoformat().split('T')[0]
    n = datetime.datetime.now()
    now_time = ':'.join(n.isoformat().split('T')[1].split(':')[:2])
    home_airport = str(raw_input('home airport:')).upper()

    assert len(home_airport) == 3
    # find N closest airports > 1000 miles away sorted by distance
    destination_codes = get_candidates(home_airport)

    # for airport in airports
    for code in destination_codes[0:2]:  # TODO once bugs are done lose this
        j = copy.deepcopy(JSON_TEMPLATE)
        # calc price to fly today ( if it's before noon )
        j['request']['slice'][0]['destination'] = code
        j['request']['slice'][0]['date'] = today_date
        r = requests.post(api_url, data=json.dumps(j))
        # calc price to fly tomorrow
        j2 = copy.deepcopy(JSON_TEMPLATE)
        j2['request']['slice'][0]['destination'] = code
        j2['request']['slice'][0]['date'] = tomorrow_date
        j2['request']['slice'][0]["permittedDepartureTime"] = {"latestTime":  now_time}
        break
    print r
    print r.text
    print r.raw
    print r.json()




if __name__ == '__main__':
    main()
