# -*- coding: utf-8 -*-
from ArcManager import *
from tkinter import ttk
import tkinter as tk
import tkMessageBox


def quitter():
    root.quit()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Interface de gestion")



liste_frame = tk.Frame(root)
liste_frame.pack(side=tk.LEFT, padx=10, pady=10)


global liste
liste = tk.Listbox(liste_frame)
for couche in GetCouche():
    liste.insert('end', couche)
liste.pack()


def Erreur(liste):
    if liste.curselection():
        pass
    else:
        tkMessageBox.showerror("Erreur", "Aucune couche selectionnee")


def Afficher_liste():
    liste.delete(0, tk.END)
    for couche in GetCouche():
        liste.insert('end', couche)
    liste.pack()

# Bouton Actualiser
bouton_actualiser = tk.Button(liste_frame, text="Actualiser", command=Afficher_liste)
bouton_actualiser.pack()
def afficher_couche():
    Erreur(liste)
    selected_index = liste.curselection()
    couche_selectionnee = liste.get(selected_index)


    # Obtenir les noms des attributs de la couche
    attributs = [field.name for field in arcpy.ListFields(couche_selectionnee)]
    # Obtenir les valeurs des attributs pour chaque enregistrement
    valeurs_attributs = []
    with arcpy.da.SearchCursor(couche_selectionnee, '*') as curseur:
        for row in curseur:
            valeurs_attributs.append(row)

    # Créer la fenêtre Tkinter
    fenetre = tk.Tk()
    fenetre.title("La Couche "+ str(couche_selectionnee).upper())

    # Créer le tableau
    tableau = ttk.Treeview(fenetre, columns=attributs, show="headings")

    # Ajouter les colonnes au tableau
    for attribut in attributs:
        tableau.heading(attribut, text=attribut)
        tableau.column(attribut, width=100)

    # Ajouter les enregistrements au tableau
    for valeur_attribut in valeurs_attributs:
        tableau.insert("", tk.END, values=valeur_attribut)

    # Afficher le tableau
    tableau.pack()

    # Exécuter la boucle principale Tkinter
    fenetre.mainloop()

def ajouter_couche():
    def valider():
        nom_couche = champ_saisie.get()
        type_couche = liste_types.get()

        if nom_couche and type_couche:
            Ajouter_Couche(nom_couche, type_couche)
            tkMessageBox.showinfo("Information",
                                "Nom de la couche : {}\nType de la couche : {}".format(nom_couche,type_couche))
            Afficher_liste()
            fenetre_saisie.destroy()
        else:
            tkMessageBox.showerror("Erreur", "Veuillez remplir tous les champs.")

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("300x100")
    fenetre_saisie.title("Ajouter une couche")

    # Zone de saisie pour le nom de la couche
    label_nom = tk.Label(fenetre_saisie, text="Nom de la couche:")
    label_nom.pack()
    champ_saisie = tk.Entry(fenetre_saisie)
    champ_saisie.pack()

    # Liste déroulante pour le type de la couche
    label_type = tk.Label(fenetre_saisie, text="Type de la couche:")
    label_type.pack()
    types_couche = ["POINT", "MULTIPOINT", "POLYGON", "POLYLINE", "MULTIPATCH"]  # Exemple de types de couche
    liste_types = ttk.Combobox(fenetre_saisie, values=types_couche, state="readonly")
    liste_types.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()


