import pandas as pd
import numpy as np
import datetime as dt
import scipy as s
import sys
import json
from nameparser import HumanName
from SPARQLWrapper import SPARQLWrapper, JSON
# import progressbar

def find_DBpedia(name):
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        query = """
            PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX  dbo: <http://dbpedia.org/ontology/>
            PREFIX  dbp: <http://dbpedia.org/property/>

            SELECT ?resource ?name
            WHERE {
              ?resource  rdf:type  dbo:Person;
              rdfs:label ?name. 
              FILTER regex(?name,"""+'"'+name+'"'+""","i")
            }
            """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data_db=pd.DataFrame(results['results']['bindings']) 

        return(data_db) 

def find_WikiData(name):
    data_Wiki = None
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        query = """
        SELECT ?p ?pLabel ?name 
        WHERE {
          ?p wdt:P31 wd:Q5.
          ?p wdt:P1559 ?name.
          FILTER regex(?name,"""+'"'+name+'"'+""","i")
          SERVICE wikibase:label { bd:serviceParam wikibase:language "all". }
        }
            """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data_Wiki=pd.DataFrame(results['results']['bindings']) 
    except TypeError as e1:
        print ('The index:', i, 'encountered exception: TypeError')
        print(e1)
        pass
    except ValueError as e2: 
        print ('The index:', i, 'encountered exception: ValueError')
        print(e2)
        pass
    except NameError as e4:
        print ('The index:', i, 'encountered exception: NameError')
        print(e4)
        pass
    except Exception as e:
        print ('The index:', i, 'encountered exception: Exception')
        print(e)
        pass
    
    return(data_Wiki) 

def find_WikiYago(name):
    data_Wiki = None
    try:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        query = """
            SELECT ?human ?name
            WHERE {
                ?human a <http://dbpedia.org/class/yago/WikicatLivingPeople>;
                rdfs:label ?name
                FILTER regex(?name,"""+'"'+name+'"'+""","i")
                }
            """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        data_Wiki=pd.DataFrame(results['results']['bindings']) 

    except TypeError as e1:
        print ('The index:', i, 'encountered exception: TypeError')
        print(e1)
        pass
    except ValueError as e2: 
        print ('The index:', i, 'encountered exception: ValueError')
        print(e2)
        pass
    except NameError as e4:
        print ('The index:', i, 'encountered exception: NameError')
        print(e4)
        pass
    except Exception as e:
        print ('The index:', i, 'encountered exception: Exception')
        print(e)
        pass

    return(data_Wiki) 

def clean_char(df):
    df['name_mod'] = df['name'].replace({'\$': '', ',': '', "'":'', '"': ''}, regex=True)
    return(df)

def split_names(df):
    try:
        for i, row in data_per[95000:].iterrows():
        #for i, row in data_per[:10].iterrows():
            aux = HumanName(i.encode('utf-8'))
            df.loc[i]['Title']=aux.title
            df.loc[i]['First_Name']=aux.first
            df.loc[i]['Middle_Name']=aux.middle
            df.loc[i]['Last_Name']=aux.last
            df.loc[i]['Suffix_Name']=aux.suffix
            df.loc[i]['nickName']=aux.nickname
            df.to_json("SplittedNames.JSON",orient='table')
    except AttributeError:
        pass
    return(df)


if __name__ == '__main__':
    org=pd.read_json('organizations.json')
    per=pd.read_json('persons.json')
    news=pd.read_json('news.json')
    try:
        data_per = pd.read_json('wikiData_all.json', orient='records')
    except Exception as e:
        print(e)
        data_per= pd.read_json('Clean_DS.json', orient='records')
    
    data_per['index'] = data_per['Name_mod']
    data_per.set_index('index', inplace=True)
    print(data_per)
    
    for j in range(0, len(data_per), 100): 
        if not (data_per.ix[j:j+100,'rawData_wiki']).isnull().any():
            print (j, 'already computed')
            continue
        print(j)  
        try:
            per_aux = data_per[j:j+100]
            data_per.loc[j:j+100,'rawData_wiki'] = per_aux['Name_mod'].apply(lambda i: str(find_WikiData(str(i))))

            # for i, row in per_aux.iterrows():
            #     try:
            #         data_per.loc[i,'rawData_Yago'] = str(find_WikiYago(str(i)))
                
            # except TypeError as e1:
            #     print ('The index:', i, 'encountered exception: TypeError')
            #     print(e1)
            #     pass
            # except ValueError as e2: 
            #     print ('The index:', i, 'encountered exception: ValueError')
            #     print(e2)
            #     pass
            # except NameError as e4:
            #     print ('The index:', i, 'encountered exception: NameError')
            #     print(e4)
            #     pass
            # except Exception as e:
            #     print ('The index:', i, 'encountered exception: Exception')
            #     print(e)
            #     pass

            data_per.to_json('WikiData_all.json', orient='records')
        except Exception as e:
            print(e)
            pass


