# Let's encrypt DNS challenge Ikoula

Scripts permettant de créer un certificat grâce à Certbot et de l'enregistrer auprès du DNS Ikoula via l'API.

## Pré-requis
Les dépendances certbot, python 3 et python3-pip sont nécessaires.

Assurez-vous que les fichiers install.sh, ikoula-dns-auth.sh et ikoula-dns-cleanup.sh possèdes le droit d'exécution

## Utilisation
Afin d'exécuter le script, lancez la commande suivante:

```shell
./install.sh
```

Il vous suffit ensuite de suivre les instructions.