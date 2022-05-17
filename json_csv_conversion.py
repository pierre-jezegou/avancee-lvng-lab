import json
import os
from sympy import classify_pde

PATH="./"
SEP = ", "


fichiers = ["patients", "conditions", "allergies", "visites", "prescriptions", "obs_num", "obs_text"]


def INITIALISATION()->None:
    print("Nettoyage de l'espace de travail...")
    for fichier in fichiers:
        if os.path.exists(fichier+".csv"):
            os.remove(fichier+".csv")
    print("\tFichiers supprimés\n")




def JSON_CSV_CONVERTER(json_path:str) -> None:
    print("Début de la conversion")
    with open("Donnes_demo_pharmIA.json", "r") as fichier:
        all_data = json.load(fichier)
        print("\tfichier ouvert")
    # taille_json = len(all_data["entry"])
    for evenement in all_data["entry"]:
        evenement = evenement["resource"]
        if evenement["resourceType"]=="Patient":
            add_patient(evenement)
        elif evenement["resourceType"]=="Condition":
            add_condition(evenement)
        elif evenement["resourceType"]=="AllergyIntolerance":
            add_allergy(evenement)
    return None

def ouverture_fichier(filename:str, path:str =PATH, mode:str="a"):
    return open(PATH+filename, mode)




def add_patient(evenement:dict, IA_mode=False)->None:
    ''' Ajout d'un patient au fichier 'patients.csv' '''
    fichier = ouverture_fichier("patients.csv")
    id = evenement["identifier"][0]["value"]
    family = evenement["name"][0]["family"].lower()
    name = evenement["name"][0]["given"][0].lower()
    gender = evenement["gender"]
    birthDate = evenement["birthDate"]

    if not(IA_mode):
        fichier.write(id +SEP+ family +SEP+ name +SEP+ gender +SEP+ birthDate+"\r")
    fichier.close()
    return None




def add_condition(evenement:dict, IA_mode=False)->None:
    ''' Ajout d'une condition au fichier 'conditions.csv' '''
    fichier = ouverture_fichier("conditions.csv")
    id = evenement["id"][1:]
    condition = evenement["code"]["coding"][0]
    system = condition["system"]
    code = condition["code"]
    display = condition["display"]
    patient = evenement["subject"]["reference"].replace("Patient/i", '')

    if not(IA_mode):
        fichier.write(id +SEP+ patient +SEP+ system +SEP+ code +SEP+ display+"\r")
    fichier.close()
    return None




def add_allergy(evenement:dict, IA_mode=False)->None:
    ''' Ajout d'une allergie au fichier 'allergies.csv' '''
    fichier = ouverture_fichier("allergies.csv")
    id = evenement["id"][1:]
    allergy_type = evenement["type"]
    category = evenement["category"][0]
    description = evenement["code"]["coding"][0]
    code = description["code"]
    display = description["display"]
    ipp = evenement["patient"]["reference"].replace("Patient/i", '')
    iep = evenement["encounter"]["reference"].replace("Encounter/i", '')

    if not(IA_mode):
        fichier.write(id +SEP+ ipp +SEP+ iep +SEP+ code +SEP+ display+"\r")
    fichier.close()
    return None





