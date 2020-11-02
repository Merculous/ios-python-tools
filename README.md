This project was inspired by Matteyeux with his ios-tools repo, this will be a similar project but for my own practice. Also, in native Python 3 code :D

### Prerequisites

    1. Run: pip install -U . (if building locally)
    2. You should then have a module called: "iospytools"

    Example: iospytools --keys iPhone2,1 3.0

### Commands

    --buildid device iOS  | convert an iOS to its buildid
    --codename device iOS | get codename of an iOS
    --download device iOS | download an ipsw
    --img3 file           | print the info of an img3 file
    --keys device iOS     | get keys for an iOS
    --manifest device iOS | downloads a BuildManifest.plist (ipsw only right now)
    --shsh device ecid    | save SHSH for all signed iOS versions of a device (Disabled atm, needs updating.)
    --signed device       | print the signed versions for a device
    --split key           | splits a GID decrypted key
    --tags file           | print the tags of an img3 file

### TODO

    foreman: key grabbing/uploading
    template: template creating
    ota/beta shsh saving: CC @mcg29_ (almost done!)
    img3: iBoot patcher, kernel patcher
    img4: idk if I can make this lol
    ipsw: ipsw handling and creating

### Credits

    Visual Studio Code: Holy! I love this IDE! (better than Pycharm...)
    Matteyeux @matteyeux: inspiration, some techniques from ios-tools
    Noah/32Bites @TheNoahParty: some techniques from PyKeys
    mcg29 @mcg29_: Helping with this project
    wxblank @wxblank2: TSS stuff!
