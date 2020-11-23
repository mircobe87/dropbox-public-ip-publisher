import requests
import dropbox
import os
import time
import uuid
from dyndns import DynDnsIpExtractor
from tokenprovider import gettoken
from datetime import datetime

current_client_name = os.getenv('CLIENT_NAME', uuid.getnode())
print("{} [     CLIENT NAME] :: {}".format(datetime.now(), current_client_name))

check_interval_minutes = max(1, int(os.getenv('CHECK_INTERVAL_MIN', '30')))
print("{} [  CHECK INTERVAL] :: {} min.".format(datetime.now(), check_interval_minutes))

try:
    oauth2_access_token = gettoken()
    print("{} [         DROPBOX] :: access token retrieved.".format(datetime.now()))
except expression as ex:
    print("{} [         DROPBOX] :: Unable to retrieve access token: {}".format(datetime.now(), str(ex)))
    exit(1)

try:
    dbx = dropbox.Dropbox(oauth2_access_token=oauth2_access_token)
    account_info = dbx.users_get_current_account()
    print("{} [         DROPBOX] :: Access granted by user <{}>.".format(datetime.now(), account_info.email))
except Exception as ex:
    print("{} [         DROPBOX] :: Unable to retrieve account info: {}".format(datetime.now(), str(ex)))
    exit(1)

check_ip_url = os.getenv('CHECK_IP_URL', 'http://checkip.dyndns.it')
print("{} [        CHECK IP] :: {}".format(datetime.now(), check_ip_url))



while True:
    try:
        response = requests.get(check_ip_url, stream=True)
        print("{} [        CHECK IP] :: <{} {}>".format(datetime.now(), response.status_code, response.reason))

        if response.status_code == requests.codes.ok:
            ip_extractor = DynDnsIpExtractor()
            try:
                ip_extractor.feed(response.text)
                ip = ip_extractor.ip()
                print("{} [    IP EXTRACTOR] :: Current public IP: {}".format(datetime.now(), ip))
                try:
                    file_metadata = dbx.files_upload(
                        bytes(ip, 'utf-8'),
                        "/{}_public-ip.txt".format(current_client_name),
                        mute=True,
                        mode=dropbox.files.WriteMode.overwrite
                    )
                    print("{} [         DROPBOX] :: File uploaded. <{}, {}>".format(datetime.now(), file_metadata.id, file_metadata.server_modified))

                except Exception as ex:
                    print("{} [         DROPBOX] :: Error uploading file on the cloud: {}".format(datetime.now(), str(ex)))

            except Exception as e:
                print("{} [    IP EXTRACTOR] :: {}".format(datetime.now(), str(e)))

        else:
            print("{} [        CHECK IP] :: Unable to retrieve the current public IP".format(datetime.now()))

    except Exception as ex:
        print("{} [        CHECK IP] :: Request error: {}".format(datetime.now(), str(ex)))
    
    print("{} [           SLEEP] :: next check in {} minutes.".format(datetime.now(), check_interval_minutes))
    time.sleep(60 * check_interval_minutes)


