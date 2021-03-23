This project was inspired by Matteyeux with his ios-tools repo, this will be a similar project but for my own practice. Also, in native Python 3 code :D

### Prerequisites

    Python >= 3.6

## How to install
    1. python3 -m venv venv
    2. source venv/bin/activate
    3. pip install .
    
    After this, running "iospytools" will print the help menu,
    also by entering "iospytools -h" or "iospytools --help".

    Use the help menu to dictate which commands are necessary to use one of the features.

### Features

    iospytools -d device -e ecid --shsh (save shsh blobs)

    iospytools -d device -i ios --codename (print codename of an iOS)
    iospytools -d device -i ios --convert (convert an iOS to a buildid)
    iospytools -d device -i ios --download (download an ipsw or OTA file)
    iospytools -d device -i ios --download --path file (download a file from an ipsw or OTA file)
    iospytools -d device -i ios --keys (get keys from theiphonewiki)
    iospytools -d device -i ios --url (print the url of an ios)

    iospytools -d device --signed (get all signed versions for a device)

    iospytools --signed (get all signed versions)


### TODO

    https://trello.com/b/2zGlkvUb/ios-python-tools

### Credits

    Matteyeux @matteyeux: inspiration
    mcg29 @mcg29_: Helping me when needed
    wxblank @wxblank2: TSS code
