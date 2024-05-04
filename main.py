import json
import tkinter

import pandas as pd
from tkinter import Tk, Frame, Label, Entry, Text
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import plotly.express as px
import plotly.graph_objects as go

from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
from plotly.colors import n_colors
from plotly.subplots import make_subplots
from IPython.display import Image

import tkinter as tk  # Using 'tk' as alias for cleaner code

import pandas as pd

genero = ''
pesoGenero = 0.0

classificacao = ''
pesoClassificacao = 0.0

imdb = ''
pesoImdb = 0.0

titulo = ''
pesoTitulo = 0.0

duracao = ''
pesoDuracao = 0.0

ano = ''
pesoAno = 0.0

# Read the CSV file (replace with your actual CSV path if different)
df_tv = pd.read_csv('./tv_shows.csv')

# Drop unnecessary column if it exists
df_tv = df_tv.drop(['Unnamed: 0'], axis = 1)

# Create the main window
root = tk.Tk()
root.title("TV Show List")

class Filme:
    def __init__(self, titulo, valor_similaridade):
        self.titulo = titulo
        self.valor_similaridade = valor_similaridade


def csv_to_filme_list(filename):
    filme_list = []
    try:
        # Open the CSV file in read mode
        with open(filename, 'r', encoding='utf-8') as csvfile:
            # Skip the header row (assuming the first row contains column names)
            next(csvfile)
            for row in csvfile:
                data = row.strip().split(',')
                filme = Filme(data[2], "")
                # Add the Filme object to the list
                filme_list.append(filme)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

    return filme_list


def calcular_similaridade_genero(genero_recebido, genero_inputado):
    if genero_recebido == genero_inputado:
        return 1
    if genero_recebido == "Comedy":
        if genero_inputado == "Action":
            return 0.3
        if genero_inputado == "Drama":
            return 0.4
        if genero_inputado == "Romance":
            return 0.7
        if genero_inputado == "Musical":
            return 0.5
        if genero_inputado == "History":
            return 0.2
    if genero_recebido == "Action":
        if genero_inputado == "Comedy":
            return 0.3
        if genero_inputado == "Drama":
            return 0.4
        if genero_inputado == "Romance":
            return 0.2
        if genero_inputado == "Musical":
            return 0.1
        if genero_inputado == "History":
            return 0.4
    if genero_recebido == "Drama":
        if genero_inputado == "Comedy":
            return 0.4
        if genero_inputado == "Action":
            return 0.4
        if genero_inputado == "Romance":
            return 0.5
        if genero_inputado == "Musical":
            return 0.2
        if genero_inputado == "History":
            return 0.8
    if genero_recebido == "Romance":
        if genero_inputado == "Comedy":
            return 0.7
        if genero_inputado == "Action":
            return 0.2
        if genero_inputado == "Drama":
            return 0.5
        if genero_inputado == "Musical":
            return 0.3
        if genero_inputado == "History":
            return 0.2
    if genero_recebido == "Musical":
        if genero_inputado == "Comedy":
            return 0.5
        if genero_inputado == "Action":
            return 0.1
        if genero_inputado == "Drama":
            return 0.3
        if genero_inputado == "Romance":
            return 0.3
        if genero_inputado == "History":
            return 0
    if genero_recebido == "History":
        if genero_inputado == "Comedy":
            return 0.2
        if genero_inputado == "Action":
            return 0.4
        if genero_inputado == "Drama":
            return 0.8
        if genero_inputado == "Romance":
            return 0.2
        if genero_inputado == "Musical":
            return 0
    return 0

def calcular_similaridade_imdb(imdb_recebido, imdb_inputado):
    inputado = 0
    recebido = 0

    print(imdb_recebido)
    print(imdb_inputado)

    if imdb_recebido >= 1 and imdb_recebido < 2:
        recebido = 1
    if imdb_recebido >= 2 and imdb_recebido < 4:
        recebido = 2
    if imdb_recebido >= 4 and imdb_recebido < 6:
        recebido = 3
    if imdb_recebido >= 6 and imdb_recebido < 8:
        recebido = 4
    if imdb_recebido >= 8:
        recebido = 5

    if imdb_inputado >= 1 and imdb_inputado < 2:
        inputado = 1
    if imdb_inputado >= 2 and imdb_inputado < 4:
        inputado = 2
    if imdb_inputado >= 4 and imdb_inputado < 6:
        inputado = 3
    if imdb_inputado >= 6 and imdb_inputado < 8:
        inputado = 4
    if imdb_inputado >= 8:
        inputado = 5

    resultado = 1  - ( abs(inputado - recebido) / ( inputado + recebido) )

    return resultado

