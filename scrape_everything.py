import auth
import scraper
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')
config = cfg["DEFAULT"]

# everything i want to scrape
everything = config["EVERYTHING"].split(",")

for thing in everything:
    try:
        scraper.scrape_file(thing)
    except scraper.StaleCookieException:
        auth.authenticate()
        scraper.scrape_file(thing)
