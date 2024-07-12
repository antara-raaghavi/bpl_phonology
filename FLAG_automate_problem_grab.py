# -*- coding: utf-8 -*-
# 
import codecs
import os
import json
from FLAG_our_features import *
import re

def transposeInflections(inflections):
    return [ tuple([ inflections[x][y] for x in range(len(inflections)) ]) for y in range(len(inflections[0])) ]

def stripConsonants(matrix):
    def s(x):
        if x == None: return x
        canonical = []
        for p in tokenize(x):
            if p == u'##': canonical.append(p)
            #elif 'vowel' in featureMap[p]: canonical.append(p)
            elif 'vowel' in featureMap[p] and not 'highTone' in featureMap[p]: canonical.append(u'a')
            elif 'vowel' in featureMap[p] and 'highTone' in featureMap[p]: canonical.append(u'á')
        return u''.join(canonical)
    return [tuple(map(s,i)) for i in matrix ]

def processMorphology(stems, inflections, dictionary):
    # map from (stem, inflection) to surface form
    surfaces = {}
    for surface, translation in dictionary.iteritems():
        found = False
        for stem in stems:
            for inflection in inflections:
                if inflection + ' ' + stem == translation or stem + ' ' + inflection == translation or stem + inflection == translation:
                    if found:
                        print "DEGENERACY:"
                        print "Trying to parse the mapping:",surface, translation
                        print "found that it is compatible with",stem, inflection
                        print "previously found it to be",found
                    assert not found
                    found = (stem, inflection)
                    surfaces[(stem, inflection)] = surface.replace(' ','##').replace(u'ɗ',u'd').replace(u'ɓ',u'b')
        if not found:
            print "Could not explain",surface, translation
            assert False
    # Construct the inflection matrix
    matrix = [ tuple([ surfaces.get((stem, inflection),None) for inflection in inflections ])
             for stem in stems ]
    return matrix
            
            
                



class Problem():
    named = {}
    def __init__(self,description,data,parameters = None,solutions = [],supervised=False,stressful=False):
        self.stressful = stressful
        self.supervised = supervised
        self.parameters = parameters
        self.description = description
        self.solutions = solutions
        if isinstance(data[0], basestring):
            self.data = [ x.replace(u"’",u"").replace(u"'",u"").replace(u"-",u"") for x in data ]
        else:
            self.data = [ tuple([ (None if x == None else x.replace(u"’",u"").replace(u"'",u"").replace(u"-",u""))
                                  for x in inflections ])
                          for inflections in data ]

        for n in range(len(data)):
            assert isinstance(data[n], (unicode,tuple,list)), "Problem data should be either a list of tuples of Unicode or a list of Unicode"
        if isinstance(data[0], unicode):
            for n in range(len(data)):
                assert isinstance(data[n], unicode), "Data started out as a Unicode string but turned into %s"%(data[n])
        if isinstance(data[0], (list, tuple)):
            for xs in data:
                assert isinstance(xs, (list, tuple)), "Data started out as tuples but turned into %s"%xs
                assert len(data[0]) == len(xs), "Data should be of uniform length"

        sources = ["Odden","Halle","Roca","Kevin"]
        self.languageName = None
        self.source = None
        for l in description.split("\n"):
            l = l.strip()
            if len(l) > 0:
                if any( s in l for s in sources ):
                    m = re.search("(%s).*"%("|".join(sources)),l)
                    assert m is not None, "This should be impossible - sent to Kevin if this occurs"
                    self.source = str(m.group(0))
                    l = l[:m.start(0)].strip()
                    if len(l) == 0: continue
                l = ' '.join(l.split(' '))
                self.languageName = str(l)
            if self.source is not None and self.languageName is not None: break
        assert self.languageName is not None,\
            "Could not find a valid language name in description %s"%description
        assert self.source is not None,\
            "Could not find a valid problem source in description %s; try adding something like Odden pg <page numbers>"%description
        self.key = (self.source + "_" + self.languageName).replace(' ','_').replace('-','_').replace('(','').replace(')','')
        Problem.named[self.key] = self
        print "Loaded %s problem from %s, named %s"%(self.source, self.languageName, self.key)
        if "en_A" not in self.key:
            if "Kevin" not in self.key:
                if "Tibetan" not in self.key:
                    FeatureBank([w for ws in self.data for w in (ws if isinstance(ws,(list, tuple)) else [ws]) if w]).checkCollisions()

        # As a sanity check we try to tokenize all of the data
        # This is to make sure that as we define each problem we check to see if it only uses things for which we know the features
        for d in self.data:
            if isinstance(d,basestring):
                tokenize(d)
            else:
                for x in d:
                    if x != "~" and x != None:
                        tokenize(x)

    def __str__(self):
        from FLAG_our_utilities import formatTable
        l = []
        patterns = {tuple(s is None for s in ss )
                    for ss in self.data }
        for p in patterns:
            for ss in self.data:
                if tuple(s is None for s in ss ) == p:
                    l.append(map(unicode,ss))
        return formatTable(l)
        return u"\n".join(l)
                    

