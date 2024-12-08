from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Charger la base des règles
def charger_regles():
    with open('rules.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Fonction pour appliquer les règles (sans le niveau d'études)
def consulter_filiere(moyenne, matieres, secteur):
    regles = charger_regles()
    resultats = []
    
    for filiere in regles:
        conditions = filiere['conditions']
        
        # Vérifier les conditions de moyenne, de matières, de région et de secteur
        if (moyenne >= conditions['moyenne_min'] and
            any(matiere in matieres for matiere in conditions['matieres']) and
            (secteur == 'Tout' or secteur in filiere['secteur'])):
            resultats.append(filiere)
            
    return resultats

# Route pour afficher le formulaire
@app.route('/')
def index():
    return render_template('index.html')

# Route pour traiter le formulaire et afficher les résultats
@app.route('/obtenir_resultats', methods=['POST'])
def obtenir_resultats():
    # Récupérer les données du formulaire
    moyenne = float(request.form['moyenne'])
    matieres = request.form.getlist('matieres')
    secteur = request.form['secteur']
    
    # Appliquer les règles pour obtenir les résultats
    resultats = consulter_filiere(moyenne, matieres, secteur)
    
    return render_template('resultats.html', resultats=resultats)

if __name__ == '__main__':
    app.run(debug=True)
