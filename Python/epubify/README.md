<img src="img/epubify.png" alt="drawing" width="300"/>

# ePubify

Have you ever wanted to read that huge article, but in a more readable format AND on your EBOOK reader? Maybe you started reading it, but didn't have time to finish? Maybe you use the Pocket application to save your articles? BUT that's not the same like your favourite Kindle or Pocketbook device?! Your eyes hurt?

ePubify is the answer to all that - it's a small application that will fetch the text from your article by having the URL and will store the output epub file directly on your dropbox. If you dropbox contains the folder which your Pocketbook or Kindle syncs from, that means you automatically get that long and interesting article ready for you to sync down on your device and read on your way to work! :) 

Enjoy!

### Installation
------------

```shell
git clone git://github.com/adimitrova/coding_projects.git
cd Python/epubify
pip install -e requirements.txt
```


#### Saving on different systems: 
1. To Use Dropbox to save the files, you need to authorize the Dropbox application,
see setup instructions below:

Go to https://www.dropbox.com/developers/apps

Create an application with the following settings:

```shell

Name: epubify
Permission type: Full Dropbox

```

Next, on your machine go to the epubify directory and inside the `epubidy/systems/vault` folder, create a file called `api_keys.json` and replace the `xxxxxx` with your token and keys as follows:

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