def problem_to_string(problem):
    data_str = ",\n    ".join(
        [u"({})".format(u", ".join([u"u\"{}\"".format(item) for item in entry])) for entry in problem.data]
    )
    solutions_str = "\n".join(problem.solutions)
    return u"""
    u'''
{}
    ''',
    [
    {}
    ],
    solutions = [
        '''
{}
        '''
    ]""".format(problem.description.strip(), data_str, solutions_str.strip())




def string_to_problem(problem_string):


#     so much regexing!!!!!


    description_match = re.search(r"u'''\n(.*?)\n    '''", problem_string, re.DOTALL)
    description = description_match.group(1).strip() if description_match else ""

    #FIXED REGEX FOR DATA MATCH
    data_match = re.search(r"\[\n(.*?)\n\s*\],", problem_string, re.DOTALL)
    data_str = data_match.group(1).strip() if data_match else ""
    data_entries = []
    if data_str:
        entry_pattern = r"\(\s*u\"(.*?)\",\s*u\"(.*?)\"\s*\)"
        for entry_match in re.finditer(entry_pattern, data_str, re.DOTALL):
            entry_items = [entry_match.group(1).strip(), entry_match.group(2).strip()]
            data_entries.append(tuple(entry_items))
    # print(data_entries)

    solutions_match = re.search(r"solutions = \[\n\s*'''\n(.*?)\n\s*'''\n\s*\]", problem_string, re.DOTALL)
    solutions_str = solutions_match.group(1).strip() if solutions_match else ""
    solutions = [solutions_str]


    problem_instance = Problem(description=u"{}".format(description), data=data_entries, solutions=solutions)

    return problem_instance



def compatible_char_ipa(data):
    language = data["source_language"]
    if language.lower() == 'finnish':
        data = json.loads(json.dumps(data).replace('ä', 'æ')) # FINNISH ä --> IPA æ
        data = json.loads(json.dumps(data).replace('y', 'Y')) # new phoneme added!

    elif language.lower() == 'somali':
        data = json.loads(json.dumps(data).replace('j', 'd^z')) 
        json_str = json.dumps(data)
        json_str_replaced = json_str.replace('\u0361\u0292', '^z')
        data = json.loads(json_str_replaced)

    elif language.lower() == 'mongo':
        data = json.loads(json.dumps(data).replace('\u0361\u0292', '^z')) 
        json_str = json.dumps(data)
        json_str_replaced = json_str.replace('\u0361\u0292', '^z')
        data = json.loads(json_str_replaced)

    elif language.lower() in ['quechua', 'budukh']:
        data = json.loads(json.dumps(data).replace('\u010d', 't^s')) 
        data = json.loads(json.dumps(data).replace('\u01f0', 'd^z')) 
        json_str = json.dumps(data)
        json_str_replaced = json_str.replace('\u010d', 't^s')
        data = json.loads(json_str_replaced)

    elif language.lower() in ['estonian', 'budukh']:
        print(data)
        data = json.loads(json.dumps(data).replace('\u00f6', 'ö'))
        json_str = json.dumps(data)
        json_str_replaced = json_str.replace('\u00f6', 'ö')
        data = json.loads(json_str_replaced)

    elif language.lower() == 'movima':
        json_str = json.dumps(data)
        json_str_replaced = ''
        i = 0
        while i < len(json_str):
            if json_str[i] == ':':
                json_str_replaced += json_str[i - 1]
            else:
                json_str_replaced += json_str[i]
            i += 1
        # Load the modified JSON string back to data
        data = json.loads(json_str_replaced)

    return data


    # language = data["source_language"]

    # if language.lower() == 'finnish':
    #         print(u"I am here, this is {}".format(language))
    #         data = json.loads(json.dumps(data).replace('ä', 'æ')) #FINNISH ä --> IPA æ
    #         data = json.loads(json.dumps(data).replace('y', 'Y')) #new phoneme added!



    # if language.lower() == 'somali':
    #         print(u"I am here, this is {}".format(language))
    #         data = json.loads(json.dumps(data).replace('j', 'd^z')) 
    #         json_str = json.dumps(data)
    #         json_str_replaced = json_str.replace('\u0361\u0292', '^z')
    #         data_replaced = json.loads(json_str_replaced)

    # if language.lower() == 'mongo':
    #         print(u"I am here, this is {}".format(language))
    #         data = json.loads(json.dumps(data).replace('\u0361\u0292', '^z')) 

    #         json_str = json.dumps(data)
    #         json_str_replaced = json_str.replace('\u0361\u0292', '^z')
    #         data_replaced = json.loads(json_str_replaced)
    #         # print(data)

    # if language.lower() == 'quechua':
    #         print(u"I am here, this is {}".format(language))
    #         data = json.loads(json.dumps(data).replace('\u010d', 't^s')) 
    #         data = json.loads(json.dumps(data).replace('\u01f0', 'd^z')) 

    #         json_str = json.dumps(data)
    #         json_str_replaced = json_str.replace('\u010d', 't^s')
    #         data_replaced = json.loads(json_str_replaced)

            # print("HEYYYYY", data_replaced)
            # print(data)

    return data



