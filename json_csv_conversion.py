import json

PATH="./"
SEP = ", "

# # Ouverture du fichier et parsing des données json->dictionnaire python
# with open("Donnes_demo_pharmIA.json", "r") as fichier:
#     all_data = json.load(fichier)

# print(len(all_data["entry"]))
# for i in range(10):
#     # print(all_data["entry"][i])
#     print(type(all_data["entry"][i]["resource"]))
#     print(all_data["entry"][i]["resource"]["essai"])
#     # data = json.loads(all_data["entry"][i])
#     # print(data)
# # for data in all_data:
# #     data = json.dumps(data)
# #     print(data)

def JSON_CSV_CONVERTER(json_path:str) -> None:
    with open("Donnes_demo_pharmIA.json", "r") as fichier:
        all_data = json.load(fichier)
    # taille_json = len(all_data["entry"])
    for evenement in all_data["entry"]:
        evenement = evenement["resource"]
        if evenement["resourceType"]=="Patient":
            add_patient(evenement)
        elif evenement["resourceType"]=="Condition":
            add_condition(evenement)
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
    ''' Ajout d'un patient au fichier 'conditions.csv' '''
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



def add_condition(evenement:dict, IA_mode=False)->None:
    ''' Ajout d'un patient au fichier 'conditions.csv' '''
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

    
JSON_CSV_CONVERTER("Donnes_demo_pharmIA.json")
