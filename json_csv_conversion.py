import json
import os
from sympy import classify_pde
from tqdm import tqdm

PATH="./"
SEP = ", "


fichiers = ["patients", "conditions", "allergies", "visites", "prescriptions", "obs_num", "obs_text", "ref_medications"]


def INITIALISATION() -> None:
    print("Nettoyage de l'espace de travail...")
    for fichier in fichiers:
        if os.path.exists(fichier+".csv"):
            os.remove(fichier+".csv")
    print("\tFichiers supprimés\n")




def JSON_CSV_CONVERTER(json_path:str) -> None:
    assert(os.path.exists(json_path))
    print("Début de la conversion")
    with open(json_path, "r") as fichier:
        all_data = json.load(fichier)
        print("\tFichier ouvert")
    # taille_json = len(all_data["entry"])
    for evenement in all_data["entry"]:
        evenement = evenement["resource"]
        try:
            if evenement["resourceType"]=="Patient":
                __add_patient(evenement)
            elif evenement["resourceType"]=="Condition":
                __add_condition(evenement)
            elif evenement["resourceType"]=="AllergyIntolerance":
                __add_allergy(evenement)
            elif evenement["resourceType"]=="Encounter":
                __add_encounter(evenement)
            elif evenement["resourceType"]=="MedicationRequest":
                __add_prescription(evenement)
            elif evenement["resourceType"]=="Medication":
                __add_medication(evenement)
            elif evenement["resourceType"]=="Observation":
                __add_observation(evenement)
            elif evenement["resourceType"]=="Location":
                i = 1
            elif evenement["resourceType"]=="Organization":
                i = 1
            else:
                print("Cet évènement ne correspond à aucun type connu.")
                print(evenement)
        except KeyError:
            print("error")
    print("\tTraitement terminé")
    return None

def ouverture_fichier(filename:str, path:str =PATH, mode:str="a"):
    return open(PATH+filename, mode)




def __add_patient(evenement:dict, IA_mode=False)->None:
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




def __add_condition(evenement:dict, IA_mode=False)->None:
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




def __add_allergy(evenement:dict, IA_mode=False)->None:
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



def __add_encounter(evenement:dict, IA_mode=False)->None:
    ''' Ajout d'une allergie au fichier 'visites.csv' '''
    fichier = ouverture_fichier("visites.csv")
    id = evenement["id"][1:]
    ipp = evenement["subject"]["reference"].replace("Patient/i", '')
    start = evenement["period"]["start"]
    if evenement["period"].get("end"):
        end = evenement["period"]["end"]
    else:
        end = ""
    status = evenement["status"]
    service_id = evenement["location"]["location"]["reference"][-6:]
    

    if not(IA_mode):
        fichier.write(id +SEP+ ipp +SEP+ start +SEP+ end +SEP+ status +SEP+ service_id+"\r")
    fichier.close()
    return None



def __add_prescription(evenement:dict, IA_mode=False) -> None:
    ''' Ajout d'une allergie au fichier 'prescriptions.csv' '''
    fichier = ouverture_fichier("prescriptions.csv")
    id = evenement["id"][1:]
    date = evenement["dosageInstruction"][0]["timing"]["repeat"]["boundsPeriod"]["start"]
    ipp = evenement["subject"]["reference"].replace("Patient/i", '')
    iep = evenement["encounter"]["reference"].replace("Encounter/i", '')
    medicament = evenement["medicationReference"]["reference"].replace("Medication/i", '')
    amount = evenement["dosageInstruction"][0]["doseAndRate"][0]["doseQuantity"]["value"]
    unit = evenement["dosageInstruction"][0]["doseAndRate"][0]["doseQuantity"]["unit"]
    frequence = evenement["dosageInstruction"][0]["text"]
    si_besoin = evenement["dosageInstruction"][0]["asNeededCodeableConcept"]["text"]
    commentaire = ""
    status = "A valider"
    ip = ""
    appel = ""

    if not(IA_mode):
        fichier.write(id +SEP+ date +SEP+ ipp +SEP+ iep +SEP+ medicament +SEP+ amount +SEP+ unit +SEP+ frequence +SEP+ si_besoin +SEP+ commentaire +SEP+ status +SEP+ ip +SEP+ appel+"\r")
    fichier.close()
    return None


def __add_observation(evenement:dict, IA_mode=False) -> None:
    ''' Ajout d'une allergie au fichier 'obs_num.csv' '''
    
    observation_type = evenement["code"]["coding"][0]["code"]
    if observation_type == "Commentaire IDE":
        fichier = ouverture_fichier("obs_text.csv")
        ipp = evenement["subject"]["reference"].replace("Patient/i", '')
        date = evenement["effectiveDateTime"]
        category = evenement["category"][0]["coding"][0]["code"]
        code = observation_type
        value = evenement["valueString"]
        line = ipp +SEP+ date +SEP+ category +SEP+ code +SEP+ value +"\r"
    else:
        fichier = ouverture_fichier("obs_num.csv")
        ipp = evenement["subject"]["reference"].replace("Patient/i", '')
        date = evenement["effectiveDateTime"]
        category = evenement["category"][0]["coding"][0]["code"]
        display = evenement["code"]["coding"][0]["display"]
        value = evenement["valueQuantity"]["value"]
        unit = evenement["valueQuantity"]["unit"]
        out_of_range = evenement["code"]["coding"][0]["system"]
        ref_range = evenement["referenceRange"][0]["text"]
        line = ipp +SEP+ date +SEP+ category +SEP+ display +SEP+ value +SEP+ unit +SEP+ out_of_range +SEP+ ref_range +"\r"
    if not(IA_mode):
        fichier.write(line)
    fichier.close()
    return None


def __add_medication(evenement:dict, IA_mode=False):
    ''' Ajout d'un médicament au fichier 'ref_medications.csv' '''
    fichier = ouverture_fichier("ref_medications.csv")
    code = evenement["code"]["coding"][0]["code"]
    display = evenement["code"]["coding"][0]["display"].replace(',', '.')
    fichier.write(code +SEP+ display +"\r")
    fichier.close()