# def format_phonmorph(folder_path, output_file):
#     OUR_MATRIXPROBLEMS = []

#     # for folder_path, output_file in zip(folder_paths, output_files):
#     file_list = [f for f in os.listdir(folder_path) if f.endswith('.json')]

#     for idx, file_name in enumerate(file_list):
#         with open(os.path.join(folder_path, file_name), 'r') as file:
#             data = json.load(file)
#             data = compatible_char_ipa(data)
#             language = data["source_language"]

#             if language.lower() in ['finnish', 'somali']:

#                 #TODO: THIS IS A TEMPORARY AND DEEPLY SUS FIX, I THINK J IS A CONSONANT HERE!!
#                 data = json.loads(json.dumps(data).replace('j', 'y'))


#             if language.lower() in ["tarangan", "terena", "budukh", "estonian", "movima"]:

#                 #TODO: fix! these all have phonemes that are currently NOT HANDLED in features.py "finnish", "quechua", 
#                 # need a phonology textbook -- Halle? 

#                 continue

#             # FROM HERE IS OK 

#             try:
#                 entries = data["train"]

#                 formatted_entries = [tuple(elem.replace(' ', '') for elem in entry if elem.strip()) for entry in entries] #to get it in the (u"<1>", u"<2>") format

#                 #NB:  if elem.strip() --> takes care of emmpty string

#                 problem_text = (
#                     u"{} Saujas {} Odden\n"
#                     u"Provide underlying representations and a phonological rule which will account for the following alternations."
#                 ).format(language, idx)

#                 solutions_text = u"""
#     + stem  
#     """

#                 problem_instance = Problem(
#                     description=u'''{}'''.format(problem_text),
#                     data=formatted_entries,
#                     solutions=[solutions_text.strip()]
#                 )
#                 OUR_MATRIXPROBLEMS.append(problem_instance)
            
#             except Exception as e:
#                 print(u"\n\n{}. \n Error: Problem in {} has an issue.\n\n".format(e, language))
#                 continue


#     # need codecs because  they use python 2.7 (sobbing noises)

#     with codecs.open(output_file, 'w', encoding='utf-8') as out_file:
#         for problem in OUR_MATRIXPROBLEMS:
#             out_file.write(problem_to_string(problem) + u"\n\n")

    # for problem in OUR_MATRIXPROBLEMS:
    #     print(problem_to_string(problem))
    #     print("\n")







def format_phonmorph(folder_paths, output_files):
    OUR_MATRIXPROBLEMS = []

    if len(folder_paths) != len(output_files):
        raise ValueError("Number of folder_paths must be equal to number of output_files")

    for folder_path, output_file in zip(folder_paths, output_files):
        OUR_MATRIXPROBLEMS = []
        file_list = [f for f in os.listdir(folder_path) if f.endswith('.json')]

        for idx, file_name in enumerate(file_list):
            try:
                with codecs.open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    data = compatible_char_ipa(data)
                    language = data["source_language"]
                    print(language)

                    if language.lower() in ["finnish", "tarangan", "terena", "estonian"]:

                        #FINNISH AND TARANGAN ARE INCOMPATIBLE
                        continue

                    entries = data["train"]
                    formatted_entries = [
                        tuple(elem.replace(' ', '') for elem in entry if elem.strip()) for entry in entries
                    ]

                    problem_text = (
                        u"{} Saujas {} Odden\n"
                        u"Provide underlying representations and a phonological rule which will account for the following alternations."
                    ).format(language, idx)

                    solutions_text = u"""
    + stem  
    """

                    problem_instance = Problem(
                        description=u'''{}'''.format(problem_text),
                        data=formatted_entries,
                        solutions=[solutions_text.strip()]
                    )
                    OUR_MATRIXPROBLEMS.append(problem_instance)

            except Exception as e:
                if 'language' in locals():
                    print(u"\n\n{}. \n Error: Problem in {} has an issue.\n\n".format(e, language))
                else:
                    print(u"\n\n{}. \n Error: Unknown language has an issue.\n\n".format(e))
                continue

        with codecs.open(output_file, 'w', encoding='utf-8') as out_file:
            for problem in OUR_MATRIXPROBLEMS:
                out_file.write(problem_to_string(problem) + u"\n\n")
        OUR_MATRIXPROBLEMS = []




