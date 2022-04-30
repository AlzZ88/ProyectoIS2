from flask import Flask, redirect ,render_template,request,url_for
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST']='103.195.100.230'
app.config['MYSQL_USER']='jookeezc_catalina'
app.config['MYSQL_PASSWORD']='is2_gonzal0'
app.config['MYSQL_DB']='jookeezc_encuesta'
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("index.html")

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

@app.route('/encuestas')
def encuestas():
    return render_template("encuestas.html")#'encuestas' 


@app.route('/crearencuesta')
def crearencuesta():
    return render_template("crearencuesta.html")

app.route('/nuevaEnc',methods=['POST'])
def nuevaEnc():
    if request.method == 'POST':
        tit = request.form['titulo']
        desc = request.form['descripcion']
        print(tit)
        print(desc)
    return render_template("encuestas.html")





if __name__ == '__main__':
    app.run(debug=True)

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
        self.polls.insert(poll);
    def removePoll(self,poll):
        self.polls.remove(poll)
    def getPoll(self,code):
        for i in self.polls:
            if self.polls[i].getCode()== code:
                return self.polls[i]
    def getPoll(self,title):
        for i in self.polls:
            if self.polls[i].getTitle()== title:
                return self.polls[i]

    