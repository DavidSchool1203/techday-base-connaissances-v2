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
styles.add(ParagraphStyle(name='GuideSmallWhite', fontName='Guide', fontSize=8.45, leading=10.7, textColor=colors.white))
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

def role_box(draw, x, y, width, height, name, role, color, detail=''):
    draw.rounded_rectangle((x, y, x+width, y+height), radius=22, fill='white', outline=color, width=4)
    draw.rounded_rectangle((x, y, x+width, y+50), radius=22, fill=color)
    draw.rectangle((x, y+25, x+width, y+50), fill=color)
    draw.text((x+16, y+12), name, font=hexfont(23, True), fill='white')
    for i, line in enumerate(wrap(draw, role, width-32, hexfont(17, True))[:2]):
        draw.text((x+16, y+68+i*21), line, font=hexfont(17, True), fill=INK)
    if detail:
        for i, line in enumerate(wrap(draw, detail, width-32, hexfont(15))[:2]):
            draw.text((x+16, y+118+i*19), line, font=hexfont(15), fill=MUTED)

def arrow_path(draw, points, color, width=5):
    for a, b in zip(points, points[1:]):
        draw.line((a, b), fill=color, width=width)
    start, end = points[-2], points[-1]
    angle = atan2(end[1]-start[1], end[0]-start[0])
    length = 19
    a = (end[0]-length*cos(angle-pi/7), end[1]-length*sin(angle-pi/7))
    b = (end[0]-length*cos(angle+pi/7), end[1]-length*sin(angle+pi/7))
    draw.polygon([end, a, b], fill=color)

def dashed_link(draw, start, end, color):
    dx, dy = end[0]-start[0], end[1]-start[1]
    distance = max(1, (dx*dx + dy*dy) ** .5)
    ux, uy = dx/distance, dy/distance
    for n in range(0, int(distance), 20):
        if n % 40 == 0:
            a = (start[0]+ux*n, start[1]+uy*n)
            b = (start[0]+ux*min(n+12, distance), start[1]+uy*min(n+12, distance))
            draw.line((a, b), fill=color, width=3)

def label(draw, x, y, text, color):
    font = hexfont(15, True)
    width = int(draw.textlength(text, font=font)) + 20
    draw.rounded_rectangle((x, y, x+width, y+27), radius=12, fill='white', outline=color, width=2)
    draw.text((x+10, y+5), text, font=font, fill=color)

def story_box(draw, x, y, width, height, name, purpose, action, color):
    draw.rounded_rectangle((x, y, x+width, y+height), radius=22, fill='white', outline=color, width=4)
    draw.rounded_rectangle((x, y, x+width, y+48), radius=22, fill=color)
    draw.rectangle((x, y+25, x+width, y+48), fill=color)
    draw.text((x+16, y+8), name, font=hexfont(28, True), fill='white')
    draw.text((x+16, y+64), 'BUT', font=hexfont(17, True), fill=MUTED)
    for i, line in enumerate(wrap(draw, purpose, width-32, hexfont(20, True))[:1]):
        draw.text((x+16, y+86+i*20), line, font=hexfont(20, True), fill=INK)
    draw.text((x+16, y+117), 'CE QUI A ÉTÉ FAIT', font=hexfont(17, True), fill=MUTED)
    for i, line in enumerate(wrap(draw, action, width-32, hexfont(18))[:2]):
        draw.text((x+16, y+140+i*21), line, font=hexfont(18), fill=INK)

