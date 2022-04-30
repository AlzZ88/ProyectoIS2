
from flask import Flask , render_template, request, redirect, url_for
from flask_mysqldb import MySQL
#(id_encuesta, nombre, descripcion, estado, fecha_inicio, fecha_fin , id_encuestador)
class Poll:
    _code=-1
    _title="Encuesta sin Título"
    _description="--?--"
    estado=1
    
    def __init__ (self,code):
        self._code = code
        self.estado = 1
    def addTitle(self,title):
        self._title = title
    def addDescription(self,description):
        self._description = description
    def setState(self,state):
        self.estado = state
    def getTitle(self):
        return self._title
    def getCode(self):
        return self._code
    def getDescription(self):
        return self._description
    def getState(self):
        return self.estado    
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
       
    def getPolltitle(self,title):
        for i in self.polls:
            if self.polls[i].getTitle()== title:
                return self.polls[i]
    def getAll(self):
        return self.polls
    def getState(self,state):
        for item in self.polls:
            print(item.getState())
        print("----") 
        statePolls = []
        i=0
        while(i < len(self.polls)):
            if self.polls[i].getState() == state:
                statePolls.append(self.polls[i])
            i=i+1
        return statePolls

    def getCount(self):
        return len(self.polls)
    def isEmpty(self):
        if len(self.polls) == 0:
            return True
        else:
            return False





app = Flask(__name__)#-------> Main de la aplicación

app.config['MYSQL_HOST']='103.195.100.230'
app.config['MYSQL_USER']='jookeezc_alejandro'
app.config['MYSQL_PASSWORD']='is2_gonzal0'
app.config['MYSQL_DB']='jookeezc_encuesta'
mysql = MySQL(app)



# Se inicializa el almacen de encuestas
polls=SystemPoll()

poll1=Poll(1)#-------> Encuesta de prueba
poll1.addTitle("Segunda Encuesta presidencial 2026")
poll1.addDescription("resultados de vocaciones año 2026")
poll1.setState(1)
polls.addPoll(poll1)

poll2=Poll(2)#-------> Encuesta de prueba
poll2.addTitle("Primera Encuesta presidencial 2026")
poll2.addDescription("resultados de vocaciones año 2026")
poll2.setState(2)
polls.addPoll(poll1)

poll3=Poll(3)#-------> Encuesta de prueba
poll3.addTitle("Encuesta presidencial 2021")
poll3.addDescription("resultados de vocaciones año 2026")
poll3.setState(3)
polls.addPoll(poll1)

#-------> Aca deberia estar la query de la base de datos
#SELECT E.id_encuesta,E.nombre,E.descripcion FROM Encuestas as E


@app.route("/")
def home():#----> pagina home
    return render_template('index.html')


@app.route("/encuestas")
def encuestas():#----> pagina
    
    return render_template("encuestas.html",
        polls=polls.getAll())

@app.route("/nueva_encuesta")
def nueva_encuesta():
    return render_template("nueva_encuesta.html")

@app.route("/crear_encuesta", methods=['POST'])
def crear_encuesta():
    if request.method =='POST':
        title=request.form['title']
        des=request.form['description']
        print("Ingresar en base de datos "+title+" y "+ des+".")

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Encuestas (nombre, descripcion) VALUES (%s,%s)",(title,des))
        mysql.connection.commit()
        newpoll=Poll(polls.getCount()+1)
        newpoll.addTitle(title)
        newpoll.addDescription(des)
        polls.addPoll(newpoll)
    return redirect(url_for('encuestas'))
@app.route("/editar_encuesta", methods=['POST'])
def editar_encuesta():
    if request.method =='POST':
        True
        code=request.form['code']
        #title=request.form['title']
        #des=request.form['description']
        newpoll=polls.getPollcode(code)
        print(newpoll)
    return render_template("editar_encuesta.html")
@app.route('/encuestados')
def encuestados():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Encuestados')
    data = cur.fetchall()
    return render_template("encuestados.html", encuestados = data)#'encuestados'

@app.route('/nuevo_enc', methods=['POST'])
def nuevo_enc():
    if request.method == 'POST':
        correo = request.form['correo']
        nombre = request.form['nombre']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO Encuestados (correo,nombre) VALUES (%s,%s)',(correo,nombre))
        mysql.connection.commit()
    return redirect(url_for('encuestados'))

    
@app.route('/editar_encuestado/<email>')
def get_encuestado(email):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Encuestados WHERE correo = %s', [email])
    data = cur.fetchall()
    return render_template('e-encuestado.html', encuestado = data[0])

@app.route('/eliminar_encuestado/<email>')
def elim_encuestado(email):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Encuestados WHERE correo = %s',[email])
    mysql.connection.commit()
    return redirect(url_for('encuestados'))
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/sigin")
def sigin():
    return render_template("sigin.html")

@app.route('/eliminar_encuesta/<num>')
def eliminar_encuesta(num):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Encuestas WHERE id_encuesta = %s',[num])
    mysql.connection.commit()
    return redirect(url_for('encuestas'))
