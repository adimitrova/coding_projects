To Use Dropbox to save the files, see setup instructions below:

Go to https://www.dropbox.com/developers/apps

Create an application and inside the `epubidy/systems/vault` folder, create a file called `api_keys.json` and replace the `xxxxxx` with your token and keys as follows:
(You could use a different filename as well, but have to specify its name in the epubify config file later.)

```json
{
    "dropbox": {
        "token": "xxxxxx",
        "app_key": "xxxxxx",
        "app_secret": "xxxxxx"
    }
}
```
