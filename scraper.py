import requests
import csv
import sys
from lxml import etree
from datetime import datetime
import configparser
import influxdb_client

class StaleCookieException(Exception):
    pass

def scrape_file(resource=None):
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    config = cfg["DEFAULT"]

    if not resource and len(sys.argv) > 1:
        resource = sys.argv[1]
    elif not resource:
        resource = config["RESOURCE"]


    address = config["ADDRESS"]
    url = f"http://{address}/{resource}.XML"

    cookie_id = config["COOKIE"]

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0",
        "Accept": "application/xml, text/xml, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"http://{address}/main.xml",
        "Cookie": f"SoftPLC={cookie_id}; language=cs"
    }

    print(f"getting {resource}")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"HTTP code {response.status_code}")
    elif response.url.endswith("LOGIN.XML"):
        raise StaleCookieException("Stale cookie! Reauth please!")

    tree = etree.fromstring(response.content)

    main_vals = {}
    with open(f'scraping_mapping/{resource}.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            main_vals = row

    # results: dict[str, str] = {"TIME": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    results: dict[str, str] = {}

    for key in main_vals:
        el = tree.xpath(main_vals[key])[0]
        val = el.attrib["VALUE"]
        results[key] = val

    # influx
    influx_url = config["INFLUX_URL"]
    influx_token = config["INFLUX_TOKEN"]
    influx_org = config["INFLUX_ORG"]
    influx_bucket = config["INFLUX_BUCKET"]
    client = influxdb_client.InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
    write_api = client.write_api(write_options=influxdb_client.client.write_api.SYNCHRONOUS)

    point = influxdb_client.Point(resource) # event name = resource

    for result in results:
        point = point.field(result, float(results[result])) # add the results

    write_api.write(bucket=influx_bucket, org=influx_org, record=point)

    print(f"got {resource}")

if __name__ == "__main__":
    scrape_file()
