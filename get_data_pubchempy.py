#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 12:25:32 2019

@author: tania
"""



import pubchempy as pcp
from bs4 import BeautifulSoup
import pandas as pd
import bs4
import numpy as np
import psycopg2
from sqlalchemy import create_engine

user_pg = "user_pg"
passwd_pg = "passwd_pg"

db_pg = psycopg2.connect(host="localhost",
                         database="uniiquim",
                         user=user_pg,
                         password=passwd_pg)


cur = db_pg.cursor()


rec = True

while rec:
    sql = 'SELECT r.id_formula, r.plain_text_molecular_formula \
           FROM public.distinct_formula_rev2 r \
           LEFT JOIN public.ncbi_result_formula2 h \
           ON r.id_formula = h.id_formula \
           WHERE h.id_formula IS NULL \
           LIMIT 1'
    cur.execute(sql)  #
    rec = cur.fetchone()  
    #print rec
    num_compound = rec[0] #de
    formula = rec[1]

    cur.execute("INSERT INTO public.ncbi_result_formula2 (id_formula, plain_text_molecular_formula, processed) VALUES (%s, %s, 1);", (num_compound, formula,))
    db_pg.commit()   #
    

s = True

while s:
    sql = 'SELECT id_formula, cid \
           FROM public.ncbi_result_formula2 \
           WHERE processed = 2 \
           AND cid IS NOT NULL\
           ORDER BY id_formula \
           LIMIT 1'
    cur.execute(sql)  #
    s = cur.fetchone()  
    num_compound = s[0]
    cid = s[1]

        

    try:
        #cid = pcp.get_cids(formula, 'formula', listkey_count=1)
        print "Getting synonym on " + str(cid)
        #properties = pcp.get_properties(['ExactMass','MolecularWeight', 'MolecularFormula', 'CanonicalSMILES', 'IUPACName', 'InChIKey', 'InChi'], formula, 'formula', listkey_count=1)
        #list_p = list.index(properties)
       # molecular_weight = pcp.get_properties(formula, 'formula', listkey_count=1))
       # molecular_formula = pcp.get_properties(formula, 'formula', listkey_count=1))
       # molecular_weight = pcp.get_properties(formula, 'formula', listkey_count=1))
       # molecular_weight = pcp.get_properties(formula, 'formula', listkey_count=1))
        synonyms = pcp.get_synonyms(cid, 'cid', listkey_count=1)
        for syn in synonyms:
            #print(item)
        #for p in properties:
            sql = "UPDATE ncbi_result_formula2 \
                   SET synonyms = %s, processed = %s \
                   WHERE id_formula = %s and cid = %s \
                  "
            cur.execute(sql, (syn["Synonym"], 3, num_compound, syn["CID"] ))


        cur.execute("DELETE FROM ncbi_result_formula2 WHERE cid=%s AND processed=2", (cid,))
        db_pg.commit()                
         
    except:
        pass 









