from pathlib import Path
from math import atan2, cos, sin, pi
from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'Guide_TechDay_base_connaissances.pdf'
MAP = ROOT / 'docs' / 'carte_outils_techday.png'

NAVY = '#102A43'
BLUE = '#1677B8'
GREEN = '#138A72'
PALE_BLUE = '#EAF5FB'
PALE_GREEN = '#E9F7F2'
INK = '#243B53'
MUTED = '#627D98'
LINE = '#D9E2EC'

pdfmetrics.registerFont(TTFont('Guide', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('GuideBold', 'C:/Windows/Fonts/arialbd.ttf'))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='GuideTitle', fontName='GuideBold', fontSize=27, leading=31, textColor=HexColor(NAVY), spaceAfter=6))
styles.add(ParagraphStyle(name='GuideSub', fontName='Guide', fontSize=12, leading=15, textColor=HexColor(MUTED), spaceAfter=15))
styles.add(ParagraphStyle(name='GuideH1', fontName='GuideBold', fontSize=18, leading=22, textColor=HexColor(NAVY), spaceBefore=10, spaceAfter=6, keepWithNext=True))
styles.add(ParagraphStyle(name='GuideH2', fontName='GuideBold', fontSize=11.5, leading=14, textColor=HexColor(BLUE), spaceBefore=8, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name='GuideBody', fontName='Guide', fontSize=10, leading=13.5, textColor=HexColor(INK), spaceAfter=6))
styles.add(ParagraphStyle(name='GuideSmall', fontName='Guide', fontSize=8.45, leading=10.7, textColor=HexColor(INK)))
styles.add(ParagraphStyle(name='GuideTiny', fontName='Guide', fontSize=7.9, leading=9.7, textColor=HexColor(INK)))
styles.add(ParagraphStyle(name='GuideBullet', fontName='Guide', fontSize=9.8, leading=12.7, textColor=HexColor(INK), leftIndent=12, firstLineIndent=-8, spaceAfter=3))
styles.add(ParagraphStyle(name='GuideQuote', fontName='Guide', fontSize=16, leading=21, textColor=HexColor(GREEN), spaceBefore=15, spaceAfter=14))

def p(text, style='GuideBody'):
    return Paragraph(text, styles[style])

def bullet(text):
    return Paragraph('• ' + text, styles['GuideBullet'])

def title(name, subtitle):
    return [p(name, 'GuideTitle'), p(subtitle, 'GuideSub')]

def h(name, level=1):
    return p(name, 'GuideH1' if level == 1 else 'GuideH2')

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(HexColor(LINE)); canvas.setLineWidth(.4)
    canvas.line(18*mm, 13*mm, 192*mm, 13*mm)
    canvas.setFont('Guide', 7.5); canvas.setFillColor(HexColor(MUTED))
    canvas.drawString(18*mm, 8*mm, 'TechDay  |  Guide personnel pour comprendre et refaire le projet')
    canvas.drawRightString(192*mm, 8*mm, f'Page {doc.page}')
    canvas.restoreState()

def hexfont(size, bold=False):
    path = 'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf'
    return ImageFont.truetype(path, size)

def wrap(draw, text, width, font):
    words = text.split(); rows = []; line = ''
    for word in words:
        next_line = (line + ' ' + word).strip()
        if draw.textlength(next_line, font=font) > width:
            rows.append(line); line = word
        else:
            line = next_line
    if line: rows.append(line)
    return rows

def box(draw, x, y, width, height, heading, receive, send, color):
    draw.rounded_rectangle((x, y, x+width, y+height), radius=20, fill='white', outline=color, width=4)
    draw.rounded_rectangle((x, y, x+width, y+43), radius=20, fill=color)
    draw.rectangle((x, y+22, x+width, y+43), fill=color)
    draw.text((x+15,y+10), heading, font=hexfont(22, True), fill='white')
    draw.text((x+15,y+58), 'Reçoit', font=hexfont(15, True), fill='#627D98')
    lines = wrap(draw, receive, width-30, hexfont(15))
    for i, line in enumerate(lines[:2]): draw.text((x+15,y+78+i*18), line, font=hexfont(15), fill='#243B53')
    draw.text((x+15,y+118), 'Transmet', font=hexfont(15, True), fill='#627D98')
    lines = wrap(draw, send, width-30, hexfont(15))
    for i, line in enumerate(lines[:2]): draw.text((x+15,y+138+i*18), line, font=hexfont(15), fill='#243B53')

