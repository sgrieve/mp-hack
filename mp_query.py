import re
import json
from SPARQLWrapper import SPARQLWrapper, JSON

class MPHack():

    def __init__(self):

        url = SPARQLWrapper("https://dbpedia.org/sparql")

        url.setReturnFormat(JSON)

        url.setQuery("select * where { ?s dbo:wikiPageWikiLink dbc:UK_MPs_2019–present } ")

        results = url.queryAndConvert()

        result_dict = {}

        for result in results["results"]["bindings"]:
            mp_url = result["s"]["value"]
            slug = mp_url.split("/")[4]

            d = "wikipedia-en:" + slug
            # q = (f"select ?p ?o where {{ ?s foaf:isPrimaryTopicOf {d} ; owl:sameAs ?o }}")

            # q = f"select ?c where {{ ?a foaf:isPrimaryTopicOf {d} ; owl:sameAs ?c FILTER regex(?c, 'wikidata', 'i') }}"
            # q = re.sub("(", "\\(", q)

            # q = f"select ?name where {{ ?name foaf:isPrimaryTopicOf {d} }}"

            q = f"select ?name ?o ?comment where {{ ?u foaf:isPrimaryTopicOf {d} ; rdfs:label ?name ; rdfs:comment ?comment ; owl:sameAs ?o FILTER regex(?o, 'wikidata', 'i') FILTER(lang(?name)='en') FILTER(lang(?comment)='en')}}"



            
            # print(q)
            # q.translate({"(":  r"\(",
            #                 ")":  r"\)"
            #             })
            

            # print(q)

            # print(q)

            url.setQuery(q)


            # get name
            

            try:
                results = url.queryAndConvert()

                for result in results["results"]["bindings"]:
                    print(result)
                    name = result["name"]["value"]
                    abstract = result["comment"]["value"]
                    # wd = wd.split("/")[4]
                    # # name = self.get_wikidata(wd)
                    wd = result["o"]["value"]
                    wd = wd.split("/")[4]
                    # result_dict[wd] = {"Name": name}
            except:
                print(q)

            # result_dict[wd] = name

            # get alma maters

            q = f"select ?name ?lat ?lon where {{ ?u foaf:isPrimaryTopicOf {d} ; dbp:almaMater ?uni . ?uni geo:lat ?lat ; geo:long ?lon ; rdfs:label ?name filter(lang(?name)='en')}}"

            education = []

            url.setQuery(q)
            try:
                results = url.queryAndConvert()

                for result in results["results"]["bindings"]:
                    # print(result)
                    # unis.append(result["name"]["value"])

                    education.append({"UniName": result["name"]["value"], "UniLocation": result["lat"]["value"] + ", " + result["lon"]["value"] })
                    # wd = wd.split("/")[4]
                    # name = self.get_wikidata(wd)
                    # result_dict[wd] = {"Name": name}
            except:
                print(q)

            result_dict[wd] = {"Name": name, "Abstract": abstract, "Education": education}

        print(result_dict)

        with open('mps.json', 'w') as f:
            json.dump(result_dict, f)

    def get_wikidata(self, id):

        url = SPARQLWrapper("https://query.wikidata.org/sparql")

        url.setReturnFormat(JSON)
        # q = f"select * where {{ wd:{id} wdt:P69 ?o }}"
        q = f"select * where {{ wd:{id} rdfs:label ?o FILTER(LANG(?o) = 'en' )}}"


        print("ugg")
        print(q)

        url.setQuery(q)

        results = url.queryAndConvert()

        # print(results)

        

        for i in results["results"]["bindings"]:
            name = i["o"]["value"]
        
        return name

        


if __name__ == "__main__":
    m = MPHack()
    # m.main()
