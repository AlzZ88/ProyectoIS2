
from flask import Flask , render_template, request, redirect, url_for

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





app = Flask(__name__)#-------> Main de la aplicación

# Se inicializa el almacen de encuestas
polls=SystemPoll()

poll1=Poll(1)#-------> Encuesta de prueba
poll1.addTitle("Encuesta presidencial 2026")
poll1.addDescription("resultados de vocaciones año 2026")
polls.addPoll(poll1)


#-------> Aca deberia estar la query de la base de datos



@app.route("/")
def home():#----> pagina home
    return render_template('index.html')

"""
pagina de encuestas, recive el objeto SystemPoll que contiene todas
las encuestas y las despliega
"""
@app.route("/encuestas")
def encuestas():#----> pagina

    return render_template("encuestas.html",
        polls=polls.getAll())

@app.route("/encuestados")
def encuestados():
    return render_template('encuestados.html')

@app.route("/nueva_encuesta")
def nueva_encuesta():
    return render_template("nueva_encuesta.html")

@app.route("/crear_encuesta", methods=['POST'])
def crear_encuesta():
    if request.method =='POST':
        title=request.form['title']
        des=request.form['description']
        print("Ingresar en base de datos "+title+" y "+ des+".")
        newpoll=Poll(polls.getCount()+1)
        newpoll.addTitle(title)
        newpoll.addDescription(des)
        polls.addPoll(newpoll)
    return redirect(url_for('encuestas'))


    