def arrow(draw, start, end, color):
    draw.line((start,end), fill=color, width=5)
    angle = atan2(end[1]-start[1], end[0]-start[0])
    length = 20
    a = (end[0]-length*cos(angle-pi/7), end[1]-length*sin(angle-pi/7))
    b = (end[0]-length*cos(angle+pi/7), end[1]-length*sin(angle+pi/7))
    draw.polygon([end,a,b], fill=color)

def make_map():
    image = PILImage.new('RGB', (1600, 920), '#F8FBFD')
    draw = ImageDraw.Draw(image)
    draw.text((60,38), 'Carte des outils', font=hexfont(40, True), fill=NAVY)
    draw.text((60,88), 'Vert : les données. Bleu : la question et la réponse du chatbot.', font=hexfont(21), fill=MUTED)
    box(draw, 65, 225, 275, 180, 'CSV', 'Les fiches de départ', 'Les données à importer', GREEN)
    box(draw, 470, 225, 310, 180, 'Supabase', 'Les fiches et la clé API_1', 'Les fiches ou le contexte du chat', NAVY)
    box(draw, 1030, 225, 310, 180, 'HTML local', 'Les fiches et les réponses', 'Une recherche ou une question', BLUE)
    box(draw, 470, 600, 310, 180, 'Gemini', 'Question et fiches retenues', 'Une réponse avec sources', BLUE)
    box(draw, 1030, 600, 310, 180, 'GitHub', 'Le code et les documents', 'L historique des versions', GREEN)
    # data path
    arrow(draw, (340,315),(470,315),GREEN)
    arrow(draw, (780,315),(1030,315),GREEN)
    # RAG path
    arrow(draw, (1030,365),(780,365),BLUE)
    arrow(draw, (625,405),(625,600),BLUE)
    arrow(draw, (780,690),(1030,690),BLUE)
    draw.text((360,280),'import',font=hexfont(17,True),fill=GREEN)
    draw.text((820,280),'lecture',font=hexfont(17,True),fill=GREEN)
    draw.text((825,390),'question',font=hexfont(17,True),fill=BLUE)
    draw.text((640,500),'fiches retenues',font=hexfont(17,True),fill=BLUE)
    draw.text((805,660),'réponse et sources',font=hexfont(17,True),fill=BLUE)
    # outer tools
    draw.rounded_rectangle((75,485,340,570), radius=15, fill='#EEF3F7', outline='#B8C7D5', width=2)
    draw.text((92,500),'AGENTS.md',font=hexfont(20,True),fill=NAVY)
    draw.text((92,530),'Les règles et la mémoire du projet.',font=hexfont(15),fill=INK)
    draw.rounded_rectangle((1020,485,1350,570), radius=15, fill='#EEF3F7', outline='#B8C7D5', width=2)
    draw.text((1038,500),'ChatGPT',font=hexfont(20,True),fill=NAVY)
    draw.text((1038,530),'Aide à planifier, expliquer et coder.',font=hexfont(15),fill=INK)
    image.save(MAP)