# folder_path = '../../datasets/phon_morph_problems/morphology'
# output_file = '../../datasets/phon_morph_problems/morphology/morph_bpl_format.txt'

folder_paths = ['../../datasets/phon_morph_problems/morphology', '../../datasets/phon_morph_problems/multilingual', ]
                #'../../datasets/phon_morph_problems/stress', '../../datasets/phon_morph_problems/transliteration']
output_files = [i + "/bpl_format.txt" for i in folder_paths]

format_phonmorph(folder_paths, output_files)

def small_test_run():
    file_path = 'FLAG_grabbed.txt' 

    print("\nEntering small_test to load data.\n")

    with codecs.open(file_path, 'r', encoding='utf-8') as file:
        problem_strings = file.read().split("""+ stem
            '''
        ]""")  # split at end 
        for problem_string in problem_strings:
            if problem_string.strip():  # Ensure it's not an empty string
                problem_string += """+ stem
            '''
        ]"""    #adding back the thing we split based on 

                problem_instance = string_to_problem(problem_string.strip())






#COMMENTING THIS OUT RN BECAUSE IT"S IN THE SMALL_TEST_AUTO FILE -- JUL 10 AFTERNOON

# file_path = output_file 

# with codecs.open(file_path, 'r', encoding='utf-8') as file:
#     problem_strings = file.read().split("""+ stem
#         '''
#     ]""")  # split at end 
#     for problem_string in problem_strings:
#         if problem_string.strip():  # Ensure it's not an empty string
#             problem_string += """+ stem
#         '''
#     ]"""    #adding back the thing we split based on 

#             problem_instance = string_to_problem(problem_string.strip())
            

            # print("YOOO\n")



# def string_to_problem(problem_string):

#     #so much regexing!!!!!


#     description_match = re.search(r"u'''\n(.*?)\n    '''", problem_string, re.DOTALL)
#     description = description_match.group(1).strip() if description_match else ""
    

#     data_match = re.search(r"\[\n(.*?)\n\]", problem_string, re.DOTALL)
#     data_str = data_match.group(1).strip() if data_match else ""
#     data_entries = []
#     for entry in re.findall(r"\((.*?)\)", data_str):
#         entry_items = entry.split(", ")
#         entry_items = [item.replace("u\"", "").replace("\"", "") for item in entry_items]
#         data_entries.append(tuple(entry_items))
    

#     solutions_match = re.search(r"solutions = \[\n(.*?)\n\]", problem_string, re.DOTALL)
#     solutions_str = solutions_match.group(1).strip() if solutions_match else ""
#     solutions = [solutions_str]
    

#     problem_instance = Problem(
#         description=u"{}".format(description),
#         data=data_entries,
#         solutions=solutions
#     )
    
#     return problem_instance




    # data_match = re.search(r"\[\n(.*?)\n\]", problem_string, re.DOTALL)
    # data_str = data_match.group(1).strip() if data_match else ""
    # print("DIATA", data_str)
    # data_entries = []
    # for entry in re.findall(r"\((.*?)\)", data_str):
    #     entry_items = entry.split(", ")
    #     entry_items = [item.replace("u\"", "").replace("\"", "") for item in entry_items]
    #     data_entries.append(tuple(entry_items))


    # solutions_match = re.search(r"solutions = \[\n(.*?)\n\]", problem_string, re.DOTALL)
    # print("KJSGF:  ", solutions_match)
    # solutions_str = solutions_match.group(1).strip() if solutions_match else ""
    # print("OSLSNLSKNDGLFSF:  ", solutions_str)
    # solutions = [solutions_str]


    # if data_str:
    #     for entry in re.findall(r"\(\n\s*(.*?)\n\s*\)", data_str, re.DOTALL):
    #         entry_items = entry.split(",\n")
    #         entry_items = [item.strip().replace("u\"", "").replace("\"", "") for item in entry_items]
    #         data_entries.append(tuple(entry_items))