def calcular_similaridade_ano(ano_recebido, ano_inputado):
    inputado = 0
    recebido = 0

    if ano_recebido <= 1900:
        recebido = 1
    if ano_recebido >= 1900 and ano_recebido < 1960:
        recebido = 2
    if ano_recebido >= 1960 and ano_recebido < 1980:
        recebido = 3
    if ano_recebido >= 1980 and ano_recebido < 2000:
        recebido = 4
    if ano_recebido >= 2000 and ano_recebido < 2015:
        recebido = 5
    if ano_recebido >= 2015:
        recebido = 6

    if ano_inputado <= 1900:
        inputado = 1
    if ano_inputado >= 1900 and ano_inputado < 1960:
        inputado = 2
    if ano_inputado >= 1960 and ano_inputado < 1980:
        inputado = 3
    if ano_inputado >= 1980 and ano_inputado < 2000:
        inputado = 4
    if ano_inputado >= 2000 and ano_inputado < 2015:
        inputado = 5
    if ano_inputado >= 2015:
        inputado = 6

    resultado = 1  - ( abs(inputado - recebido) / ( inputado + recebido) )

    return resultado

def calcular_similaridade_classificacao(classficacao_recebido, classificacao_inputado):
    dicionario = {
        "all": 1,
        "7+": 2,
        "13+": 3,
        "16+": 4,
        "18+": 5,
    }

    inputado = 0 if dicionario.get(classificacao_inputado) == None else dicionario.get(classificacao_inputado)
    recebido = 0 if dicionario.get(classficacao_recebido) == None else dicionario.get(classficacao_recebido)

    resultado = 1 - ( abs(inputado - recebido) / ( inputado + recebido) )

    return resultado

def calcular_similaridade_duracao(duracao_recebido, duracao_inputado):
    inputado = 0
    recebido = 0

    if duracao_recebido <= 40:
        recebido = 1
    if duracao_recebido >= 40 and duracao_recebido < 60:
        recebido = 2
    if duracao_recebido >= 60 and duracao_recebido < 90:
        recebido = 3
    if duracao_recebido >= 90 and duracao_recebido < 120:
        recebido = 4
    if duracao_recebido >= 120:
        recebido = 5

    if duracao_inputado <= 40:
        inputado = 1
    if duracao_inputado >= 40 and duracao_inputado < 60:
        inputado = 2
    if duracao_inputado >= 60 and duracao_inputado < 90:
        inputado = 3
    if duracao_inputado >= 90 and duracao_inputado < 120:
        inputado = 4
    if duracao_inputado >= 120:
        inputado = 5

    resultado = 1  - ( abs(inputado - recebido) / ( inputado + recebido) )

    return resultado


filme_list = []
def update_table():
    genero = new_search_entry.get()
    pesoGenero = float(search_entry.get())

    classificacao =  new_search_entry2.get()
    pesoClassificacao = float(search_entry2.get())

    imdb =  new_search_entry5.get()
    pesoImdb = float(search_entry5.get())

    duracao =  new_search_entry3.get()
    pesoDuracao = float(search_entry3.get())

    ano =  new_search_entry4.get()
    pesoAno = float(search_entry4.get())

    lista = []

    with open("MoviesOnStreamingPlatforms_updated.csv", 'r', encoding='utf-8') as csvfile:
        # Skip the header row (assuming the first row contains column names)
        next(csvfile)
        for row in csvfile:
            data = row.strip().split(',')

            similiraridade_genero = calcular_similaridade_genero(data[13].split(",")[0].replace('"', ''), genero) * pesoGenero
            similiraridade_ano = calcular_similaridade_ano(int(data[3]), int(ano)) * pesoAno
            similiraridade_classificacao = calcular_similaridade_classificacao(data[4], classificacao) * pesoClassificacao
            similiraridade_imdb = calcular_similaridade_imdb(float(data[5].split("/")[0].replace("'", "")), float(imdb)) * pesoImdb
            similiraridade_duracao = calcular_similaridade_duracao(( 0.0 if data[-1] == '' else float(data[-1]) ), float(duracao)) * pesoDuracao

            peso_total = pesoGenero + pesoAno + pesoDuracao + pesoImdb + pesoClassificacao
            similiraridade_total = (similiraridade_duracao + similiraridade_imdb + similiraridade_classificacao + similiraridade_ano + similiraridade_genero) / peso_total

            filme = Filme(data[2], similiraridade_total)
            lista.append({
                "titulo": data[2],
                "valor_similaridade": similiraridade_total
            })
    pass

    sorted_filmes = sorted(lista, key=lambda x: x["valor_similaridade"], reverse=True)

    df_tv2 = pd.read_json(json.dumps(sorted_filmes))
    table_text.delete('1.0', tk.END)
    table_text.insert(tk.END, df_tv2.to_string())


