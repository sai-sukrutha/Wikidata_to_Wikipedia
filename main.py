import wikidata_query
from qwikidata.linked_data_interface import get_entity_dict_from_api
from qwikidata.entity import WikidataItem, WikidataProperty, WikidataLexeme

properties_dict = {}
properties_dict['instance of'] = 'P31'

colleges_fields_dict = {}
colleges_fields_dict['inception'] = 'P571'
colleges_fields_dict['country'] = 'P17'
colleges_fields_dict['location'] = 'P276'
colleges_fields_dict['location2'] = 'P131'
colleges_fields_dict['coordinates'] = 'P625'
colleges_fields_dict['chairperson'] = 'P488'

#in telugu
telugu_dict = {}
telugu_dict["instance"]= "ఒక"
telugu_dict["this"] = "ఇది"
telugu_dict['in'] ="లో"
telugu_dict['there'] = "ఉంది"
telugu_dict['for this'] = "దీనికి"
telugu_dict['chairperson'] = "అధ్యక్షుడు"
telugu_dict['started'] = "ప్రారంభం అయింది"


def form_query_college(q_no):
    college_query = """
    SELECT DISTINCT ?instance ?instanceLabel ?location ?locationLabel ?country ?countryLabel ?start ?person ?personLabel
    WHERE {
        { wd:"""+q_no+""" wdt:"""+properties_dict['instance of']+""" ?instance } .
        { wd:"""+q_no+""" wdt:"""+colleges_fields_dict['location2']+""" ?location } .
        { wd:"""+q_no+""" wdt:"""+colleges_fields_dict['country']+""" ?country } .
        { wd:"""+q_no+""" wdt:"""+colleges_fields_dict['inception']+""" ?start } .
        OPTIONAL { wd:"""+q_no+""" wdt:"""+colleges_fields_dict['chairperson'] +""" ?person } .
        SERVICE wikibase:label { 
          bd:serviceParam wikibase:language "te,en". 
    }
    }
    """
    return college_query


def get_wikidata(item):
    q_no = wikidata_query.get_qnumber(wikiarticle=item, wikisite="enwiki")
    #print(q_no)
    query = form_query_college(q_no)
    #print(query)
    data = wikidata_query.run_query(query)
    #print(data)
    return data



def get_page_from_data(data,item):
    #title
    #print(item)
    res = data['results']['bindings'][0]

    page = ""
    page += item+"\n"
    page += "----------------------------------------\n"
    page += item +" "+ telugu_dict['instance']+" "
    page += res['instanceLabel']['value']+"."
    page += telugu_dict['this']+" "+res['locationLabel']['value']+","+res['countryLabel']['value']
    page += " "+telugu_dict['in']+" "+telugu_dict['there']+"."
    if( 'personLabel' in res):
        page+= " "+telugu_dict['for this']+" "+ res['personLabel']['value'] +" "+ telugu_dict['chairperson']+"."
    if( 'start' in res):
        page+= " "+telugu_dict['this']+ " "+ res['start']['value'].split('T')[0] +" " +telugu_dict['in'] + " "+telugu_dict['started']+ "."
    return page




def main():
    item = "International Institute of Information Technology, Hyderabad"
    #item = "Jawaharlal Nehru Technological University, Hyderabad"
    data = get_wikidata(item)
    page = get_page_from_data(data,item)
    print(page)


if __name__ == "__main__":
    main()