def make_map():
    image = PILImage.new('RGB', (1800, 1350), '#F8FBFD')
    draw = ImageDraw.Draw(image)
    purple = '#7C3AED'
    orange = '#C56A00'
    draw.text((58, 34), 'Vue d ensemble : ce qui a été fait', font=hexfont(42, True), fill=NAVY)
    draw.text((58, 88), 'Chaque carte indique le but de l outil et son rôle dans la construction du projet.', font=hexfont(21), fill=MUTED)
    draw.rounded_rectangle((58, 136, 1742, 194), radius=18, fill='white', outline=LINE, width=2)
    draw.line((90, 165, 155, 165), fill=GREEN, width=6); draw.text((175, 150), 'documents et fiches', font=hexfont(17, True), fill=GREEN)
    dashed_link(draw, (495,165), (560,165), purple); draw.text((580,150), 'travail réalisé avec ChatGPT', font=hexfont(17, True), fill=purple)
    draw.line((1130, 165, 1195, 165), fill=orange, width=6); draw.text((1215, 150), 'clé API privée', font=hexfont(17, True), fill=orange)

    draw.text((70, 238), 'Ce que tu as donné à ChatGPT', font=hexfont(22, True), fill=NAVY)
    draw.text((690, 238), 'Le travail fait avec ChatGPT', font=hexfont(22, True), fill=NAVY)
    draw.text((1400, 238), 'Les résultats et services', font=hexfont(22, True), fill=NAVY)

    story_box(draw, 70, 290, 390, 195, 'Ton objectif', 'Dire ce que doit faire l application.', 'Tu as demandé une base de fiches avec un chatbot.', BLUE)
    story_box(draw, 70, 525, 390, 195, 'base de connaissance.csv', 'Fournir les 147 fiches de départ.', 'Envoyé à ChatGPT pour préparer l import Supabase.', GREEN)
    story_box(draw, 70, 760, 390, 195, 'AGENTS.md', 'Donner les règles du projet.', 'Envoyé à ChatGPT pour guider le travail.', GREEN)
    story_box(draw, 670, 510, 490, 260, 'ChatGPT', 'T aider à construire et comprendre.', 'Lecture des documents, code, Supabase, tests, explications et préparation de GitHub.', purple)
    story_box(draw, 1010, 285, 330, 190, 'Google AI Studio', 'Créer une clé API pour le chatbot.', 'Tu as créé la clé. Elle va dans les secrets Supabase.', orange)
    story_box(draw, 1400, 285, 330, 190, 'Supabase', 'Garder les fiches et la clé API.', 'ChatGPT l a configuré : import des fiches et chatbot.', NAVY)
    story_box(draw, 1400, 525, 330, 195, 'HTML local', 'Afficher les fiches et le chatbot.', 'Créé par ChatGPT. Il lit Supabase et affiche les résultats.', BLUE)
    story_box(draw, 1400, 755, 330, 195, 'GitHub', 'Garder l historique du projet.', 'ChatGPT y a envoyé le code et les documents vérifiés.', GREEN)

    arrow_path(draw, [(460, 380), (670, 570)], purple); label(draw, 485, 425, 'ta demande', purple)
    arrow_path(draw, [(460, 615), (670, 635)], GREEN); label(draw, 490, 575, 'les fiches', GREEN)
    arrow_path(draw, [(460, 850), (670, 710)], GREEN); label(draw, 485, 765, 'les règles', GREEN)
    arrow_path(draw, [(1160, 590), (1280, 590), (1280, 500), (1400, 440)], purple); label(draw, 1190, 545, 'configure + importe', purple)
    arrow_path(draw, [(1160, 645), (1400, 610)], purple); label(draw, 1200, 620, 'crée la page', purple)
    arrow_path(draw, [(1160, 720), (1400, 845)], purple); label(draw, 1190, 755, 'enregistre les versions', purple)
    arrow_path(draw, [(1340, 380), (1400, 380)], orange); label(draw, 1240, 335, 'clé API → secrets', orange)

    draw.rounded_rectangle((70, 1095, 1730, 1240), radius=20, fill='#F1F7FB', outline=LINE, width=2)
    draw.text((100, 1122), 'Quand tu ouvres l application', font=hexfont(20, True), fill=NAVY)
    draw.text((100, 1160), 'HTML local', font=hexfont(18, True), fill=BLUE)
    arrow_path(draw, [(300, 1175), (650, 1175)], BLUE); label(draw, 385, 1138, 'questions et affichage', BLUE)
    draw.text((680, 1160), 'Supabase', font=hexfont(18, True), fill=NAVY)
    arrow_path(draw, [(860, 1175), (1230, 1175)], GREEN); label(draw, 940, 1138, 'fiches et réponses', GREEN)
    draw.text((1260, 1160), 'Chatbot visible dans le HTML', font=hexfont(18, True), fill=BLUE)
    draw.text((100, 1205), 'ChatGPT, GitHub, le CSV et AGENTS.md ont servi à construire le projet : ils ne sont pas utilisés à chaque question.', font=hexfont(16, True), fill=MUTED)
    draw.text((70, 1290), 'La clé API reste dans Supabase. Elle ne se trouve ni dans le fichier HTML, ni dans le CSV, ni dans GitHub.', font=hexfont(17, True), fill=orange)
    image.save(MAP)