# Create frames for table and inputs
table_frame = tk.Frame(root)
table_frame.pack()

# Table label and Text widget
table_label = tk.Label(table_frame, text="TV Shows")
table_label.pack()

table_text = tk.Text(table_frame, height=20, width=120)
table_text.pack()

input_frame = tk.Frame(root)
input_frame.pack()

input_frame2 = tk.Frame(root)
input_frame2.pack()

input_frame3 = tk.Frame(root)
input_frame3.pack()

input_frame4 = tk.Frame(root)
input_frame4.pack()

input_frame5 = tk.Frame(root)
input_frame5.pack()

input_frame6 = tk.Frame(root)
input_frame6.pack()



# Input labels and Entry widgets
input_label = tk.Label(input_frame, text="Gênero:")
input_label.pack(side=tk.LEFT)  # Place label to the left

search_entry = tk.Entry(input_frame)
search_entry.pack(side=tk.RIGHT)  # Place entry to the right

# New entry for additional information
new_entry_label = tk.Label(input_frame, text="   ")  # Spacer label
new_entry_label.pack(side=tk.RIGHT)

new_search_entry = tk.Entry(input_frame)
new_search_entry.pack(side=tk.RIGHT)  # Place new entry next to original

# Repeat for other input frames
input_label2 = tk.Label(input_frame2, text="Classificação Indicativa:")
input_label2.pack(side=tk.LEFT)

search_entry2 = tk.Entry(input_frame2)
search_entry2.pack(side=tk.RIGHT)

new_entry_label2 = tk.Label(input_frame2, text="   ")
new_entry_label2.pack(side=tk.RIGHT)

new_search_entry2 = tk.Entry(input_frame2)
new_search_entry2.pack(side=tk.RIGHT)

input_label3 = tk.Label(input_frame3, text="Duração:")
input_label3.pack(side=tk.LEFT)

search_entry3 = tk.Entry(input_frame3)
search_entry3.pack(side=tk.RIGHT)

new_entry_label3 = tk.Label(input_frame3, text="   ")
new_entry_label3.pack(side=tk.RIGHT)

new_search_entry3 = tk.Entry(input_frame3)
new_search_entry3.pack(side=tk.RIGHT)


input_label4 = tk.Label(input_frame4, text="Ano de Lançamento:")
input_label4.pack(side=tk.LEFT)

search_entry4 = tk.Entry(input_frame4)
search_entry4.pack(side=tk.RIGHT)

new_entry_label4 = tk.Label(input_frame4, text="   ")
new_entry_label4.pack(side=tk.RIGHT)

new_search_entry4 = tk.Entry(input_frame4)
new_search_entry4.pack(side=tk.RIGHT)


input_label5 = tk.Label(input_frame5, text="Nota IMDb:")
input_label5.pack(side=tk.LEFT)

search_entry5 = tk.Entry(input_frame5)
search_entry5.pack(side=tk.RIGHT)

new_entry_label5 = tk.Label(input_frame5, text="   ")
new_entry_label5.pack(side=tk.RIGHT)

new_search_entry5 = tk.Entry(input_frame5)
new_search_entry5.pack(side=tk.RIGHT)

# (Optional) Button (commented out as update logic is based on entry changes)
update_button = tk.Button(input_frame6, text="Pesquisar", command=update_table)
update_button.pack()


root.mainloop()