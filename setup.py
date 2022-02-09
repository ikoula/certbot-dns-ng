import argparse
import json

parser = argparse.ArgumentParser(description='DNS Authentification')
parser.add_argument('login', type=str)
parser.add_argument('password', type=str)
parser.add_argument('publicKeyPath', type=str)

args = parser.parse_args()

data = {}
# On modifie les valeurs
data['login'] = args.login
data['password'] = args.password
data['publicKeyPath'] = args.publicKeyPath

# On sauvegarde
json_file = open('config.json', 'w')
json.dump(data, json_file)
json_file.close()