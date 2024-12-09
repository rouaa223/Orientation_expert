import json
from fpdf import FPDF
from flask import Flask, render_template, request, make_response, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'votre_clé_secrète_pour_flash'  # Remplacez par une clé sécurisée


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
        
        # Vérifier les conditions de moyenne, de matières et de secteur
        if (moyenne >= conditions['moyenne_min'] and
            any(matiere in matieres for matiere in conditions['matieres']) and
            (secteur == 'Tout' or secteur in filiere['secteur'])):
            resultats.append(filiere)
            
    return resultats
@app.route('/orientation')
def orientation():
    return render_template('orientation.html')

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

# Route pour générer le PDF
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Récupérer les choix du formulaire
    choix = [request.form[f'choix{i}'] for i in range(1, 7)]

    # Créer un PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Vos Choix d'Orientation", ln=True, align='C')
    pdf.ln(10)

    for index, choix_item in enumerate(choix, start=1):
        pdf.cell(200, 10, txt=f"Choix {index}: {choix_item}", ln=True, align='L')

    # Créer la réponse pour télécharger le PDF
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=choix_orientation.pdf'

    return response

if __name__ == '__main__':
    app.run(debug=True)
