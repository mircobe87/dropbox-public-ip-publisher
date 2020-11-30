import settings
import my_logging
import token_provider
from public_ip_finder import public_ip_service

import dropbox
import os
import time

if __name__ == "__main__":

    log_level = my_logging.log_level_from_name(os.getenv("APP_LOG_LEVEL"))
    Logger = my_logging.Logger(log_level)

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
            raise Exception(
                "{} is not a service. Available services: {}".format(config.check.service, available_services))

        Logger.info("Configuration loaded.")
        Logger.debug(str(config))
    except Exception as e:
        Logger.error("Configuration error: {}".format(str(e)))
        exit(1)

    oauth2_access_token = ''
    try:
        tp = token_provider.TokenProvider(
            config.dropbox.api_key,
            config.dropbox.api_secret,
            config.dropbox.token_file_name
        )
        oauth2_access_token = tp.token()
        Logger.info("Access token retrieved.")
        Logger.debug(oauth2_access_token)
    except Exception as ex:
        Logger.error("Unable to retrieve access token: {}".format(str(ex)))
        exit(1)

    dbx = None
    try:
        dbx = dropbox.Dropbox(oauth2_access_token=oauth2_access_token)
        account_info = dbx.users_get_current_account()
        Logger.info("Access granted by user <{}>.".format(account_info.email))
    except Exception as ex:
        Logger.error("Unable to retrieve account info".format(str(ex)))
        exit(1)

    ip_service = public_ip_service.get_service(config.check.service)
    cached_ip = None
    while True:
        Logger.info("Getting the current public ip...")
        try:
            current_ip = ip_service.get_public_ip()

            if not public_ip_service.check_ip(current_ip):
                Logger.error("The service has returned an invalid ip: {}".format(current_ip))
            else:
                if current_ip != cached_ip:
                    Logger.info("New IP found: {}".format(current_ip))
                    try:
                        file_metadata = dbx.files_upload(
                            bytes(current_ip, 'utf-8'),
                            "/{}_public-ip.txt".format(config.client.name),
                            mute=True,
                            mode=dropbox.dropbox.files.WriteMode.overwrite
                        )
                        Logger.info("New IP updated on DropBox")
                        Logger.debug("{}, {}".format(file_metadata.id, file_metadata.server_modified))
                        cached_ip = current_ip
                    except Exception as ex:
                        Logger.error("Error updating the IP on DropBox: {}".format(str(ex)))
                else:
                    Logger.info("The current IP is not changed since last check. No updating needed.")
        except Exception as ex:
            Logger.error("Unable to retrieve the current public IP: {}".format(str(ex)))

        Logger.info("Next check in {} minutes.".format(config.check.interval))
        time.sleep(60 * config.check.interval)
