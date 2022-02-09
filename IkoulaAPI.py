#################################################
####    ..:: Ikoula Hosting Services ::..     ###
####    Wrapper for https://api.ikoula.com	  ###
#################################################

import requests
from urllib.parse import urlencode
import os
import hmac
from hashlib import sha1
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

class IkoulaAPI:
    # Ikoula API URI
    urlAPI = "https://api.ikoula.com/"

    @classmethod
    def requestApi(self, email: str, password: str, publicKey: str, webservice: str, format: str, type: str, params: dict = {}):
        # Add connexion information
        params['login'] = email
        params['crypted_password'] = self.opensslEncryptPublic(publicKey, password)
        params['format'] = format

        # Fix params to lowercase for generate signature correctly
        params = {k.lower(): v for k, v in params.items()}

        # Generate signature
        signature = self.createSignature(publicKey, params)

        # Add signature for call
        params['signature'] = signature

        # Create API URI
        url = self.urlAPI+webservice

        # Exec request
        if(type == "GET"):
            data = requests.get(url, params)
        elif(type == "POST"):
            data = requests.post(url, params)
        else:
            return False

        return data.text

    @classmethod
    def createSignature(self, publicKey: str, params: dict = {}):
        # Signature to send
        signature = False

        # Verify parameters
        if params:
            # Sort params
            sorted_params = {}
            for key in sorted(params):
                sorted_params[key] = params[key]

            # Encode params
            query = urlencode(sorted_params)

            # Encode "plus "+"
            query = query.replace("+", "%20")

            # Transform in lowercase
            query = query.lower()

            public_key = ""

            # Verify if key file is present
            if os.path.exists(publicKey):
                # Get public key
                f = open(publicKey)
                public_key = f.read()
                f.close()

                public_key = public_key.replace("\n", "").replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "")

            # SHA1 hash
            hash = hmac.digest(public_key.encode(), query.encode(), sha1)

            # base64 encode
            signature = base64.b64encode(hash).decode()

        return signature

    @classmethod
    def opensslEncryptPublic(self, publicKey: str, password: str):
        # Verify if key file exist
        if os.path.exists(publicKey):
            # Verify if password is not empty
            if password:
                # Get file content
                f = open(publicKey)
                public_key = f.read()
                f.close()

                # If we get file content without error
                if public_key:
                    # Encrypt password
                    encrypter = PKCS1_v1_5.new(RSA.importKey(public_key))
                    crypted = encrypter.encrypt(password.encode())

                    if crypted:
                        return base64.b64encode(crypted).decode()
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
