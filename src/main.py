import settings
import my_logging
import token_provider
from public_ip_finder import public_ip_service

import dropbox
import os
import time


config = None
try:
    config = settings.AppSettings(
        os.getenv("APP_DPX_APIKEY"),
        os.getenv("APP_DPX_APISECRET"),
        os.getenv("APP_DPX_TOKENFILE"),
        os.getenv("APP_CLIENT_NAME"),
        os.getenv("APP_CHECK_INTERVAL_MIN"),
        os.getenv("APP_CHECK_SERVICE")
    )

    if not public_ip_service.check_service(config.check.service):
        available_services = public_ip_service.get_all_services()
        raise Exception("{} is not a service. Available services: {}".format(config.check.service, available_services))

    my_logging.info("Configuration loaded.")
    my_logging.debug(str(config))
except Exception as e:
    my_logging.error("Configuration error: {}".format(str(e)))
    exit(1)


oauth2_access_token = ''
try:
    tp = token_provider.TokenProvider(
        config.dropbox.api_key,
        config.dropbox.api_secret,
        config.dropbox.token_file_name
    )
    oauth2_access_token = tp.token()
    my_logging.info("Access token retrieved.")
    my_logging.debug(oauth2_access_token)
except Exception as ex:
    my_logging.error("Unable to retrieve access token: {}".format(str(ex)))
    exit(1)


dbx = None
try:
    dbx = dropbox.Dropbox(oauth2_access_token=oauth2_access_token)
    account_info = dbx.users_get_current_account()
    my_logging.info("Access granted by user <{}>.".format(account_info.email))
except Exception as ex:
    my_logging.error("Unable to retrieve account info".format(str(ex)))
    exit(1)

ip_service = public_ip_service.get_service(config.check.service)
cached_ip = None
while True:
    my_logging.info("Getting the current public ip...")
    try:
        current_ip = ip_service.get_public_ip()

        if not public_ip_service.check_ip(current_ip):
            my_logging.error("The service has returned an invalid ip: {}".format(current_ip))
        else:
            if current_ip != cached_ip:
                my_logging.info("New IP found: {}".format(current_ip))
                try:
                    file_metadata = dbx.files_upload(
                        bytes(current_ip, 'utf-8'),
                        "/{}_public-ip.txt".format(config.client.name),
                        mute=True,
                        mode=dropbox.dropbox.files.WriteMode.overwrite
                    )
                    my_logging.info("New IP updated on DropBox")
                    my_logging.debug("{}, {}".format(file_metadata.id, file_metadata.server_modified))
                    cached_ip = current_ip
                except Exception as ex:
                    my_logging.error("Error updating the IP on DropBox: {}".format(str(ex)))
            else:
                my_logging.info("The current IP is not changed since last check. No updating needed.")
    except Exception as ex:
        my_logging.error("Unable to retrieve the current public IP: {}".format(str(ex)))

    my_logging.info("Next check in {} minutes.".format(config.check.interval))
    time.sleep(60 * config.check.interval)