def three_column(title_text, request, outcome, check):
    data = [[p('<b>' + title_text + '</b>', 'GuideSmallWhite'), '', ''], [p('<b>Je demande</b><br/>'+request, 'GuideTiny'), p('<b>J obtiens</b><br/>'+outcome, 'GuideTiny'), p('<b>Je vérifie</b><br/>'+check, 'GuideTiny')]]
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
        ('5. Connecter l IA', '« Crée une clé API dans Google AI Studio, puis mets-la dans les secrets Supabase, jamais dans le HTML. »', 'Un chatbot qui utilise la fonction Supabase.', 'Une question retourne une réponse et une source.'),
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
    result = Table([[p('<b>Dans le navigateur</b><br/>Une application locale avec deux onglets : <b>Base de connaissances</b> et <b>Chatbot</b>.','GuideBody'), p('<b>Dans Supabase</b><br/>Les fiches, la fonction du chatbot et la clé API Google gardée secrète.','GuideBody'), p('<b>Dans GitHub</b><br/>Les versions du code et les documents de suivi.','GuideBody')]], colWidths=[59.3*mm]*3)
    result.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),HexColor(PALE_BLUE)),('BACKGROUND',(1,0),(1,0),HexColor(PALE_GREEN)),('BACKGROUND',(2,0),(2,0),HexColor('#F2F4F8')),('GRID',(0,0),(-1,-1),.5,HexColor(LINE)),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),11),('BOTTOMPADDING',(0,0),(-1,-1),11)])); s += [result]
    s += [h('Avant chaque séance',2), bullet('<b>1.</b> Demander un plan avant de demander du code.'), bullet('<b>2.</b> Demander quelles décisions ou questions sont importantes.'), bullet('<b>3.</b> Avancer une étape, vérifier le résultat, puis seulement continuer.'), h('La règle simple',2), p('ChatGPT peut préparer, expliquer, écrire du code et tester. Je garde les décisions, les accès à mes comptes et la vérification finale.')] 
    s.append(PageBreak())
    # Page 2
    s += title('La carte des outils', 'Comprendre les liaisons en un regard')
    s += [Image(str(MAP), width=178*mm, height=133.5*mm), Spacer(1,5), p('<b>Lire la carte :</b> à gauche, ce que tu as donné à ChatGPT. Au centre, ce qu il a fait avec toi. À droite, les outils qu il a configurés ou créés. Les flèches indiquent le lien concret entre eux.', 'GuideSmall'), p('<b>À retenir :</b> ChatGPT est central pendant la construction. Quand tu ouvres ensuite l application, seuls le HTML et Supabase sont utilisés pour afficher les fiches et le chatbot. Google AI Studio a servi à créer la clé API, qui reste dans Supabase.', 'GuideSmall')]
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
    s += [p('Imagine une bibliothèque. Tu poses une question au bibliothécaire. Il cherche des fiches utiles, les donne à l IA Google par l API, puis elle rédige une réponse avec les références trouvées.'), h('Le chemin actuel',2)]
    rag = Table([[p('<b>1. Question</b><br/>Je demande par exemple : « Que sais-tu sur Blender ? »','GuideSmall'),p('<b>2. Recherche</b><br/>Supabase cherche les mots présents dans les fiches.','GuideSmall'),p('<b>3. Lecture</b><br/>L IA Google reçoit au plus 12 fiches trouvées.','GuideSmall'),p('<b>4. Réponse</b><br/>Le chatbot répond et affiche les fiches utilisées.','GuideSmall')]], colWidths=[44.5*mm]*4)
    rag.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),HexColor(PALE_BLUE)),('BACKGROUND',(1,0),(1,0),HexColor(PALE_GREEN)),('BACKGROUND',(2,0),(2,0),HexColor(PALE_BLUE)),('BACKGROUND',(3,0),(3,0),HexColor(PALE_GREEN)),('GRID',(0,0),(-1,-1),.5,HexColor(LINE)),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)])); s += [rag, h('Ce qui fonctionne aujourd hui',2), bullet('Le chatbot répond à partir des fiches trouvées et cite leurs titres.'), bullet('La clé API Google reste dans Supabase. Les URL des fiches ne sont pas envoyées à l IA Google.'), h('Ce qui viendra ensuite : pgvector',2), p('Le RAG actuel cherche surtout les mêmes mots. Avec pgvector, il cherchera aussi le <b>sens</b>. Une question sur « animation 3D » pourra trouver une fiche sur Blender, même si le mot Blender n est pas écrit dans la question.')]
    s.append(PageBreak())
    # Page 6
    s += title('Rendre l outil plus intelligent', 'Les améliorations qui comptent vraiment')
    upgrades = Table([[p('<b>1. Améliorer les fiches</b><br/>Donner un titre, une courte description et des étiquettes cohérentes.','GuideSmall'),p('<b>2. Ajouter pgvector</b><br/>Chercher les fiches par le sens, en plus des mots exacts.','GuideSmall'),p('<b>3. Enrichir avec un agent</b><br/>Compléter une fiche seulement avec une source vérifiable.','GuideSmall')]], colWidths=[59.3*mm]*3)
    upgrades.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),HexColor(PALE_GREEN)),('BACKGROUND',(1,0),(1,0),HexColor(PALE_BLUE)),('BACKGROUND',(2,0),(2,0),HexColor('#F2F4F8')),('GRID',(0,0),(-1,-1),.5,HexColor(LINE)),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)])); s += [upgrades, h('Les outils à utiliser',2)]
    s += three_column('Pour améliorer le RAG', '« Ajoute pgvector. Crée des embeddings pour le titre, le texte et les étiquettes. Combine recherche par mots et recherche par le sens. »', 'Une recherche plus tolérante aux synonymes et aux formulations naturelles.', 'Une question formulée autrement retrouve une fiche pertinente.')
    s += three_column('Pour compléter les fiches', '« Propose un agent qui enrichit une fiche uniquement avec des sources vérifiables et enregistre la source. »', 'Des fiches plus complètes, sans contenu inventé.', 'Chaque ajout indique une source consultable.')
    s += [h('Règle de sécurité',2), p('Une clé API Google est un accès privé. Elle reste dans les secrets Supabase. GitHub reçoit le code, pas les mots de passe ni les clés secrètes.')]
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
