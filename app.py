
from flask import Flask , render_template, request
app = Flask(__name__)




@app.route("/")
def home():
    return render_template('index.html')



@app.route("/encuestas")
def encuestas():
    polls=SystemPoll()
    poll1=Poll(0)
    poll1.addTitle("Encuesta presidencial 2026")
    poll1.addDescription("resultados de vocaciones año 2026")
    polls.addPoll(poll1)
    for i in range(10):
        poll = Poll(i+1)
        poll.addTitle("Title")
        poll.addDescription("description ")
        polls.addPoll(poll)
    
    return render_template("encuestas.html",
        polls=polls.getAll())

@app.route("/encuestados")
def encuestados():
    return render_template('encuestados.html')

@app.route("/nueva_encuesta",methods=['POST'])
def nueva_encuesta():
    if request.method =='POST':
        title=request.form['title']
        des=request.form['description']
        print(title)
        print(des)
    return render_template("nueva_encuesta.html")

class Poll:
    _code=-1
    _title="Encuesta sin Título"
    _description="--?--"
    def __init__ (self,code):
        self._code = code
    def addTitle(self,title):
        self._title = title
    def addDescription(self,description):
        self._description = description
    def getTitle(self):
        return self._title
    def getCode(self):
        return self._code
    def getDescription(self):
        return self._description    
class SystemPoll:
    def __init__ (self):
        self.polls = []
    def addPoll(self,poll):
        self.polls.append(poll);
    def removePoll(self,poll):
        self.polls.remove(poll)
    def getPollcode(self,code):
        for i in self.polls:
            if self.polls[i].getCode()== code:
                return self.polls[i]
        
    def getPoll(self,title):
        for i in self.polls:
            if self.polls[i].getTitle()== title:
                return self.polls[i]
    def getAll(self):
        return self.polls
    def getCount(self):
        return len(self.polls)
    def isEmpty(self):
        if len(self.polls) == 0:
            return True
        else:
            return False
    