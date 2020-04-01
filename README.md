This project was inspired by Matteyeux with his ios-tools repo, this will be a similar project but for my own practice. Also, in native Python 3 code :D

### Note

Due to compatibility, ensure Python 3.6 or newer is installed. Basically this is just due some things being changed like format strings and etc.

### Prerequisites

    pip3 install -r requirements.txt

### Commands

    --buildid device iOS  | convert an iOS to its buildid
    --clean               | if there are any leftover json files, this will get rid of them
    --codename device iOS | get codename of an iOS
    --download device iOS | download an ipsw
    --keys device iOS     | get keys for an iOS
    --signed device       | print the signed versions for a device
    --split key           | splits a GID decrypted key
    --tags file           | print the tags and their hex positions of an img3 file

### Planned

    foreman: key grabbing/uploading
    template: auto key uploading

### Credits

    Visual Studio Code: Holy! I love this IDE! (better than Pycharm...)
    Matteyeux @matteyeux: inspiration, some techniques from ios-tools
    Noah/32Bites @TheNoahParty: some techniques from PyKeys
    mcg29 @mcg29_: Helping with this project
