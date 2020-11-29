# Dropbox Public IP Publisher
*A python application used to write on your DropBox account you public ip*

Useful you need to reach some services exposed on internet by a dynamic ip. In this case this little
application can be run inside your private network and periodically updates a text file in your **DropBox**
account putting inside it your public ip.

## Configuration
*This application needs several environment variables to be configured in order to do its job.*

+ **DPX_APIKEY**: The api key used to interact to Dropbox API's
+ **DPX_APISECRET**: The api secret used to interact to Dropbox API's
+ **DPX_TOKENFILE**: After the first run, the requested access token is stored into a local text
                     file located into `src/tokens/` folder. This variable defines its name.
+ **CLIENT_NAME**: Defines the name to identify this client. This value is also used as prefix in
                   the name of the file created on DropBox. (*Default: an integer generated from MAC address*)
+ **CHECK_INTERVAL_MIN**: Defines the length of the checking interval period in minutes.
                          It must be an integer value. (*Default: 30 minutes*)
+ **CHECK_IP_URL**: The URL of a public service that somehow returns the current public ip.
                    This tool sends a `GET` request and passes the text response to a parser that proceses it.
                    (*Default: http://checkip.dyndns.it*)

Before use this tool you need to have a **Api Key** and a **Api Secret**.
To achieve this go to DropBox developer [page](https://www.dropbox.com/developers) then create you app.
Allow public client access and set a non-expiring token.
Since this application writes a file, go to permission section and be sure that `files.content.write`
scope is selected.

At the first run, the application will ask you for an authorization code. To retrieve that, simply follow the
prompted steps otherwise you need to put an access token inside the related file in `src/tokens/`. You can
generate an access token from you application settings [page](https://www.dropbox.com/developers/apps).

## Docker
*Running this application in a docker container.*

Is also possible to "dockerize" this application building the image running the command:
```
docker build -f Dockerfile -t dropbox-publicip-publisher .
```
Then you can run a new container configuring the "dockerized" application setting up its environment variables:
```
docker run -d --name my-dropbox-publicip-publisher \
           -e "DPX_APIKEY=..." \
           -e "DPX_APISECRET=..." \
           -e "DPX_TOKENFILE=..." \
           -e "CLIENT_NAME=..." \
           -e "CHECK_INTERVAL_MIN=..." \
           -e "CHECK_IP_URL=..." \
           -v /local/path/to/token/folder:/app/tokens
           dropbox-publicip-publisher
```
In this example we have run the container in a detached way (`-d` option) thus you need to
mount in `/app/tokens` a folder containing the token file where its name has been specified
by `DPX_TOKENFILE` env. variable.

If you run the container in a interactive way (replace `-d` to `-it`) the application will
prompt you some steps to follow in order to authorize the application. After that the application
will be able to retrieve the access token on its own so you don't need to mount anything.
```
docker run -it --name my-dropbox-publicip-publisher \
           -e "DPX_APIKEY=..." \
           -e "DPX_APISECRET=..." \
           -e "DPX_TOKENFILE=..." \
           -e "CLIENT_NAME=..." \
           -e "CHECK_INTERVAL_MIN=..." \
           -e "CHECK_IP_URL=..." \
           dropbox-publicip-publisher
```
