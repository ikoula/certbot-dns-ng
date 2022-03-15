#!/bin/bash

if [[ ! -f $(which certbot) ]];then
    echo 'certbot est nécessaire, installez le pour continuer'
    exit
fi

if [[ ! -f $(which python3) ]];then
    echo 'python3 est nécessaire, installez le pour continuer'
    exit
fi


if [[ ! -f $(which pip3) ]];then
    echo 'pip3 est nécessaire, installez le pour continuer'
    exit
fi

echo "Afin d'éxecuter les appels API Ikoula, vous devez fournir un compte"
echo -n "Utilisateur : "; read user
echo -n "Mot de passe : "; read -s pass
echo -e "\n"

echo -n "Veuillez indiquer le nom de domaine vous voulez authentifier : "; read domain
echo -e "\n"

echo "La commande qui sera executée sera celle-ci"
echo "
    certbot certonly
    --manual
    --preferred-challenges=dns
    --manual-auth-hook ./ikoula-dns-auth.sh
    --manual-cleanup-hook ./ikoula-dns-cleanup.sh
    --manual-public-ip-logging-ok
    -d $domain -d \*.$domain
    "
read -p "Est-ce que tout est correct ? [O/n] " answervar
if [ ${answervar^^} = "O" ] || [ ${answervar^^} = "Y" ]
then
    echo "Installation dépendence python..."
    pip3 install pycryptodome

    echo "Téléchargement de la clé public d'Ikoula..."
    curl -s https://api.ikoula.com/downloads/Ikoula.API.RSAKeyPub.pem > ./Ikoula.API.RSAKeyPub.pem

    echo 'Mise en place des variables...'
    python3 setup.py $user $pass ./Ikoula.API.RSAKeyPub.pem

    echo 'Authentification DNS...'
    certbot certonly \
    --manual \
    --preferred-challenges=dns \
    --manual-auth-hook ./ikoula-dns-auth.sh \
    --manual-cleanup-hook ./ikoula-dns-cleanup.sh \
    --manual-public-ip-logging-ok \
    -d $domain -d \*.$domain
fi
exit 0