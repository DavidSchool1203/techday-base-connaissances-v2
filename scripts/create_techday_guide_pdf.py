from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'Guide_TechDay_base_connaissances.pdf'
DIAGRAM = ROOT / 'docs' / 'architecture_techday.png'
NAVY = '#0B1F3A'; BLUE = '#146C94'; TEAL = '#0F8A8A'; PALE = '#EAF4F8'; INK = '#1F2937'; MUTED = '#5B6775'; LINE = '#C9D8E1'

pdfmetrics.registerFont(TTFont('Aptos', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('AptosBold', 'C:/Windows/Fonts/arialbd.ttf'))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleTech', fontName='AptosBold', fontSize=27, leading=32, textColor=HexColor(NAVY), spaceAfter=8))
styles.add(ParagraphStyle(name='Sub', fontName='Aptos', fontSize=11.5, leading=15, textColor=HexColor(MUTED), spaceAfter=17))
styles.add(ParagraphStyle(name='H1Tech', fontName='AptosBold', fontSize=17, leading=21, textColor=HexColor(NAVY), spaceBefore=13, spaceAfter=7, keepWithNext=True))
styles.add(ParagraphStyle(name='H2Tech', fontName='AptosBold', fontSize=11.5, leading=14, textColor=HexColor(BLUE), spaceBefore=10, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name='BodyTech', fontName='Aptos', fontSize=9.6, leading=13.1, textColor=HexColor(INK), spaceAfter=6))
styles.add(ParagraphStyle(name='Small', fontName='Aptos', fontSize=8.5, leading=11.1, textColor=HexColor(INK)))
styles.add(ParagraphStyle(name='BulletTech', fontName='Aptos', fontSize=9.6, leading=12.5, textColor=HexColor(INK), leftIndent=12, firstLineIndent=-8, spaceAfter=3))
styles.add(ParagraphStyle(name='QuoteTech', fontName='Aptos', fontSize=15, leading=21, textColor=HexColor(TEAL), italic=True, spaceBefore=16, spaceAfter=14))

def P(text, style='BodyTech'):
    return Paragraph(text, styles[style])

def bullet(text):
    return Paragraph('• ' + text, styles['BulletTech'])

def heading(text, level=1):
    return P(text, 'H1Tech' if level == 1 else 'H2Tech')

def title(text, sub):
    return [P(text, 'TitleTech'), P(sub, 'Sub')]

def prompt_card(step, request, result):
    data = [
        [P('<b>' + step + '</b>', 'Small')],
        [P('<b>Demande à formuler</b><br/>' + request, 'Small')],
        [P('<b>Résultat attendu</b><br/>' + result, 'Small')],
    ]
    t = Table(data, colWidths=[178*mm], hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),HexColor(TEAL)), ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('BACKGROUND',(0,1),(-1,1),HexColor(PALE)), ('BACKGROUND',(0,2),(-1,2),colors.white),
        ('BOX',(0,0),(-1,-1),0.6,HexColor(LINE)), ('INNERGRID',(0,0),(-1,-1),0.3,HexColor(LINE)),
        ('LEFTPADDING',(0,0),(-1,-1),9), ('RIGHTPADDING',(0,0),(-1,-1),9), ('TOPPADDING',(0,0),(-1,-1),7), ('BOTTOMPADDING',(0,0),(-1,-1),7),
    ]))
    return [t, Spacer(1, 7)]

def role_table():
    rows = [[P('<b>Élément</b>','Small'), P('<b>Rôle</b>','Small'), P('<b>Lien principal</b>','Small')]]
    values = [
        ('HTML', 'La page locale visible dans le navigateur.', 'Lit les fiches et envoie les questions.'),
        ('CSV', 'La source de départ des fiches.', 'Est importé dans Supabase sans modifier l original.'),
        ('Supabase', 'La base de données et le serveur du chatbot.', 'Conserve fiches, secrets et fonction Edge.'),
        ('Google AI Studio', 'Crée la clé Gemini.', 'La clé est stockée dans les secrets Supabase.'),
        ('Gemini', 'Formule une réponse à partir du contexte.', 'Reçoit les fiches sélectionnées, sans URL.'),
        ('AGENTS.md', 'Mémoire et règles du projet.', 'Cadre les demandes et les décisions.'),
        ('GitHub', 'Historique des versions du code.', 'Reçoit le code et les documents sans secrets.'),
        ('ChatGPT', 'Aide à concevoir, coder et expliquer.', 'Lit AGENTS.md et suit les demandes.'),
    ]
    for row in values:
        rows.append([P(x,'Small') for x in row])
    t = Table(rows, colWidths=[29*mm, 68*mm, 81*mm], repeatRows=1)
    commands = [('BACKGROUND',(0,0),(-1,0),HexColor(NAVY)),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),0.45,HexColor(LINE)),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]
    for i in range(1,len(rows)):
        if i % 2 == 0: commands.append(('BACKGROUND',(0,i),(-1,i),HexColor(PALE)))
    t.setStyle(TableStyle(commands)); return t

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(HexColor(LINE)); canvas.setLineWidth(.4); canvas.line(18*mm, 13*mm, 192*mm, 13*mm)
    canvas.setFont('Aptos', 7.5); canvas.setFillColor(HexColor(MUTED))
    canvas.drawString(18*mm, 8*mm, 'TechDay  |  Guide de réalisation de la base de connaissances')
    canvas.drawRightString(192*mm, 8*mm, f'Page {doc.page}')
    canvas.restoreState()

