# iScoop

I wasn't able to find a really simple way of downloading all the photos and videos off my iphone 5 with my Ubuntu linux laptop. 

I was told it would work upon plugging it in. It did not. I went through some `apt install ...` suggested by some answers on google (`libimobiledevice`, etc), but it didn't resolve the issue. I tried installing `shotwell` and using it, but it would fail with an error being able to access the USB device. That led to bugreports and elaborate solutions I was hardly interested in.

Enter `iScoop`. 

Things that are pretty easy to do:
1. make your laptop into a private WiFi AP
2. run a web upload server

## Prerequisites

You'll need to have python installed. That's it.

## WiFi AP

It's true. Much of the simplicity and security of `iScoop` comes from the easy and security of your ability to make a good WiFi access point (AP) with your computer. Unfortunately, not all platforms are the same, so provided are some basic instructions to get you started. They've been tested as working as of `Aug 29, 2017`.

#### In Ubuntu:

Steps:

1. go to your `WiFi Settings`, either through the `Settings` application or the menu bar
2. select `Use as Hotspot` and you should see the name and password associated with your Access Point

#### In Windows:

Steps:

1. I have no idea.

#### In OS X:

Steps:

1. You'll, first, need to set up having the Loopback network interface show up `Network Preferences`.
	- `sudo networksetup -createnetworkservice Loopback lo0`
	- `sudo networksetup -setmanual Loopback 172.20.42.42 255.255.255.255`
2. Open up `Sharing` from `Settings`
3. Share your connection from: `Loopback` to computers using `Wi-Fi`
4. You can set up your `Wi-Fi Options` as you'd like to improve security

## Usage

After downloading this repo, you:

1. start your computer/laptop as a WiFi AP
2. connect your iDevice to that WiFi AP
3. run `iscoop` by executing `python iscoop.py` in your terminal
4. open up Safari (see Notes) and upload away!

## Thanks

Your help to quicken the making of this tool is greatly appreciated.

- [hayageek](https://github.com/hayageek/jquery-upload-file/) for a simple js uploader.

## Notes

Apparently, you need to use safari on iOS to be able to upload `.mov` files because [there's an issue](https://bugs.chromium.org/p/chromium/issues/detail?id=414769) with 0-byte file reporting.

## License

Copyright (c) 2017 Aditya Natraj aditya@jawns.us

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


