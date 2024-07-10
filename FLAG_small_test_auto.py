from FLAG_automate_problem_grab import *

file_path = 'FLAG_grabbed.txt' 

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
            

            # print("Working so far! \n\n")