from flask import Flask, request
import mysql.connector
from urllib.parse import urlparse

app = Flask(__name__)

def get_db():
    url = "mysql://root:kCpZknHrbmtmexzErrsBJXlbyvkuuqKb@roundhouse.proxy.rlwy.net:28464/railway"
    result = urlparse(url)

    return mysql.connector.connect(
        host=result.hostname,
        user=result.username,
        password=result.password,
        port=result.port,
        database=result.path.lstrip("/")
    )

STYLE = """
<style>
body {
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    margin: 0;
    padding: 0;
}

.container {
    background: white;
    width: 400px;
    margin: 60px auto;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.2);
}

h2 {
    margin-bottom: 20px;
    color: #333;
}

input, select {
    width: 100%;
    padding: 10px;
    margin: 8px 0;
    border-radius: 8px;
    border: 1px solid #ccc;
    outline: none;
    transition: 0.3s;
}

input:focus, select:focus {
    border-color: #007BFF;
}

button {
    width: 100%;
    padding: 12px;
    background: #007BFF;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    transition: 0.3s;
}

button:hover {
    background: #0056b3;
}

a {
    display: block;
    margin-top: 15px;
    color: #007BFF;
    text-decoration: none;
}

table {
    margin: 40px auto;
    border-collapse: collapse;
    width: 80%;
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
}

th {
    background: #007BFF;
    color: white;
}

td, th {
    padding: 12px;
    text-align: center;
}

tr:nth-child(even) {
    background: #f2f2f2;
}
</style>
"""

@app.route("/", methods=["GET"])
def home():
    return STYLE + '''
    <div class="container">
        <h2>BIENVENU A LA COLLECTE DE DONNEE ACADEMIQUE DE L'UNIVERSITE DE YAOUNDE 1</h2>

        <form action="/submit" method="POST">
            <input name="matricule" placeholder="Matricule" required>
            <input name="nom" placeholder="Nom" required>

            <select name="filiere">
                <option>Informatique</option>
                <option>Mathématiques</option>
                <option>Physique</option>
                <option>Droit</option>
                <option>Biologie</option>
                <option>Chimie</option>
                <option>ICT</option>
                <option>Géoscience</option>
            </select>

            <select name="niveau">
                <option>Licence</option>
                <option>Master</option>
                <option>Doctorat</option>
            </select>

            <input name="mgp" type="float" placeholder="mgp" required>

            <button type="submit">Enregistrer</button>
        </form>

        <a href="/data">Voir données</a>
    </div>
    '''

@app.route("/submit", methods=["POST"])
def submit():
    db = get_db()
    cursor = db.cursor()

    matricule = request.form["matricule"]
    nom = request.form["nom"]
    filiere = request.form["filiere"]
    note = request.form["mgp"]
    niveau = request.form["niveau"]

    sql = "INSERT INTO students (matricule, nom, filiere, note, niveau) VALUES (%s, %s, %s, %s, %s)"
    values = (matricule, nom, filiere, note, niveau)

    cursor.execute(sql, values)
    db.commit()

    return STYLE + "<div class='container'><h3>✔️Enregistré</h3><a href='/'>Retour</a></div>"

@app.route("/data")
def data():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT matricule, nom, filiere, note, niveau FROM students")
    rows = cursor.fetchall()

    table = ""
    for r in rows:
        table += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"

    return STYLE + f"""
    <h2 style="text-align:center;">Étudiants</h2>
    <table>
        <tr>
            <th>Matricule</th>
            <th>Nom</th>
            <th>Filière</th>
            <th>Mgp</th>
            <th>Niveau</th>
        </tr>
        {table}
    </table>
    <br><div style="text-align:center;"><a href="/">Retour</a></div>
    """

if __name__ == "__main__":
    app.run(debug=True)