def modifier_couche():
    Erreur(liste)
    selected_index = liste.curselection()
    couche_selectionnee = liste.get(selected_index)

    def valider():
        nom_couche = champ_saisie.get()
        type_couche = liste_types.get()

        if nom_couche and type_couche:
            pass
        else:
            tkMessageBox.showerror("Erreur", "Veuillez remplir tous les champs.")

        resultat = Modifier_Couche(couche_selectionnee ,nom_couche, type_couche)
        if resultat[0]:
            tkMessageBox.showinfo("Information", resultat[1])
            Afficher_liste()
            fenetre_saisie.destroy()
        else:
            tkMessageBox.showerror("Erreur", resultat[1])

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("300x100")
    fenetre_saisie.title("Modifier une couche")

    # Zone de saisie pour le nom de la couche
    label_nom = tk.Label(fenetre_saisie, text="Nom de la couche:")
    label_nom.pack()
    champ_saisie = tk.Entry(fenetre_saisie)
    champ_saisie.insert(0, couche_selectionnee)
    champ_saisie.pack()

    # Liste déroulante pour le type de la couche
    label_type = tk.Label(fenetre_saisie, text="Type de la couche:")
    label_type.pack()
    types_couche = ["POINT", "MULTIPOINT", "POLYGON", "POLYLINE", "MULTIPATCH"]  # Exemple de types de couche
    liste_types = ttk.Combobox(fenetre_saisie, values=types_couche, state="readonly")
    liste_types.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()


def supprimer_couche():
    Erreur(liste)
    selected_index = liste.curselection()
    couche_selectionnee = liste.get(selected_index)

    resultat = Supprimer_Couche(couche_selectionnee)

    if resultat[0]:
        tkMessageBox.showinfo("Information",
                              resultat[1])
        Afficher_liste()
    else:
        tkMessageBox.showerror("Erreur",
                               resultat[1])

def ajouter_champe():
    Erreur(liste)
    selected_index = liste.curselection()
    couche_selectionnee = liste.get(selected_index)

    def valider():
        nom_champe = champ_saisie.get()
        type_champe = liste_types.get()

        if nom_champe and type_champe:
            pass
        else:
            tkMessageBox.showerror("Erreur", "Veuillez remplir tous les champs.")

        resultat = Ajouter_champe(couche_selectionnee ,nom_champe, type_champe)
        if resultat[0]:
            tkMessageBox.showinfo("Information", resultat[1])
            Afficher_liste()
            fenetre_saisie.destroy()
        else:
            tkMessageBox.showerror("Erreur", resultat[1])

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("300x100")
    fenetre_saisie.title("Ajouter un champe a la couche " + str(couche_selectionnee).upper())

    # Zone de saisie pour le nom de la couche
    label_nom = tk.Label(fenetre_saisie, text="Nom de champe:")
    label_nom.pack()
    champ_saisie = tk.Entry(fenetre_saisie)
    champ_saisie.pack()

    # Liste déroulante pour le type de la couche
    label_type = tk.Label(fenetre_saisie, text="Type de champe:")
    label_type.pack()
    types_champe = ["TEXT", "FLOAT", "DOUBLE", "SHORT", "LONG", "DATE", "BLOB", "RASTER", "SHORT", "GUID"]
    liste_types = ttk.Combobox(fenetre_saisie, values=types_champe, state="readonly")
    liste_types.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()


# def ajouter_enregistrement_couche_arcgis():
#     Erreur(liste)
#     # Création de la fenêtre principale
#     fenetre = tk.Tk()
#     fenetre.title("Ajouter un nouvel enregistrement")
#
#     # Connexion à la couche ArcGIS
#     selected_index = liste.curselection()
#     couche = liste.get(selected_index)
#     arcpy.MakeFeatureLayer_management(couche, "couche_temporaire")
#
#
#     champs_couche = [field.name for field in arcpy.ListFields("couche_temporaire")]
#
#     # Création des labels et des champs de saisie pour les champs de la couche
#     for champ in champs_couche:
#         label = tk.Label(fenetre, text=champ)
#         label.pack()
#         champ_saisie = tk.Entry(fenetre)
#         champ_saisie.pack()
#
#     # Fonction pour ajouter l'enregistrement à la couche
#     def ajouter_enregistrement():
#         # Récupération des valeurs saisies
#
#         valeurs_champs = [champ.get() for champ in champ_saisie ]
#
#
#         ajouter_enregistrement_dans_couche(couche, valeurs_champs)
#
#     # Bouton pour ajouter l'enregistrement
#     bouton_ajouter = tk.Button(fenetre, text="Ajouter", command=ajouter_enregistrement)
#     bouton_ajouter.pack()
#
#     # Exécution de la fenêtre principale
#     fenetre.mainloop()





