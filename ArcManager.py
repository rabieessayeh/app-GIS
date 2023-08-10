# -*- coding: utf-8 -*-

import arcpy

path = 'G:\Mon Drive\Mes cours\Master\S2\Datawarehouse  Geographic Information Systems\Geographic Information Systems\TP_GIS\Geodatabase.gdb'
def GetCouche():
    # Vérifier que la géodatabase existe
    if not arcpy.Exists(path):
        print("La géodatabase spécifiée n'existe pas.")
        return

    arcpy.env.workspace = path
    layer_list = []

    # Parcourir les couches à la racine de la géodatabase
    for layer in arcpy.ListFeatureClasses():
        layer_list.append(layer)

    # Parcourir les datasets dans la géodatabase
    for data in arcpy.ListDatasets():
        # Parcourir les couches dans le dataset
        for layer in arcpy.ListFeatureClasses("", "", data):
            layer_list.append(layer)

    if not layer_list:
        return "Aucune couche n'a été trouvée dans le dataset."
    else:
        return layer_list


def Ajouter_Couche(nom_couche, type_couche):
    # Vérifier si la couche existe déjà dans la géodatabase
    if arcpy.Exists(path + "\\" + nom_couche):
        return 0
    else:
        # Ajouter la couche à la géodatabase
        arcpy.CreateFeatureclass_management(path, nom_couche,type_couche )

        return 1


def Modifier_Couche(nom_couche, nouveau_nom, nouveau_type):
    arcpy.env.workspace = path
    arcpy.env.overwriteOutput = True

    # Vérifier si la couche existe dans la géodatabase
    if arcpy.Exists(nom_couche):
        # Obtenir le chemin complet de la couche
        couche = arcpy.Describe(nom_couche)
        chemin_couche = couche.catalogPath

        # Renommer la couche
        arcpy.Rename_management(chemin_couche, nouveau_nom)

        # Convertir la couche en nouveau type
        arcpy.CopyFeatures_management(nouveau_nom, nouveau_type)

        print("La couche a été modifiée avec succès.")
        return (1, "La couche a été modifiée avec succès.")
    else:
        print("La couche spécifiée n'existe pas dans la géodatabase.")
        return (0, "La couche spécifiée n'existe pas dans la géodatabase.")


def Supprimer_Couche(nom_couche):

    try:
        arcpy.env.workspace = path
        arcpy.Delete_management(nom_couche)
        print("La couche {} a été supprimée avec succès.".format(nom_couche))
        return (1, "La couche {} a été supprimée avec succès.".format(nom_couche))
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        return (0, arcpy.GetMessages())

def Ajouter_champe(nom_couche, nom_champ, type_champ):

    # Vérifier si la couche existe déjà dans la géodatabase
    if arcpy.Exists(path + "\\" + nom_couche):
        arcpy.AddField_management(nom_couche, nom_champ, type_champ)
        print("Le champ a été ajouté avec succès à la couche.")
        return (1, "Le champ a été ajouté avec succès à la couche.")
    else:
        print("La couche spécifiée n'existe pas.")
        return (0, "La couche spécifiée n'existe pas.")

def ajouter_enregistrement_dans_couche(couche, values):
    chemin_couche = path + "\\" + couche
    couche = arcpy.management.MakeFeatureLayer(chemin_couche, "couche_temp").getOutput(0)
    description = arcpy.Describe(couche)
    # champs = description.fields
    champs = [champ for champ in description.fields if champ.name not in ["OBJECTID", "SHAPE", "Shape"]]

    types_champs = {}
    for champ in champs:
        types_champs[champ.name] = champ.type

    # Vérification du nombre de valeurs et du nombre de champs
    if len(values) != len(champs):
        print("Le nombre de valeurs ne correspond pas au nombre de champs.")
        return

    valeurs_converties = []
    for i in range(len(values)):
        valeur = values[i]
        champ = champs[i]
        if champ.type == 'String':
            valeur_convertie = str(valeur)
        elif champ.type == 'Double':
            valeur_convertie = float(valeur)
        elif champ.type == 'Integer':
            valeur_convertie = int(valeur)
        elif champ.type == 'Date':
            # Adapter la conversion de la date selon le format attendu
            valeur_convertie = arcpy.ParseDateTime(valeur)
        else:
            # Gérer d'autres types de champs selon les besoins
            valeur_convertie = valeur

        valeurs_converties.append(valeur_convertie)

    with arcpy.da.InsertCursor(couche, [champ.name for champ in champs if not champ.required]) as curseur:
        curseur.insertRow(valeurs_converties)
    print("Enregistrement ajouté avec succès.")


def supprimer_enregistrement_dans_arcgis(nom_couche, objectid):
    chemin_couche = path + "\\" + nom_couche
    couche = arcpy.management.MakeFeatureLayer(chemin_couche, "couche_temp").getOutput(0)

    with arcpy.da.UpdateCursor(couche, "*") as curseur:
        for row in curseur:

            if row[0] == objectid:
                curseur.deleteRow()
                print ("Supprimer avec sucees")
            return

    print("Aucun enregistrement correspondant à l'OBJECTID spécifié n'a été trouvé.")