def three_column(title_text, request, outcome, check):
    data = [[p('<b>' + title_text + '</b>', 'GuideSmall'), '', ''], [p('<b>Je demande</b><br/>'+request, 'GuideTiny'), p('<b>J obtiens</b><br/>'+outcome, 'GuideTiny'), p('<b>Je vérifie</b><br/>'+check, 'GuideTiny')]]
    table = Table(data, colWidths=[59.3*mm,59.3*mm,59.4*mm])
    table.setStyle(TableStyle([
        ('SPAN',(0,0),(-1,0)), ('BACKGROUND',(0,0),(-1,0),HexColor(NAVY)), ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('BACKGROUND',(0,1),(0,1),HexColor(PALE_BLUE)), ('BACKGROUND',(1,1),(1,1),colors.white), ('BACKGROUND',(2,1),(2,1),HexColor(PALE_GREEN)),
        ('GRID',(0,0),(-1,-1),.4,HexColor(LINE)), ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),7), ('RIGHTPADDING',(0,0),(-1,-1),7), ('TOPPADDING',(0,0),(-1,-1),6), ('BOTTOMPADDING',(0,0),(-1,-1),6),
    ]))
    return [table, Spacer(1,7)]

def six_steps():
    steps = [
        ('1. Définir le but', '« Crée un plan et pose-moi les questions importantes avant de coder. »', 'Un objectif clair et les décisions à prendre.', 'Je comprends le but en une phrase.'),
        ('2. Lire le CSV', '« Analyse le CSV sans le modifier. Compte les lignes et les champs manquants. »', 'Un inventaire des données à importer.', 'Le CSV original reste intact.'),
        ('3. Organiser Supabase', '« Crée ou vérifie la table de fiches. Ne supprime aucune donnée. »', 'Une table prête à recevoir les fiches.', 'Les 147 fiches sont présentes.'),
        ('4. Créer le HTML', '« Crée une page avec Base de connaissances et Chatbot. »', 'Une application locale simple à ouvrir.', 'Les fiches s affichent et se filtrent.'),
        ('5. Connecter l IA', '« Mets la clé Gemini dans les secrets Supabase, jamais dans le HTML. »', 'Un chatbot qui utilise la fonction Supabase.', 'Une question retourne une réponse et une source.'),
        ('6. Tester et garder une version', '« Teste le parcours puis crée un commit clair et envoie-le sur GitHub. »', 'Une version vérifiée dans l historique.', 'GitHub contient le dernier commit.'),
    ]
    story=[]
    for step in steps: story += three_column(*step)
    return story

def copyable_prompt(label, text):
    t = Table([[p('<b>'+label+'</b><br/>'+text,'GuideSmall')]], colWidths=[178*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),HexColor(PALE_BLUE)),('BOX',(0,0),(-1,-1),.5,HexColor(LINE)),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    return [t, Spacer(1,6)]