#Création des boutons de gestion
def ajouter_enregistrement_couche_arcgis():
    # Créer une fenêtre Tkinter
    fenetre = tk.Tk()
    fenetre.title("Ajouter un nouvel enregistrement")

    # # Récupérer les informations de la couche ArcGIS
    selected_index = liste.curselection()
    couche = liste.get(selected_index)

    description = arcpy.Describe(couche)
    champs = description.fields

    # Créer les champs de saisie pour chaque champ de la couche
    entrees = []
    for champ in champs:
        if not champ.required:
            tk.Label(fenetre, text=champ.name).pack()
            entree = tk.Entry(fenetre)
            entree.pack()
            entrees.append(entree)

    # Fonction pour ajouter l'enregistrement à la couche
    def ajouter():
        valeurs = [entree.get() for entree in entrees]
        # with arcpy.da.InsertCursor(couche, [champ.name for champ in champs if not champ.required]) as curseur:
        #     curseur.insertRow(valeurs)
        ajouter_enregistrement_dans_couche(couche, valeurs)
        fenetre.destroy()

    # Ajouter un bouton pour ajouter l'enregistrement
    bouton = tk.Button(fenetre, text="Ajouter", command=ajouter)
    bouton.pack()

    fenetre.mainloop()

def supprimer_enregistrement():
    Erreur(liste)
    selected_index = liste.curselection()
    couche = liste.get(selected_index)
    def valider():
        IDOBJECT =champ_saisie.get()

        if IDOBJECT :
            supprimer_enregistrement_dans_arcgis(couche, IDOBJECT)
            tkMessageBox.showinfo("Information",
                                "L'enregistrement a ete supprimer avec succes")
            Afficher_liste()
            fenetre_saisie.destroy()
        else:
            tkMessageBox.showerror("Erreur", "Veuillez entrer l'OBJECTID.")

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("300x100")
    fenetre_saisie.title("Supprimer un enregistrement")

    # Zone de saisie pour le nom de la couche
    label_nom = tk.Label(fenetre_saisie, text="OBJECTID:")
    label_nom.pack()
    champ_saisie = tk.Entry(fenetre_saisie)
    champ_saisie.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()
    afficher_couche()


    fenetre_saisie.mainloop()
gestion_frame = tk.Frame(root)
gestion_frame.pack(padx=20, pady=20)

label_Couche = tk.Label(gestion_frame, text="Gestion des couches", font=("Arial", 10), anchor="center")
label_Couche.grid(row=0, column=0, padx=5)

afficher_button = tk.Button(gestion_frame, text="Afficher", command=afficher_couche)
afficher_button.grid(row=1, column=0, padx=5)

ajouter_button = tk.Button(gestion_frame, text="Ajouter", command=ajouter_couche)
ajouter_button.grid(row=1, column=1, padx=5)

modifier_button = tk.Button(gestion_frame, text="Modifier", command=modifier_couche)
modifier_button.grid(row=1, column=2, padx=5)

supprimer_button = tk.Button(gestion_frame, text="Supprimer", command=supprimer_couche)
supprimer_button.grid(row=1, column=3, padx=5)

label_champe = tk.Label(gestion_frame, text="Gestion des champes", font=("Arial", 10), anchor="center")
label_champe.grid(row=2, column=0, padx=5)

ajouter_champe = tk.Button(gestion_frame, text="Ajouter champe", command=ajouter_champe)
ajouter_champe.grid(row=3, column=0, padx=5)

ajouter_enregistrement = tk.Button(gestion_frame, text="Ajouter enregistrement", command=ajouter_enregistrement_couche_arcgis)
ajouter_enregistrement.grid(row=3, column=1, padx=5)

supprimer_enregistrement = tk.Button(gestion_frame, text="Supprimer enregistrement", command=supprimer_enregistrement)
supprimer_enregistrement.grid(row=3, column=2, padx=5)


quitter_button = tk.Button(root, text="Quitter", font=("Arial", 10), command=quitter)
quitter_button.pack(pady=10)

# Exécution de la boucle principale
root.mainloop()