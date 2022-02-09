from IkoulaAPI import IkoulaAPI
import argparse
import json

parser = argparse.ArgumentParser(description='DNS Authentification')
parser.add_argument('CERTBOT_DOMAIN', type=str)
parser.add_argument('CERTBOT_VALIDATION', type=str)

args = parser.parse_args()

# On récupère les données d'authentification
json_file = open("config.json", 'r')
data = json.load(json_file)
json_file.close()

request = IkoulaAPI.requestApi(data['login'], data['password'], data['publicKeyPath'], "wsndd/add-dns-registration", "JSON", "GET", {'CERTBOT_DOMAIN': args.CERTBOT_DOMAIN, 'CERTBOT_VALIDATION': args.CERTBOT_VALIDATION})

print(request)