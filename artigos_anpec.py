#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 10:02:49 2020

@author: pedro
"""

from selenium import webdriver
import pandas as pd

# Alguns anos estão dividos por Áreas, outros não. Criei duas funções para
# acomodar os dois casos. Em especial, o ano de 2015 ainda dá problemas. 

# Funções para os anos com áreas definidas
def get_pattern_artigos(ano):  
    driver = webdriver.Firefox(executable_path=r'/home/pedro/Área de Trabalho/gecko/geckodriver')
    url = 'https://en.anpec.org.br/previous-editions.php?r=encontro-'+ str(ano)
    driver.get(url)
    numero_de_areas = len(driver.find_element_by_id('tab_articles').find_element_by_class_name('panel-group').find_elements_by_class_name('panel-default'))
    ano_da_tag = driver.find_element_by_class_name('section-tabs').get_attribute('id')[8::]
    areas = [ano_da_tag + '-area-' + str(i) for i in range(1,numero_de_areas+1)]
    articles = {'area': [], 'titulos': [], 'autores': []}
    for area in areas:
        artigos = driver.find_elements_by_id(area)[0]        
        ul = artigos.find_elements_by_class_name('normal-text')[0]
        lista_de_artigos = ul.find_elements_by_tag_name('li')
        for artigo in lista_de_artigos:
            titulo_full = artigo.get_attribute("innerHTML") 
            titulo =titulo_full.split('<br>')[0]
            autor = titulo_full.split('<br>')[1]
            articles['area'].append(area[5::])
            articles['titulos'].append(titulo)
            articles['autores'].append(autor)
    
    driver.close()
    return articles

# Funções para os anos sem áreas definidas
def get_diff_artigos(ano):    
    driver = webdriver.Firefox(executable_path=r'/home/pedro/Área de Trabalho/gecko/geckodriver')
    url = 'https://en.anpec.org.br/previous-editions.php?r=encontro-'+ str(ano)
    driver.get(url)
    articles = {'area': [], 'titulos': [], 'autores': []}
    ul = driver.find_elements_by_class_name('normal-text')[0]
    lista_de_artigos = ul.find_elements_by_tag_name('li')
    for artigo in lista_de_artigos:
        titulo_full = artigo.get_attribute("innerHTML") 
        titulo =titulo_full.split('<br>')[0]
        autor = titulo_full.split('<br>')[1]
        articles['area'].append('SEM AREA')
        articles['titulos'].append(titulo)
        articles['autores'].append(autor)
    driver.close()
    return articles


# Coleta os artigos
def get_artigos(ano):
    anos_padrao = [2001, 2002, 2004, 2005, 2006, 2012, 2013, 2014, 
                   2016, 2017, 2018, 2019]
    if ano in anos_padrao:
        artigos = get_pattern_artigos(ano)
        return artigos
    elif ano == 2015:
        next
    else:
        artigos = get_diff_artigos(ano)
        return artigos
        
# Faz um for loop e pega logo tudo
anos = list(map(int, range(2001, 2021)))
artigos = {}
for ano in anos:
  artigos[ano] = get_artigos(ano)

artigos.pop(2015, None)

# Colocar no formato de DataFrame (Não necessário)
anos = list(artigos.keys())
d = pd.DataFrame()
for ano in anos:
    teste = artigos[ano]
    year = [ano]*len(teste['area'])
    df = pd.DataFrame([year, teste['area'], teste['titulos'], teste['autores']]).transpose()
    d = d.append(df)

d.columns =['ano','area','titulos','autores']
usp = d[d['autores'].str.contains("USP")]





