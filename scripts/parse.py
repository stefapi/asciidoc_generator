#!/usr/bin/env python3

# Program to parse a docbook file generated by asciidoctor and extract information to inject
# everything into a generated fodt file
# asciidoctor document header is formatted as follow
#
# = Title of the document
# :asciidoctor_directives:
# Author_firstname Lastname <mail@address.com>
# version, date : author_initials | Comment (you may write several lines; one per version)
# :authortile: Title of the Author (CTPO for example)
# :reviewer: Name of reviewer | Title of the reviewer
# :approver: Name of the Approver | Title of the Approver



import sys
import re
import html
import datetime
import xml.etree.ElementTree as ET
from jinja2 import Template

# Récupération des arguments
xml_file = sys.argv[1]
template_file = sys.argv[2]
output_file = sys.argv[3]

# Charger et parser le fichier XML
tree = ET.parse(xml_file)
root = tree.getroot()

# Définir les espaces de noms
namespaces = {'doc': 'http://docbook.org/ns/docbook'}

# Extraire les informations principales
try:
    author_firstname = html.escape(root.find('.//doc:firstname', namespaces).text)
except:
    author_firstname = ''
try:
    author_surname = html.escape(root.find('.//doc:surname', namespaces).text)
except:
    author_surname = ''
try:
    author_email = html.escape(root.find('.//doc:email', namespaces).text)
except:
    author_email = ''
try:
    author_initials = html.escape(root.find('.//doc:authorinitials', namespaces).text)
except:
    author_initials = ''
try:
    title = html.escape(root.find('.//doc:title', namespaces).text)
except:
    title = ''
try:
    subtitle = html.escape(root.find('.//doc:subtitle', namespaces).text)
except:
    subtitle = ''
try:
    date = html.escape(root.find('.//doc:date', namespaces).text)
except:
    title = datetime.datetime.now()


# Fonction pour extraire une valeur basée sur une balise
def extract_field(simpara, field_name):
    for line in simpara.splitlines():
        if line.startswith(f":{field_name}:"):
            return line.split(f":{field_name}:")[1].strip()
    return ''

# Extraire la table de versions depuis simpara
revtable = []
authortitle=''
access_level=''
reviewer=''
reviewertitle=''
approver=''
approvertitle=''
try:
    simpara_content = root.find('.//doc:simpara', namespaces).text

    # Extraire authortitle et reviewer depuis simpara
    try:
        authortitle = html.escape(extract_field(simpara_content, 'authortitle'))
    except:
        pass
    try:
        access_level = html.escape(extract_field(simpara_content, 'access'))
    except:
        pass
    if not access_level:
        access_level='public'
    reviewer_line = extract_field(simpara_content, 'reviewer')
    if reviewer_line:
        reviewer, reviewertitle = [html.escape(s.strip()) for s in reviewer_line.split('|')]
    else:
        reviewer, reviewertitle = '', ''

    approver_line = extract_field(simpara_content, 'approver')
    if approver_line:
        approver, approvertitle = [html.escape(s.strip()) for s in approver_line.split('|')]
    else:
        approver, approvertitle = '', ''



    for line in simpara_content.splitlines():
        if line.startswith(':') or not line.strip():
            continue
        try:
            version, rest = line.split(',', 1)
            date, rest = rest.split(':', 1)
            author, comment = rest.split('|', 1)
            revtable.append({
                'version': html.escape(version.strip()),
                'author': html.escape(author.strip()),
                'date': html.escape(date.strip()),
                'comment': html.escape(comment.strip()),
            })
        except ValueError:
            # Si une ligne est mal formée, on l'ignore
            continue
except:
    pass


# Extraire les données depuis <revhistory>
revhistory = root.find('.//doc:revhistory', namespaces)
if revhistory is not None:
    for revision in revhistory.findall('.//doc:revision', namespaces):
        revnumber = html.escape(revision.find('./doc:revnumber', namespaces).text)
        date = html.escape(revision.find('./doc:date', namespaces).text)
        revremark = html.escape(revision.find('./doc:revremark', namespaces).text)
        comment = ' '
        if revremark is None:
            author = html.escape(revision.find('./doc:authorinitials', namespaces).text)
            comment = ''
        else:
            author = html.escape(revremark.strip().split('|',1)[0])
            comment = html.escape(revremark.strip().split('|',1)[1])
        # Ajouter la révision au début du tableau
        revtable.insert(0, {
            'version': revnumber.strip(),
            'author': author,
            'date': date.strip(),
            'comment': comment,
        })
else:
    revnumber=''

# Préparer les données pour le template
context = {
    'title': title,
    'subtitle': subtitle,
    'revision': revnumber,
    'date': date,
    'access': access_level,
    'author': f"{author_firstname} {author_surname}",
    'email': author_email,
    'authorfirstname': author_firstname,
    'authorsurname': author_surname,
    'authorinitials': author_initials,
    'authortitle': authortitle,
    'reviewername': reviewer,
    'reviewertitle': reviewertitle,
    'approvername': approver,
    'approvertitle': approvertitle,
    'revtable': revtable,
}

# Lecture du fichier template
try:
    with open(template_file, 'r', encoding='utf-8') as file:
        template_content = file.read()
except FileNotFoundError:
    print(f"Erreur : le fichier {template_file} n'existe pas.")
    sys.exit(1)


template_content = template_content.replace('{{startrev}}', '{% for revision in revtable %}')
template_content = template_content.replace('{{endrev}}', '{% endfor %}')

template = Template(template_content)

# Rendre le template avec les données
output = template.render(context)

# remplace maintenant toutes les admonestations

def treat_admonest(data, admon, tag, puce, style):
    # Expression régulière pour capturer les blocs <text:p> avec le texte variable
    pattern = (
        fr'<text:p text:style-name="[^"]*">{tag}</text:p>\s*'
        r'<text:p text:style-name="[^"]*">(.*?)</text:p>'
    )

    # Fonction de remplacement
    def replacement(match):
        variable_text = match.group(1)  # Texte variable capturé
        return (
            f'<text:list text:style-name="{puce}">\n'
            '<text:list-item>\n'
            f'<text:p text:style-name="{style}">{admon}<text:line-break/>{variable_text}</text:p>\n'
            '</text:list-item>\n'
            '</text:list>'
        )

    # Remplacer les occurrences
    return re.sub(pattern, replacement, output, re.DOTALL)


output = treat_admonest(output, "Tip", "Tip981267", "Puce_20_Tip", "Tip")
output = treat_admonest(output, "Important", "Important981267", "Puce_20_Important", "Important")
output = treat_admonest(output, "Note", "Note981267", "Puce_20_Note", "Note")
output = treat_admonest(output, "Caution", "Caution981267", "Puce_20_Caution", "Caution")
output = treat_admonest(output, "Warning", "Warning981267", "Puce_20_Warning", "Warning")
output = treat_admonest(output, "", "Informalexample981267", "Puce_20_Informalexample", "Informalexample")

output = re.sub(r".*saut_de_page784567.*", '<text:p text:style-name="Pagebreak"/>', output)

# Écriture du résultat dans le fichier de sortie
try:
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(output)
    print(f"Le fichier résultat a été écrit dans : {output_file}")
except Exception as e:
    print(f"Erreur lors de l'écriture dans le fichier {output_file}: {e}")
    sys.exit(1)

