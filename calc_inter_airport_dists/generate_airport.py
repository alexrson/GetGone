import json


def main():
    code2city_name = {}
    for line in open('list_of_airports.txt'):
        city = line.split('(')[0].strip()
        code = line.split('(')[-1].split(')')[0]
        print code
        assert len(code) == 3
        code2city_name[code] = city
    json.dump(code2city_name,
              open('code_city.json', 'w'),
              indent=2)

if __name__ == '__main__':
    main()
