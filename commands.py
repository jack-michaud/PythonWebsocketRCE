
import abc


'''
Custom commands for the javascript interpreter.

E.g.
>pwned - Clears the whole screen and replaces it with a glitchy image

'''


class CMD(object):

    def __init__(self, name, command, description):
        self.name = name
        self.command = command
        self.description = description
        self.argv = []

    def matches_command(self, arg):
        if len(arg) > 0 and arg[0] == ">":
            if arg[1:].split(' ')[0] == self.command:
                self.argv = arg.split(' ')
                return True
        return False

    @abc.abstractmethod
    def get_payload(self):
        return

class CommandPWN(CMD):

    def __init__(self):
        super(CommandPWN, self).__init__(
              "PWN",
              "pwned",
              "Clears the whole screen and replaces it with glitchy text (usage: >pwned [Text])")

    def get_payload(self):
        cmd = CommandClearBody()
        payload = cmd.get_payload()
        payload = payload + """
            (function (){
              var canvas = document.createElement('canvas');
              canvas.id = "c";
              canvas.width = "1000";
              canvas.height = "500";
              document.body.appendChild(canvas);
              var ctx = canvas.getContext('2d');
              var text = \"""" + " ".join(self.argv[1:]) + """\";

              var count = 200;
              var dir = 5;

              ctx.textAlign = "center"
              ctx.textBaseline = "middle";
              ctx.font = "200pt Arial";


              function ret(nr) {
                return Math.abs((nr%400) + 100);
              }
              function pos(nr) {
                //return nr;

                if(nr<300) {
                  return ret(nr);
                }


                if(nr>=500 && nr<700) {
                  return ret((nr-300)/2 + 300);
                }

                return ret((500-nr));

              }

              function step() {
                count += dir;


                if(count >= 1000) {
                  count = 200;
                  window.setTimeout(function(){window.requestAnimationFrame(step)},500);
                  return;
                }

                var top = pos(count);

                ctx.clearRect(0,0,1000,500);

                ctx.save();
                ctx.beginPath();
                ctx.rect(0,top,1000,100);
                ctx.clip();
                ctx.fillStyle = "blue"
                ctx.fillText(text,495,245,1000,500)
                ctx.restore();

                ctx.save();
                ctx.beginPath();
                ctx.rect(0,top-100,1000,10);
                ctx.clip();
                ctx.fillStyle = "red"
                ctx.fillText(text,505,255,1000,500)
                ctx.restore();

                  ctx.fillStyle = "white"
                ctx.fillText(text,500,250,1000,500)


                bw(top,40,10,1000,500);
                bw(top,120,-17,500,0);



                window.requestAnimationFrame(step)
              }

              function bw(top,o,off,r,i) {
                    ctx.save();
                ctx.beginPath();
                ctx.rect(i,top-o,r,30);
                ctx.clip();
                ctx.fillStyle = "black"
                ctx.fillText(text,500,250,1000,500)
                ctx.restore();

                ctx.save();
                ctx.beginPath();
                ctx.rect(i,top-o,r,20);
                ctx.clip();
                ctx.fillStyle = "white"
                ctx.fillText(text,500-off,250,1000,500)
                ctx.restore();
              }


              window.requestAnimationFrame(step)
            })();

        """
        return payload

class CommandClearBody(CMD):

    def __init__(self):
        super(CommandClearBody, self).__init__(
              "Clear Body",
              "clearbody",
              "Clears the whole client webpage.")

    def get_payload(self):
        return """
            var body = document.createElement('body');
            document.body = body;
        """

class CommandFishy(CMD):

    def __init__(self):
        super(CommandFishy, self).__init__(
              "Fishy",
              "fishy",
              "Adds an intensified Penguin/fish sticker to the bottom of a page.")

    def get_payload(self):
        return """
            var img = document.createElement('img');
            img.src="http://i.imgur.com/zIRoFeJ.gif";
            img.width="1000";img.height="1200";
            document.body.appendChild(img);
        """

class CommandInsertImage(CMD):

    def __init__(self):
        super(CommandInsertImage, self).__init__(
              "Insert Image",
              "insertimage",
              "Adds an image to the end of a webpage. (usage: >insertimage [url])")

    def get_payload(self):
        if len(self.argv) < 2:
            print "Must provide URL (usage: >insertimage [url])"
            return ""

        return """
            var img = document.createElement('img');
            img.src="{}";
            img.width="1000";img.height="1200";
            document.body.appendChild(img);
        """.format(self.argv[1])

class CommandInsertImage(CMD):

    def __init__(self):
        super(CommandInsertImage, self).__init__(
              "Request Notification",
              "reqnote",
              "Requests notification in a browser.")

    def get_payload(self):
        return """Notification.requestPermission().then(function(result) {
                    console.log(result);
                    });"""