def build():
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=16*mm, rightMargin=16*mm, topMargin=16*mm, bottomMargin=19*mm, title='Guide TechDay Base de connaissances', author='DavidSchool1203')
    story = []
    # 1
    story += title('Mes notes de départ', 'TechDay  |  Construire une base de connaissances avec un chatbot')
    story += [P('« Donc j avais écrit avec des dessins le but de ce travail. »', 'QuoteTech'), heading('Le but reconstitué')]
    story += [P('Créer une application locale simple à ouvrir dans un navigateur. Elle sert à consulter une base de connaissances personnelle et à poser des questions à un chatbot qui répond à partir de cette base.')]
    story += [bullet('<b>Interface locale :</b> une page HTML avec un onglet fiches et un onglet chatbot.'), bullet('<b>Données organisées :</b> un CSV de départ importé dans une table Supabase.'), bullet('<b>IA utile :</b> Gemini répond après avoir reçu les fiches pertinentes.'), bullet('<b>Mémoire du projet :</b> AGENTS.md garde les règles et GitHub garde les versions.')]
    story += [heading('Phrase de départ à donner à ChatGPT',2), P('« Je veux une application HTML locale pour consulter ma base de connaissances et poser des questions à un chatbot. Les données sont dans Supabase, la clé Gemini reste dans Supabase, et GitHub sert à conserver l historique du code. Explique-moi les étapes simplement. »')]
    story.append(PageBreak())
    # 2
    story += title('Vue d ensemble du système', 'Les outils et leurs liaisons')
    story += [Image(str(DIAGRAM), width=178*mm, height=108*mm), Spacer(1,5), P('<i>Architecture actuelle de l application TechDay</i>', 'Small'), Spacer(1,7), P('Le navigateur lit les fiches depuis Supabase. Quand une question est posée, il appelle une fonction Supabase. Cette fonction sélectionne des fiches pertinentes puis demande à Gemini de rédiger une réponse. La clé Gemini ne passe jamais dans le navigateur.')]
    story.append(PageBreak())
    # 3
    story += title('Rôle de chaque élément', 'Comprendre ce qui sert à quoi')
    story += [role_table(), Spacer(1,9), heading('Règle essentielle',2), P('La clé Gemini est secrète. Elle ne doit jamais être collée dans le fichier HTML, dans le CSV ou dans GitHub. Le navigateur ne contient qu une clé Supabase publishable, conçue pour être visible côté application.')]
    story.append(PageBreak())
    # 4
    story += title('Étape 1  Clarifier le projet', 'Partir d une demande claire et d une mémoire durable')
    story += [P('Avant de créer du code, il faut définir ce que l outil doit faire, où les données vivent et où les secrets restent cachés. AGENTS.md sert de mémoire : il évite d oublier les règles importantes à la prochaine séance.')]
    story += prompt_card('1. Créer la règle de travail', '« Crée un AGENTS.md en français. Il doit rappeler que le CSV original ne doit pas être modifié, que les clés secrètes ne vont jamais dans GitHub, et que chaque étape vérifiée doit être notée dans JOURNAL.md et ROADMAP.md. »', 'Un fichier de règles court, lisible et réutilisable à chaque séance.')
    story += prompt_card('2. Décrire le résultat attendu', '« Je veux une page HTML locale avec deux onglets : Base de connaissances et Chatbot. Supabase contient les fiches. Gemini répond à partir des fiches. GitHub conserve le code. »', 'Une architecture simple : interface, données, IA et historique sont séparés.')
    story += [heading('Pourquoi cette étape est utile',2), P('Une demande précise évite que l application mélange les clés, les données et le code. Elle indique aussi ce qui doit rester local, public ou secret.')]
    story.append(PageBreak())
    # 5
    story += title('Étape 2  Préparer les données', 'Respecter le CSV et structurer Supabase')
    story += prompt_card('3. Analyser le fichier de départ', '« Analyse le CSV Base de connaissance sans le modifier. Indique le nombre de lignes, les colonnes, les lignes vides et les champs manquants. Prépare un plan d import dans Supabase. »', 'Un inventaire clair. Ici, la table contient 147 fiches, dont certaines sont incomplètes ou sans titre.')
    story += prompt_card('4. Créer la table', '« Crée dans Supabase une table base_connaissances avec les colonnes du CSV. Garde l identifiant de chaque fiche et active RLS. N efface aucune donnée existante. »', 'Une table qui reçoit les fiches et peut évoluer plus tard.')
    story += [heading('Résultat actuel',2), bullet('Les 147 fiches du CSV sont dans Supabase.'), bullet('L application les affiche en lecture seule.'), bullet('Les fiches sans titre restent visibles comme « Fiche sans titre » : elles ne sont pas supprimées.'), bullet('La recherche de la page HTML cherche dans les titres, notes, textes et étiquettes.')]
    story.append(PageBreak())
    # 6
    story += title('Étape 3  Construire l interface HTML', 'Créer une application locale simple')
    story += prompt_card('5. Créer la page', '« Crée un index.html moderne et lisible. Il doit se connecter à Supabase avec une clé publishable, afficher les fiches, proposer une recherche exacte et avoir un deuxième onglet Chatbot. Il ne doit contenir aucune clé Gemini. »', 'Une page autonome ouverte localement dans un navigateur.')
    story += [P('La page HTML est le comptoir de l application : elle affiche les données et transmet la question au serveur Supabase. Elle ne répond pas elle-même avec de l IA.'), heading('Connexion ou pas',2), P('Le choix actuel est une consultation sans connexion. Cela rend les fiches accessibles en lecture à toute personne qui peut atteindre le projet Supabase. Si les fiches deviennent sensibles, la bonne demande à formuler est : « Remets une connexion Supabase et autorise seulement mon compte à lire les fiches. »')]
    story.append(PageBreak())
    # 7
    story += title('Le chatbot RAG', 'Étape 4  Faire répondre l IA à partir des fiches')
    story += [P('<b>RAG</b> signifie Retrieval Augmented Generation. En français : le chatbot cherche d abord des documents, puis il donne ces documents à l IA pour rédiger une réponse. Cela limite les réponses inventées et permet d afficher les sources.')]
    story += prompt_card('6. Créer la fonction chatbot', '« Crée une Edge Function Supabase chat-with-knowledge. Elle reçoit une question, cherche des fiches pertinentes dans base_connaissances, en transmet au maximum 12 à Gemini et retourne une réponse en français avec la liste des fiches utilisées. N envoie pas les URL à Gemini. Utilise le secret API_1. »', 'Un chatbot côté serveur : la clé Gemini ne quitte pas Supabase et la réponse garde une trace des fiches utilisées.')
    story += [heading('Le RAG actuel',2), bullet('<b>Recherche :</b> les mots de la question sont comparés aux textes des fiches.'), bullet('<b>Contexte :</b> au plus 12 fiches correspondantes sont données à Gemini.'), bullet('<b>Réponse :</b> Gemini formule une réponse courte et indique les fiches utilisées.'), bullet('<b>Limite :</b> une question formulée avec des mots très différents peut ne pas trouver la bonne fiche.')]
    story.append(PageBreak())
    # 8
    story += title('Étape 5  Créer et protéger la clé Gemini', 'Google AI Studio puis secrets Supabase')
    story += prompt_card('7. Préparer la clé', '« Explique-moi comment créer une clé Gemini dans Google AI Studio, puis comment la stocker dans les secrets Supabase avec le nom API_1. Ne me demande jamais de la coller dans le HTML ou dans GitHub. »', 'Une clé créée dans Google AI Studio et conservée uniquement par Supabase.')
    story += [heading('Pourquoi passer par Supabase',2), P('Si la clé est placée dans le HTML, toute personne qui ouvre la page peut la récupérer et utiliser ton quota. Dans une Edge Function, la clé reste côté serveur. Le navigateur demande seulement une réponse au chatbot.'), heading('Outils IA à connaître',2)]
    ai_rows = [[P('<b>Outil</b>','Small'),P('<b>À quoi il sert</b>','Small'),P('<b>Quand le demander</b>','Small')], [P('Gemini API','Small'),P('Rédiger une réponse ou produire des résumés.','Small'),P('Quand les fiches utiles ont déjà été trouvées.','Small')], [P('Edge Function Supabase','Small'),P('Exécuter du code côté serveur et accéder au secret API_1.','Small'),P('Quand une action nécessite une clé secrète.','Small')], [P('pgvector','Small'),P('Comparer le sens des textes avec des vecteurs.','Small'),P('Quand la recherche par mots devient insuffisante.','Small')], [P('Plugin ou connecteur','Small'),P('Relier un outil externe à l assistant.','Small'),P('Seulement lorsqu un service extérieur est nécessaire.','Small')]]
    ai = Table(ai_rows, colWidths=[39*mm,71*mm,68*mm], repeatRows=1); ai.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor(NAVY)),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.45,HexColor(LINE)),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('BACKGROUND',(0,2),(-1,2),HexColor(PALE)),('BACKGROUND',(0,4),(-1,4),HexColor(PALE))])); story.append(ai)
    story.append(PageBreak())
    # 9
    story += title('Rendre l IA plus performante', 'Passer du RAG simple au RAG par le sens')
    story += [heading('1. Améliorer les fiches avant tout',2), bullet('Donner un titre clair à chaque fiche, même lorsqu elle contient seulement une URL.'), bullet('Ajouter une phrase qui explique la valeur de la ressource.'), bullet('Utiliser des étiquettes cohérentes : IA, logiciel, matériel, artiste, tutoriel.'), bullet('Repérer les doublons et les fiches vides, mais conserver le CSV original intact.'), heading('2. Ajouter la recherche par le sens',2), P('Avec pgvector, chaque fiche reçoit une représentation numérique de son sens, appelée embedding. Une question comme « animation 3D » peut alors trouver une fiche sur Blender même si elle ne contient pas exactement les mêmes mots.')]
    story += prompt_card('8. Demande pour la version suivante', '« Ajoute pgvector dans Supabase. Crée des embeddings pour le titre, le texte et les étiquettes de chaque fiche. Le chatbot doit combiner recherche par mots et recherche par le sens, puis citer les fiches utilisées. »', 'Un RAG plus tolérant aux synonymes et aux formulations naturelles.')
    story += [heading('3. Ajouter un agent d enrichissement avec prudence',2), P('Un agent peut compléter une fiche en lisant une source fiable. Il doit enregistrer l URL de la source, proposer les informations manquantes et signaler les cas où il ne peut pas vérifier. Il ne doit pas inventer de contenu.')]
    story.append(PageBreak())
    # 10
    story += title('Étape 6  Tester et garder l historique', 'Vérifier avant de publier une version')
    story += prompt_card('9. Tester le système', '« Vérifie que les 147 fiches se chargent, que la recherche exacte fonctionne, que le chatbot répond à une question sur Blender et qu il affiche la source utilisée. Note le résultat dans JOURNAL.md. »', 'Une preuve que la base, le HTML et le chatbot travaillent ensemble.')
    story += prompt_card('10. Envoyer le code dans GitHub', '« Utilise GitHub CLI pour me donner un lien et un code de connexion. Après mon autorisation, crée un commit clair, récupère l historique existant sans rien écraser, puis envoie le code sans force push. »', 'Un dépôt GitHub avec les versions du code et des documents de suivi.')
    story += [heading('Ce qui doit aller dans GitHub',2), bullet('index.html, les fonctions Supabase, les scripts et les documents de suivi.'), bullet('AGENTS.md, JOURNAL.md, ROADMAP.md et DECISIONS.md.'), bullet('Jamais : API_1, mots de passe, clé service_role, export de secrets ou CSV confidentiel.'), heading('Checklist avant la prochaine évolution',2), bullet('Formuler une demande claire et la faire relire par rapport à AGENTS.md.'), bullet('Tester sur une copie ou vérifier les données existantes avant une modification Supabase.'), bullet('Vérifier que la clé API reste dans Supabase.'), bullet('Mettre à jour le journal et envoyer un commit avec un message qui décrit le changement.')]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUT)

if __name__ == '__main__': build()
