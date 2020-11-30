# Dropbox Public IP Publisher
*A python application used to write on your DropBox account your public ip.*

Useful if you need to reach some services exposed on internet by a dynamic ip. In this case this little
application can be run inside your private network and periodically it updates a text file in your
**DropBox** account putting inside it your public ip.

## Configuration
*This application needs several environment variables to be configured in order to do its job.*

+ **APP_DPX_APIKEY**: The api key used to interact to Dropbox API's
+ **APP_DPX_APISECRET**: The api secret used to interact to Dropbox API's
+ **APP_DPX_TOKENFILE**: After the first run, the requested access token is stored into a local text
  file located into `src/tokens/` folder. This variable defines its name.
+ **APP_CLIENT_NAME**: Defines the name to identify this client. This value is also used as prefix in
  the name of the file created on DropBox. (*Default: an integer generated from MAC address*)
+ **APP_CHECK_INTERVAL_MIN**: Defines the length of the checking interval period in minutes.
  It must be an integer value. (*Default: 30 minutes*)
+ **APP_CHECK_SERVICE**: To retrieve public IPs, this application uses several public webservices.
  Here a list of all supported services:
  - `dyndns` http://checkip.dyndns.it (*Default*)
  - `ipify` https://www.ipify.org
+ **APP_LOG_LEVEL**: Sets the verbosity of the console output. Available values are `debug`, `warning`,
  `info` and `error`. (*Default: `info`*)

Before to use this tool you need to have a **Api Key** and a **Api Secret**.
To achieve this go to DropBox developer [page](https://www.dropbox.com/developers) then create you app.
Allow public client access and set a non-expiring token.
Since this application writes a file, go to permission section and be sure that `files.content.write`
scope is selected.

At the first run, the application will ask you for an authorization code. To retrieve that, simply follow the
prompted steps otherwise you need to put an access token inside the related file in `src/tokens/`. You
can generate an access token from you application settings [page](https://www.dropbox.com/developers/apps).

## Docker
*Running this application in a docker container.*

Is also possible to "dockerize" this application building its docker image.
To do so, run the command:
```
docker build -f Dockerfile -t dropbox-publicip-publisher .
```
Then you can run a new container configuring the "dockerized" application setting up its environment variables:
```
docker run -d --name my-dropbox-publicip-publisher \
           -e "APP_DPX_APIKEY=..." \
           -e "APP_DPX_APISECRET=..." \
           -e "APP_DPX_TOKENFILE=..." \
           -e "APP_CLIENT_NAME=..." \
           -e "APP_CHECK_INTERVAL_MIN=..." \
           -e "APP_CHECK_SERVICE=..." \
           -e "APP_LOG_LEVEL=..." \
           -v /local/path/to/token/folder:/app/tokens
           dropbox-publicip-publisher
```
In this example we have run the container in a detached way (`-d` option) thus you need to
mount in `/app/tokens` a folder containing the token file where its name has been specified
by `APP_DPX_TOKENFILE` env. variable.

If you run the container in a interactive way (replace `-d` to `-it`) the application will
prompt you some steps to follow in order to authorize the application. After that the application
will be able to retrieve the access token on its own so you don't need to mount anything.
```
docker run -it --name my-dropbox-publicip-publisher \
           -e "APP_DPX_APIKEY=..." \
           -e "APP_DPX_APISECRET=..." \
           -e "APP_DPX_TOKENFILE=..." \
           -e "APP_CLIENT_NAME=..." \
           -e "APP_CHECK_INTERVAL_MIN=..." \
           -e "APP_CHECK_SERVICE=..." \
           -e "APP_LOG_LEVEL=..." \
           dropbox-publicip-publisher
```