def build():
    make_map()
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=16*mm, rightMargin=16*mm, topMargin=16*mm, bottomMargin=19*mm, title='Guide TechDay pour débuter', author='DavidSchool1203')
    s=[]
    # Page 1
    s += title('Mon projet TechDay', 'Un guide personnel pour comprendre le système et savoir quoi demander')
    s += [p('« Je veux consulter mes fiches et interroger un chatbot qui répond à partir de ma base. »', 'GuideQuote'), h('Le résultat visible')]
    result = Table([[p('<b>Dans le navigateur</b><br/>Une application locale avec deux onglets : <b>Base de connaissances</b> et <b>Chatbot</b>.','GuideBody'), p('<b>Dans Supabase</b><br/>Les fiches, la fonction du chatbot et la clé Gemini gardée secrète.','GuideBody'), p('<b>Dans GitHub</b><br/>Les versions du code et les documents de suivi.','GuideBody')]], colWidths=[59.3*mm]*3)
    result.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),HexColor(PALE_BLUE)),('BACKGROUND',(1,0),(1,0),HexColor(PALE_GREEN)),('BACKGROUND',(2,0),(2,0),HexColor('#F2F4F8')),('GRID',(0,0),(-1,-1),.5,HexColor(LINE)),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),11),('BOTTOMPADDING',(0,0),(-1,-1),11)])); s += [result]
    s += [h('Avant chaque séance',2), bullet('<b>1.</b> Demander un plan avant de demander du code.'), bullet('<b>2.</b> Demander quelles décisions ou questions sont importantes.'), bullet('<b>3.</b> Avancer une étape, vérifier le résultat, puis seulement continuer.'), h('La règle simple',2), p('ChatGPT peut préparer, expliquer, écrire du code et tester. Je garde les décisions, les accès à mes comptes et la vérification finale.')] 
    s.append(PageBreak())
    # Page 2
    s += title('La carte des outils', 'Comprendre les liaisons en un regard')
    s += [Image(str(MAP), width=178*mm, height=102.35*mm), Spacer(1,5), p('<b>Le chemin des données :</b> CSV → Supabase → HTML.<br/><b>Le chemin du chatbot :</b> HTML → Supabase → Gemini → HTML.', 'GuideSmall'), h('Ce que chaque outil apporte',2), p('Le CSV apporte le contenu de départ. Supabase garde les données et protège la clé Gemini. Le HTML est l écran que tu utilises. Gemini écrit la réponse. GitHub mémorise les versions. AGENTS.md rappelle les règles. ChatGPT t aide à organiser le travail.')] 
    s.append(PageBreak())
    # Page 3
    s += title('Travailler avec ChatGPT', 'Ce qui peut être délégué et ce que je garde en main')
    table = Table([[p('<b>ChatGPT peut</b>','GuideSmall'),p('<b>Je dois</b>','GuideSmall')],[p('• analyser le CSV<br/>• proposer un plan<br/>• créer le HTML et les fonctions<br/>• expliquer les mots techniques<br/>• tester les résultats<br/>• préparer les commits GitHub','GuideSmall'),p('• définir le but<br/>• choisir ce qui est public ou privé<br/>• autoriser les connexions et les envois<br/>• saisir mes mots de passe<br/>• vérifier que le résultat me convient','GuideSmall')]], colWidths=[89*mm,89*mm])
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),HexColor(BLUE)),('BACKGROUND',(1,0),(1,0),HexColor(GREEN)),('TEXTCOLOR',(0,0),(-1,0),colors.white),('BACKGROUND',(0,1),(0,1),HexColor(PALE_BLUE)),('BACKGROUND',(1,1),(1,1),HexColor(PALE_GREEN)),('GRID',(0,0),(-1,-1),.5,HexColor(LINE)),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9)])); s += [table, h('La demande qui évite de se perdre',2), p('« Avant de coder, résume ce que tu as compris, propose les étapes, puis pose-moi seulement les questions qui empêchent d avancer. Explique chaque mot technique simplement. »'), h('Astuce',2), p('Conserver cette demande dans AGENTS.md ou dans ton guide. Elle transforme ChatGPT en guide de projet au lieu de lui demander une solution trop vite.')]
    s.append(PageBreak())
    # Page 4
    s += title('Le parcours en six étapes', 'À chaque étape : je demande, j obtiens, je vérifie')
    s += six_steps()
    s.append(PageBreak())
    # Page 5
    s += title('Comprendre le chatbot RAG', 'Une bibliothèque, pas une réponse inventée')
    s += [p('Imagine une bibliothèque. Tu poses une question au bibliothécaire. Il cherche des fiches utiles, les donne à Gemini, puis Gemini rédige une réponse avec les références trouvées.'), h('Le chemin actuel',2)]
    rag = Table([[p('<b>1. Question</b><br/>Je demande par exemple : « Que sais-tu sur Blender ? »','GuideSmall'),p('<b>2. Recherche</b><br/>Supabase cherche les mots présents dans les fiches.','GuideSmall'),p('<b>3. Lecture</b><br/>Gemini reçoit au plus 12 fiches trouvées.','GuideSmall'),p('<b>4. Réponse</b><br/>Le chatbot répond et affiche les fiches utilisées.','GuideSmall')]], colWidths=[44.5*mm]*4)
    rag.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),HexColor(PALE_BLUE)),('BACKGROUND',(1,0),(1,0),HexColor(PALE_GREEN)),('BACKGROUND',(2,0),(2,0),HexColor(PALE_BLUE)),('BACKGROUND',(3,0),(3,0),HexColor(PALE_GREEN)),('GRID',(0,0),(-1,-1),.5,HexColor(LINE)),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)])); s += [rag, h('Ce qui fonctionne aujourd hui',2), bullet('Le chatbot répond à partir des fiches trouvées et cite leurs titres.'), bullet('La clé Gemini reste dans Supabase. Les URL des fiches ne sont pas envoyées à Gemini.'), h('Ce qui viendra ensuite : pgvector',2), p('Le RAG actuel cherche surtout les mêmes mots. Avec pgvector, il cherchera aussi le <b>sens</b>. Une question sur « animation 3D » pourra trouver une fiche sur Blender, même si le mot Blender n est pas écrit dans la question.')]
    s.append(PageBreak())
    # Page 6
    s += title('Rendre l outil plus intelligent', 'Les améliorations qui comptent vraiment')
    upgrades = Table([[p('<b>1. Améliorer les fiches</b><br/>Donner un titre, une courte description et des étiquettes cohérentes.','GuideSmall'),p('<b>2. Ajouter pgvector</b><br/>Chercher les fiches par le sens, en plus des mots exacts.','GuideSmall'),p('<b>3. Enrichir avec un agent</b><br/>Compléter une fiche seulement avec une source vérifiable.','GuideSmall')]], colWidths=[59.3*mm]*3)
    upgrades.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),HexColor(PALE_GREEN)),('BACKGROUND',(1,0),(1,0),HexColor(PALE_BLUE)),('BACKGROUND',(2,0),(2,0),HexColor('#F2F4F8')),('GRID',(0,0),(-1,-1),.5,HexColor(LINE)),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)])); s += [upgrades, h('Les outils à utiliser',2)]
    s += three_column('Pour améliorer le RAG', '« Ajoute pgvector. Crée des embeddings pour le titre, le texte et les étiquettes. Combine recherche par mots et recherche par le sens. »', 'Une recherche plus tolérante aux synonymes et aux formulations naturelles.', 'Une question formulée autrement retrouve une fiche pertinente.')
    s += three_column('Pour compléter les fiches', '« Propose un agent qui enrichit une fiche uniquement avec des sources vérifiables et enregistre la source. »', 'Des fiches plus complètes, sans contenu inventé.', 'Chaque ajout indique une source consultable.')
    s += [h('Règle de sécurité',2), p('Une clé Gemini est un accès privé. Elle reste dans les secrets Supabase. GitHub reçoit le code, pas les mots de passe ni les clés secrètes.')]
    s.append(PageBreak())
    # Page 7
    s += title('Modèles de demandes', 'Des phrases prêtes à copier pour chaque séance')
    s += copyable_prompt('Demander un plan', '« Voici mon objectif. Avant de coder, propose un plan court avec les résultats à vérifier après chaque étape. »')
    s += copyable_prompt('Faire poser les bonnes questions', '« Avant de commencer, pose-moi les questions qui sont indispensables. Si tu peux vérifier une information dans les fichiers du projet, fais-le sans me le demander. »')
    s += copyable_prompt('Demander une explication simple', '« Explique-moi cette étape comme à un débutant : le but, ce que je dois faire, ce que je dois voir à la fin et pourquoi. »')
    s += copyable_prompt('Demander un test', '« Vérifie le résultat avec un exemple concret, puis explique-moi simplement ce qui fonctionne et ce qui reste à faire. »')
    s += copyable_prompt('Demander une version GitHub', '« Vérifie l état Git, crée un commit avec un message clair et envoie-le sur GitHub sans force push. Dis-moi exactement ce qui a été envoyé. »')
    s += [h('Mon réflexe',2), p('Je commence par le but, je demande le plan, je vérifie un résultat à la fois et je garde une version dans GitHub lorsque tout fonctionne.')] 
    doc.build(s, onFirstPage=footer, onLaterPages=footer)
    print(OUT)

if __name__ == '__main__':
    build()
