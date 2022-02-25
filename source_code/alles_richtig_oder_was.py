import subprocess
from maximize_console import maximize_console
maximize_console(lines=30000)
from satzmetzger.satzmetzger import Satzmetzger
import language_tool_python
import pandas as pd
from pretty_html_table import build_table
import webbrowser
from add_color_print_reg import *
import os
import sys
from bs4 import BeautifulSoup
windowsrechner = os.name == "nt"
tool = language_tool_python.LanguageTool("de-de")
tool.enable_spellchecking()
drucker = Farbprinter()
if windowsrechner:
    add_color_print_to_regedit()


colorfunctions = [
    drucker.f.black.brightyellow.normal,
    drucker.f.black.brightwhite.normal,
]
colorfunctions2 = [drucker.f.black.red.normal, drucker.f.black.brightwhite.normal]

drucker.p_ascii_front_on_flag_with_border(
    text="Alles richtig, oder was?",
    colorfunctions=colorfunctions,
    bordercolorfunction=drucker.f.brightred.brightyellow.negative,
    font="jazmine",
    width=1000,
    offset_from_left_side=5,
    offset_from_text=15,
)
drucker.p_ascii_front_on_flag_with_border(
    text="Made by www.queroestudaralemao.com.br",
    colorfunctions=colorfunctions2,
    bordercolorfunction=drucker.f.red.black.normal,
    font="term",
    width=1000,
    offset_from_left_side=100,
    offset_from_text=15,
)


updates_quero_estudar_alemao()
text = ""
tokenmachen = Satzmetzger()


def text_korrigieren(text):
    einzelnesaetze = tokenmachen.zerhack_den_text(text)
    allekorrekturen = []
    for satz in einzelnesaetze:
        matches = tool.check(satz)
        for match in matches:
            wortmitproblem = match.matchedText
            problembeschreibung = match.message
            vorschlaege = match.replacements
            allekorrekturen.append(
                [
                    satz,
                    wortmitproblem,
                    problembeschreibung,
                    vorschlaege,
                    match.sentence[: match.offset]
                    + match.sentence[match.offset :].strip(),
                ]
            )
            print(
                drucker.f.brightred.black.bold(
                    f'\nAchtung! Bei "{wortmitproblem}" könnte es ein Problem geben\n'
                )
            )
            print("\n")
            try:
                print(
                    drucker.f.black.brightyellow.framed(match.sentence[: match.offset])
                    + drucker.f.brightwhite.brightred.bold("  >>>>")
                    + drucker.f.black.brightyellow.framed(
                        match.sentence[match.offset :].strip()
                    )
                    + "\n",
                    end="",
                )
            except:
                print(match.sentence)
            print("\n")
            print(
                drucker.f.brightyellow.black.framed(
                    f'Wir haben folgendes Problem festgestellt: \n"{problembeschreibung}"\n'
                ),
                end="",
            )
            print(
                drucker.f.brightgreen.black.framed(f"Hier sind ein paar Vorschläge:\n"),
                end="",
            )
            for indi, vorschlag in enumerate(vorschlaege):
                print(
                    drucker.f.cyan.brightwhite.negative(str(indi + 1).zfill(4) + ". "),
                    end="",
                )
                print(drucker.f.cyan.brightwhite.bold(f"{vorschlag}\n"), end="")
            print("\n" * 3)

    df = pd.DataFrame.from_records(allekorrekturen)
    df.columns = [
        "Original",
        "Wort mit Problem",
        "Problembeschreibung",
        "Korrekturen",
        "Wo ist das Problem?",
    ]
    drucker.p_pandas_list_dict(df, linebreak=500)
    html_table_blue_light = build_table(df, "green_dark")

    with open("ergebniss_korrektur.html", "w") as f:
        f.write(html_table_blue_light)
    webbrowser.open("ergebniss_korrektur.html")


def txtdateien_lesen(text):
    try:
        dateiohnehtml = (
                b"""<!DOCTYPE html><html><body><p>""" + text + b"""</p></body></html>"""
        )
        soup = BeautifulSoup(dateiohnehtml, "html.parser")
        soup = soup.text
        return soup.strip()
    except Exception as Fehler:
        print(Fehler)


def get_file_path(datei):
    pfad = sys.path
    pfad = [x.replace('/', '\\') + '\\' + datei for x in pfad]
    exists = []
    for p in pfad:
        if os.path.exists(p):
            exists.append(p)
    return list(dict.fromkeys(exists))


def get_text():
    p = subprocess.run("Everything2TXT.exe", capture_output=True)
    ganzertext = txtdateien_lesen(p.stdout)
    return ganzertext

while True:
    eingabe = input(
        choice(logo_auswahl)(
            f"\nWas möchtest du tun?\n1) Text korrigeren\n2) Programm beenden\n"
        )
    )
    try:
        if str(eingabe) == "1":
            text = get_text()

            text_korrigieren(text)
        elif str(eingabe) == "2":
            print("Programm wird beendet")
            sys.exit()
        else:
            print("Frangen wir noch einmal von vorn an!")
            continue
    except:
        print("Fehler bei der Eingabe! Bitte wiederholen!")


