import requests
import dropbox
import os
import time
import uuid
import ipextractor
from tokenprovider import gettoken
from datetime import datetime

current_client_name = os.getenv('CLIENT_NAME', uuid.getnode())
print("{} [     CLIENT NAME] :: {}".format(datetime.now(), current_client_name))

check_interval_minutes = max(1, int(os.getenv('CHECK_INTERVAL_MIN', '30')))
print("{} [  CHECK INTERVAL] :: {} min.".format(datetime.now(), check_interval_minutes))

oauth2_access_token = ''
try:
    oauth2_access_token = gettoken()
    print("{} [         DROPBOX] :: access token retrieved.".format(datetime.now()))
except Exception as ex:
    print("{} [         DROPBOX] :: Unable to retrieve access token: {}".format(datetime.now(), str(ex)))
    exit(1)

dbx = None
try:
    dbx = dropbox.Dropbox(oauth2_access_token=oauth2_access_token)
    account_info = dbx.users_get_current_account()
    print("{} [         DROPBOX] :: Access granted by user <{}>.".format(datetime.now(), account_info.email))
except Exception as ex:
    print("{} [         DROPBOX] :: Unable to retrieve account info: {}".format(datetime.now(), str(ex)))
    exit(1)

check_ip_url = os.getenv('CHECK_IP_URL', 'http://checkip.dyndns.it')
print("{} [    CHECK IP URL] :: {}".format(datetime.now(), check_ip_url))

check_ip_service = os.getenv('CHECK_IP_SERVICE', 'dyndns').lower().strip()
print("{} [CHECK IP SERVICE] :: {} (available services: {})".format(datetime.now(), check_ip_service,
                                                                    ipextractor.AvailableServices))

if check_ip_service not in ipextractor.AvailableServices:
    print("{} [CHECK IP SERVICE] :: {} is not a supported service".format(datetime.now(), check_ip_service))
    exit(1)

ip_extractor = None
try:
    ip_extractor = ipextractor.IpExtractorFactory(check_ip_service)
except Exception as ex:
    print("{} [    IP EXTRACTOR] :: Error getting the right ip extractor: {}".format(datetime.now(), str(ex)))
    exit(1)

while True:
    try:
        response = requests.get(check_ip_url, stream=True)
        print("{} [        CHECK IP] :: <{} {}>".format(datetime.now(), response.status_code, response.reason))

        if response.status_code == requests.codes.ok:
            try:
                ip_extractor.feed(response.text)
                ip = ip_extractor.ip()
                print("{} [    IP EXTRACTOR] :: Current public IP: {}".format(datetime.now(), ip))
                try:
                    file_metadata = dbx.files_upload(
                        bytes(ip, 'utf-8'),
                        "/{}_public-ip.txt".format(current_client_name),
                        mute=True,
                        mode=dropbox.dropbox.files.WriteMode.overwrite
                    )
                    print("{} [         DROPBOX] :: File uploaded. <{}, {}>".format(datetime.now(), file_metadata.id,
                                                                                    file_metadata.server_modified))

                except Exception as ex:
                    print("{} [         DROPBOX] :: Error uploading file on the cloud: {}".format(datetime.now(),
                                                                                                  str(ex)))

            except Exception as e:
                print("{} [    IP EXTRACTOR] :: {}".format(datetime.now(), str(e)))

        else:
            print("{} [        CHECK IP] :: Unable to retrieve the current public IP".format(datetime.now()))

    except Exception as ex:
        print("{} [        CHECK IP] :: Request error: {}".format(datetime.now(), str(ex)))
    
    print("{} [           SLEEP] :: next check in {} minutes.".format(datetime.now(), check_interval_minutes))
    time.sleep(60 * check_interval_minutes)
