import json
import os
import re
import walletpass
import pprint
import sys
from aztec_code_generator import AztecCode
from jinja2 import Environment, FileSystemLoader
from zipfile import ZipFile
import base64

jinja_env = Environment(loader=FileSystemLoader('templates'))
jinja_env.globals['render_value'] = walletpass.render_value
jinja_env.globals['render_label'] = walletpass.render_label
jinja_env.globals['barcode_to_svg'] = walletpass.barcode_to_svg

PKPASS_FN = sys.argv[1]
LANG = sys.argv[2]

INPUT_FOLDER = 'samples/1BOD3639/'

with ZipFile(PKPASS_FN) as pkpass_file:
    with pkpass_file.open("pass.json") as pass_json_f:
        pass_json = json.load(pass_json_f)
        pprint.pprint(pass_json)

    # TODO handle eventTicket and storeCard differently
    if 'eventTicket' in pass_json:
        pass_json['generic'] = pass_json['eventTicket']
    if 'storeCard' in pass_json:
        pass_json['generic'] = pass_json['storeCard']

    namelist = pkpass_file.namelist()
    localisation_folders = [ os.path.dirname(f) for f in namelist if os.path.dirname(f).endswith('.lproj') ]

    localisations = {}
    for localisation in localisation_folders:
        localisation_lang = localisation.split('.')[0]
        with pkpass_file.open(f"{localisation}/pass.strings") as localisation_strings_file:
            localisations[localisation_lang] = walletpass.read_pass_strings(localisation_strings_file)

    logo_dataurl = None
    thumbnail_dataurl = None
    if 'logo.png' in namelist:
        # TODO handle different resolutions
        with pkpass_file.open('logo.png') as logo_png:
            logo_dataurl = f"data:image/png;base64,{base64.b64encode(logo_png.read()).decode()}"
    if 'thumbnail.png' in namelist:
        with pkpass_file.open('thumbnail.png') as thumbnail_png:
            thumbnail_dataurl = f"data:image/png;base64,{base64.b64encode(thumbnail_png.read()).decode()}"

    template = jinja_env.get_template('pass.html')
    selected_localisation = {}
    if 'en' in localisations:
        selected_localisation = localisations['en']
    rendered_template = template.render(wallet_pass=pass_json, localisation=selected_localisation, thumbnail=thumbnail_dataurl, logo=logo_dataurl)
    with open('out.html', 'w') as out_html:
        out_html.write(rendered_template)