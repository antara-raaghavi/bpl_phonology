# # # # # -*- coding: utf-8 -*-
# # # # import re
# # # # import json
# # # # import argparse
# # # # import codecs


# # # # from FLAG_our_features import *


# # # # def parse_rule(rule):
# # # #     match = re.match(r'rule: \[([^\]]*)\] ---> ([^/]+) / ([^_]*)_([^$]*)$', rule.strip())
# # # #     if not match:
# # # #         match = re.match(r'rule: ([^\[\]]+) ---> ([^/]+) / ([^_]*)_([^$]*)$', rule.strip())
# # # #     if match:
# # # #         target, replacement, left_context, right_context = match.groups()
# # # #         target = target.strip()
# # # #         replacement = replacement.strip()
# # # #         left_context = left_context.strip()
# # # #         right_context = right_context.strip()
# # # #         print("\n\n\n")
# # # #         print("Target:", target, "\n Replacement: ", replacement, "\n Left and right context: ", left_context, right_context)
# # # #         print("\n\n\n")
# # # #         return target, replacement, left_context, right_context
# # # #     else:
# # # #         raise ValueError(u"Invalid rule format: {}".format(rule))

# # # # def apply_rule(word, rule, feature_bank):
# # # #     try:
# # # #         target, replacement, left_context, right_context = parse_rule(rule)
# # # #     except ValueError as e:
# # # #         print(e)
# # # #         return word

# # # #     tokens = tokenize(word)
# # # #     new_tokens = tokens[:]

# # # #     # Apply the rule
# # # #     for i in range(len(tokens)):
# # # #         if matches_context(tokens, i, left_context, right_context, feature_bank):
# # # #             if matches_target(tokens[i], target, feature_bank):
# # # #                 new_tokens[i] = apply_replacement(tokens[i], replacement, feature_bank)

# # # #     # Convert tokens back to characters
# # # #     result_word = ''.join(new_tokens)
# # # #     return result_word

# # # # def matches_context(tokens, index, left_context, right_context, feature_bank):
# # # #     # Check left context
# # # #     if left_context:
# # # #         if index == 0 or not matches_target(tokens[index - 1], left_context, feature_bank):
# # # #             return False

# # # #     # Check right context
# # # #     if right_context:
# # # #         if index >= len(tokens) - 1 or not matches_target(tokens[index + 1], right_context, feature_bank):
# # # #             return False

# # # #     return True

# # # # def matches_target(token, target, feature_bank):
# # # #     if not target:  # Empty target matches any token
# # # #         return True
# # # #     target_features = set(token_to_features(target, feature_bank))
# # # #     token_features = set(token_to_features(token, feature_bank))
# # # #     return target_features.issubset(token_features)

# # # # def apply_replacement(token, replacement, feature_bank):
# # # #     if replacement == u"Ø":
# # # #         return u""
# # # #     replacement_features = set(token_to_features(replacement, feature_bank))
# # # #     for char, features in feature_bank.featureMap.items():
# # # #         if set(features) == replacement_features:
# # # #             return char
# # # #     return replacement  # If no exact match found, return the replacement as-is

# # # # def token_to_features(token, feature_bank):
# # # #     return feature_bank.featureMap.get(token, [])

# # # # def process_data(data, rules, feature_bank):
# # # #     results = []
# # # #     for entry in data["test"]:
# # # #         underlying_form = entry[0]
# # # #         result_forms = [underlying_form]

# # # #         # Apply rules to generate each surface form
# # # #         for rule in rules:
# # # #             temp_result_forms = []
# # # #             for form in result_forms:
# # # #                 new_form = apply_rule(form, rule, feature_bank)
# # # #                 temp_result_forms.append(new_form)
# # # #                 print(u"Applying rule: {} to {} resulted in {}".format(rule, form, new_form))  # Debug statement
# # # #             result_forms = temp_result_forms

# # # #         # Fill in the "?" fields
# # # #         for i in range(1, len(entry)):
# # # #             if entry[i] == "?":
# # # #                 entry[i] = result_forms[i - 1]

# # # #         results.append(entry)

# # # #     return results

# # # # def read_rules_from_text(file_path):
# # # #     with codecs.open(file_path, "r", encoding="utf-8") as file:
# # # #         content = file.read()

# # # #     # Split the content into different solutions
# # # #     solutions = re.split(r'COST =', content)
# # # #     parsed_solutions = []

# # # #     for solution in solutions:
# # # #         if "rule:" in solution:
# # # #             rules = re.findall(r'rule:.*', solution)
# # # #             parsed_solutions.append(rules)

# # # #     return parsed_solutions

# # # # def main(json_filepath, text_filepath):
# # # #     # Load data from the JSON file
# # # #     with codecs.open(json_filepath, "r", encoding="utf-8") as file:
# # # #         data = json.load(file)

# # # #     # Read rules from the text file
# # # #     rules_sets = read_rules_from_text(text_filepath)

# # # #     # Create a dictionary to store all results
# # # #     all_results = {}

# # # #     # Process each set of rules and save results under different fields
# # # #     for idx, rules in enumerate(rules_sets):
# # # #         # Create a FeatureBank instance
# # # #         feature_bank = FeatureBank([entry[0] for entry in data["test"]])

# # # #         # Process the test set with the current set of rules
# # # #         processed_test_set = process_data(data, rules, feature_bank)

# # # #         # Save the results under a new field in the all_results dictionary
# # # #         all_results["solution_{}".format(idx+1)] = {"test": processed_test_set, "rules": rules}

# # # #     # Write all results to a new JSON file
# # # #     output_filepath = "FLAG_debugruleapplication.json"
# # # #     with codecs.open(output_filepath, "w", encoding="utf-8") as file:
# # # #         json.dump(all_results, file, ensure_ascii=False, indent=4)





# # # # if __name__ == "__main__":
# # # #     parser = argparse.ArgumentParser(description="Process phonological rules.")
# # # #     parser.add_argument("json_filepath", help="Path to the JSON file containing the test set.")
# # # #     parser.add_argument("text_filepath", help="Path to the text file containing the rules.")
# # # #     args = parser.parse_args()

# # # #     main(args.json_filepath, args.text_filepath)


# # # # # def parse_rule(rule):
# # # # #     match = re.match(r'rule: \[([^\]]*)\] ---> ([^/]+) / ([^_]*)_([^$]*)$', rule.strip())
# # # # #     if not match:
# # # # #         match = re.match(r'rule: ([^\[\]]+) ---> ([^/]+) / ([^_]*)_([^$]*)$', rule.strip())
# # # # #     if match:
# # # # #         target, replacement, left_context, right_context = match.groups()
# # # # #         target = target.strip()
# # # # #         replacement = replacement.strip()
# # # # #         left_context = left_context.strip()
# # # # #         right_context = right_context.strip()
# # # # #         return target, replacement, left_context, right_context
# # # # #     else:
# # # # #         raise ValueError(u"Invalid rule format: {}".format(rule))

# # # # # def apply_rule(word, rule, feature_bank):
# # # # #     try:
# # # # #         target, replacement, left_context, right_context = parse_rule(rule)
# # # # #     except ValueError as e:
# # # # #         print(e)
# # # # #         return word
    
# # # # #     # Tokenize the word
# # # # #     tokens = tokenize(word)
# # # # #     new_tokens = tokens[:]
    
# # # # #     # Apply the rule
# # # # #     for i in range(len(tokens)):
# # # # #         if matches_context(tokens, i, left_context, right_context, feature_bank):
# # # # #             if matches_target(tokens[i], target, feature_bank):
# # # # #                 new_tokens[i] = apply_replacement(tokens[i], replacement, feature_bank)
    
# # # # #     # Convert tokens back to characters
# # # # #     result_word = ''.join(new_tokens)
# # # # #     return result_word

# # # # # def matches_context(tokens, index, left_context, right_context, feature_bank):
# # # # #     # Check left context
# # # # #     if left_context:
# # # # #         if index == 0 or not matches_target(tokens[index - 1], left_context, feature_bank):
# # # # #             return False
    
# # # # #     # Check right context
# # # # #     if right_context:
# # # # #         if index == len(tokens) - 1 or not matches_target(tokens[index + 1], right_context, feature_bank):
# # # # #             return False
    
# # # # #     return True

# # # # # def matches_target(token, target, feature_bank):
# # # # #     target_features = set(token_to_features(target, feature_bank))
# # # # #     token_features = set(token_to_features(token, feature_bank))
    
# # # # #     return target_features.issubset(token_features)

# # # # # def apply_replacement(token, replacement, feature_bank):
# # # # #     if replacement == u"Ø":
# # # # #         return u""
# # # # #     replacement_features = set(token_to_features(replacement, feature_bank))
# # # # #     for char, features in feature_bank.featureMap.items():
# # # # #         if set(features) == replacement_features:
# # # # #             return char
# # # # #     return replacement  # If no exact match found, return the replacement as-is

# # # # # def process_data(data, rules, feature_bank):
# # # # #     results = []
# # # # #     for entry in data["test"]:
# # # # #         underlying_form = entry[0]
# # # # #         result_forms = [underlying_form]
        
# # # # #         # Apply rules to generate each surface form
# # # # #         for rule in rules:
# # # # #             temp_result_forms = []
# # # # #             for form in result_forms:
# # # # #                 new_form = apply_rule(form, rule, feature_bank)
# # # # #                 temp_result_forms.append(new_form)
# # # # #                 print(u"Applying rule: {} to {} resulted in {}".format(rule, form, new_form))  # Debug statement
# # # # #             result_forms = temp_result_forms
        
# # # # #         # Fill in the "?" fields
# # # # #         for i in range(1, len(entry)):
# # # # #             if entry[i] == "?":
# # # # #                 entry[i] = result_forms[i - 1]
        
# # # # #         results.append(entry)
    
# # # # #     return results


# # # # # def token_to_features(token, feature_bank):
# # # # #     return feature_bank.featureMap.get(token, [])


# # # # # def read_rules_from_text(file_path):
# # # # #     with codecs.open(file_path, "r", encoding="utf-8") as file:
# # # # #         content = file.read()

# # # # #     # Split the content into different solutions
# # # # #     solutions = re.split(r'COST =', content)
# # # # #     parsed_solutions = []

# # # # #     for solution in solutions:
# # # # #         if "rule:" in solution:
# # # # #             rules = re.findall(r'rule:.*', solution)
# # # # #             parsed_solutions.append(rules)
    
# # # # #     return parsed_solutions

# # # # # def main(json_filepath, text_filepath):
# # # # #     # Load data from the JSON file
# # # # #     with codecs.open(json_filepath, "r", encoding="utf-8") as file:
# # # # #         data = json.load(file)
    
# # # # #     # Read rules from the text file
# # # # #     rules_sets = read_rules_from_text(text_filepath)
    
# # # # #     # Create a dictionary to store all results
# # # # #     all_results = {}

# # # # #     # Process each set of rules and save results under different fields
# # # # #     for idx, rules in enumerate(rules_sets):
# # # # #         # Create a FeatureBank instance
# # # # #         feature_bank = FeatureBank([entry[0] for entry in data["test"]])
        
# # # # #         # Process the test set with the current set of rules
# # # # #         processed_test_set = process_data(data, rules, feature_bank)
        
# # # # #         # Save the results under a new field in the all_results dictionary
# # # # #         all_results["solution_{}".format(idx+1)] = {"test": processed_test_set, "rules": rules}
    
# # # # #     # Write all results to a new JSON file
# # # # #     output_filepath = "FLAG_testapplysolution.json"
# # # # #     with codecs.open(output_filepath, "w", encoding="utf-8") as file:
# # # # #         json.dump(all_results, file, ensure_ascii=False, indent=4)

# # # # # if __name__ == "__main__":
# # # # #     parser = argparse.ArgumentParser(description="Process phonological rules.")
# # # # #     parser.add_argument("json_filepath", help="Path to the JSON file containing the test set.")
# # # # #     parser.add_argument("text_filepath", help="Path to the text file containing the rules.")
# # # # #     args = parser.parse_args()

# # # # #     main(args.json_filepath, args.text_filepath)


# # # # -*- coding: utf-8 -*-
# # # import re
# # # import json
# # # import argparse
# # # import codecs
# # # from FLAG_our_features import *

# # # def parse_rule(rule):
# # #     match = re.match(r'rule: \[([^\]]*)\] ---> ([^/]+) / ([^_]*)_([^$]*)$', rule.strip())
# # #     if not match:
# # #         match = re.match(r'rule: ([^\[\]]+) ---> ([^/]+) / ([^_]*)_([^$]*)$', rule.strip())
# # #     if match:
# # #         target, replacement, left_context, right_context = match.groups()
# # #         target = target.strip()
# # #         replacement = replacement.strip()
# # #         left_context = left_context.strip()
# # #         right_context = right_context.strip()
# # #         print("\n\n\n")
# # #         print("Target:", target, "\nReplacement: ", replacement, "\nLeft and right context: ", left_context, right_context)
# # #         print("\n\n\n")
# # #         return target, replacement, left_context, right_context
# # #     else:
# # #         raise ValueError(u"Invalid rule format: {}".format(rule))

# # # def apply_rule(word, rule, feature_bank):
# # #     try:
# # #         target, replacement, left_context, right_context = parse_rule(rule)
# # #     except ValueError as e:
# # #         print(e)
# # #         return word

# # #     tokens = tokenize(word)
# # #     new_tokens = tokens[:]

# # #     # Check if the target phoneme is in the word
# # #     target_found = any(matches_target(token, target, feature_bank) for token in tokens)
# # #     print(u"Checking if target phoneme '{}' is in word '{}': {}".format(target, word, target_found).encode('utf-8'))
# # #     if target and not target_found:
# # #         print(u"Target phoneme not found in the word. Skipping rule application.".encode('utf-8'))
# # #         return word

# # #     # Apply the rule
# # #     for i in range(len(tokens)):
# # #         if matches_target(tokens[i], target, feature_bank):
# # #             if matches_context(tokens, i, left_context, right_context, feature_bank):
# # #                 new_tokens[i] = apply_replacement(tokens[i], replacement, feature_bank)

# # #     # Convert tokens back to characters
# # #     result_word = ''.join(new_tokens)
# # #     return result_word

# # # def matches_target(token, target, feature_bank):
# # #     if not target:  # Empty target matches any token
# # #         return True
# # #     target_features = set(token_to_features(target, feature_bank))
# # #     token_features = set(token_to_features(token, feature_bank))
# # #     print(u"Comparing token '{}' with target '{}'".format(token, target).encode('utf-8'))
# # #     print(u"Token features: {}, Target features: {}".format(token_features, target_features).encode('utf-8'))
# # #     return target_features.issubset(token_features)


# # # # def apply_rule(word, rule, feature_bank):
# # # #     try:
# # # #         target, replacement, left_context, right_context = parse_rule(rule)
# # # #     except ValueError as e:
# # # #         print(e)
# # # #         return word

# # # #     tokens = tokenize(word)
# # # #     new_tokens = tokens[:]

# # # #     # Check if the target phoneme is in the word
# # # #     if target and not any(matches_target(token, target, feature_bank) for token in tokens):
# # # #         print("IM HERE I DONT MATCH")
# # # #         return word

# # # #     # Apply the rule
# # # #     for i in range(len(tokens)):
# # # #         if matches_target(tokens[i], target, feature_bank):
# # # #             if matches_context(tokens, i, left_context, right_context, feature_bank):
# # # #                 new_tokens[i] = apply_replacement(tokens[i], replacement, feature_bank)

# # # #     # Convert tokens back to characters
# # # #     result_word = ''.join(new_tokens)
# # # #     return result_word

# # # def matches_context(tokens, index, left_context, right_context, feature_bank):
# # #     # Check left context
# # #     if left_context:
# # #         if index == 0 or not matches_target(tokens[index - 1], left_context, feature_bank):
# # #             return False

# # #     # Check right context
# # #     if right_context:
# # #         if index >= len(tokens) - 1 or not matches_target(tokens[index + 1], right_context, feature_bank):
# # #             return False

# # #     return True

# # # # def matches_target(token, target, feature_bank):
# # # #     if not target:  # Empty target matches any token
# # # #         return True
# # # #     target_features = set(token_to_features(target, feature_bank))
# # # #     token_features = set(token_to_features(token, feature_bank))
# # # #     return target_features.issubset(token_features)

# # # def apply_replacement(token, replacement, feature_bank):
# # #     if replacement == u"Ø":
# # #         return u""
# # #     replacement_features = set(token_to_features(replacement, feature_bank))
# # #     for char, features in feature_bank.featureMap.items():
# # #         if set(features) == replacement_features:
# # #             return char
# # #     return replacement  # If no exact match found, return the replacement as-is

# # # def token_to_features(token, feature_bank):
# # #     return feature_bank.featureMap.get(token, [])

# # # def process_data(data, rules, feature_bank):
# # #     results = []
# # #     for entry in data["test"]:
# # #         underlying_form = entry[0]
# # #         result_forms = [underlying_form]


# # #         # Apply rules to generate each surface form
# # #         for rule in rules:
# # #             temp_result_forms = []
# # #             for form in result_forms:
# # #                 print(form, "HEY IM AFORM")
# # #                 new_form = apply_rule(form, rule, feature_bank)
# # #                 temp_result_forms.append(new_form)
# # #                 print(u"Applying rule: {} to {} resulted in {}".format(rule, form, new_form))  # Debug statement
# # #             result_forms = temp_result_forms

# # #         # Fill in the "?" fields
# # #         for i in range(1, len(entry)):
# # #             if entry[i] == "?":
# # #                 entry[i] = result_forms[i - 1]

# # #         results.append(entry)

# # #     return results

# # # def read_rules_from_text(file_path):
# # #     with codecs.open(file_path, "r", encoding="utf-8") as file:
# # #         content = file.read()

# # #     # Split the content into different solutions
# # #     solutions = re.split(r'COST =', content)
# # #     parsed_solutions = []

# # #     for solution in solutions:
# # #         if "rule:" in solution:
# # #             rules = re.findall(r'rule:.*', solution)
# # #             parsed_solutions.append(rules)

# # #     return parsed_solutions

# # # def main(json_filepath, text_filepath):
# # #     # Load data from the JSON file
# # #     with codecs.open(json_filepath, "r", encoding="utf-8") as file:
# # #         data = json.load(file)

# # #     # Read rules from the text file
# # #     rules_sets = read_rules_from_text(text_filepath)

# # #     # Create a dictionary to store all results
# # #     all_results = {}

# # #     # Process each set of rules and save results under different fields
# # #     for idx, rules in enumerate(rules_sets):
# # #         # Create a FeatureBank instance
# # #         feature_bank = FeatureBank([entry[0] for entry in data["test"]])

# # #         # Process the test set with the current set of rules
# # #         processed_test_set = process_data(data, rules, feature_bank)

# # #         # Save the results under a new field in the all_results dictionary
# # #         all_results["solution_{}".format(idx+1)] = {"test": processed_test_set, "rules": rules}

# # #     # Write all results to a new JSON file
# # #     output_filepath = "FLAG_debugruleapplication.json"
# # #     with codecs.open(output_filepath, "w", encoding="utf-8") as file:
# # #         json.dump(all_results, file, ensure_ascii=False, indent=4)

# # # if __name__ == "__main__":
# # #     parser = argparse.ArgumentParser(description="Process phonological rules.")
# # #     parser.add_argument("json_filepath", help="Path to the JSON file containing the test set.")
# # #     parser.add_argument("text_filepath", help="Path to the text file containing the rules.")
# # #     args = parser.parse_args()

# # #     main(args.json_filepath, args.text_filepath)

# # # -*- coding: utf-8 -*-
# # import re
# # import json
# # import argparse
# # import codecs
# # from FLAG_our_features import *

# # def parse_rule(rule):
# #     match = re.match(r'rule: \[([^\]]*)\] ---> ([^/]+) / ([^_]*)_([^$]*)$', rule.strip())
# #     if not match:
# #         match = re.match(r'rule: ([^\[\]]+) ---> ([^/]+) / ([^_]*)_([^$]*)$', rule.strip())
# #     if match:
# #         target, replacement, left_context, right_context = match.groups()
# #         target = target.strip()
# #         replacement = replacement.strip()
# #         left_context = left_context.strip()
# #         right_context = right_context.strip()
# #         # print(u"\n\n\n")
# #         # print(u"Target:", target, u"\nReplacement: ", replacement, u"\nLeft and right context: ", left_context, right_context)
# #         # print(u"\n\n\n")
# #         return target, replacement, left_context, right_context
# #     else:
# #         raise ValueError(u"Invalid rule format: {}".format(rule))

# # def apply_rule(word, rule, feature_bank):
# #     try:
# #         target, replacement, left_context, right_context = parse_rule(rule)
# #     except ValueError as e:
# #         print(e)
# #         return word

# #     tokens = tokenize(word)
# #     new_tokens = tokens[:]

# #     # Check if the target phoneme is in the word
# #     target_found = any(matches_target(token, target, feature_bank) for token in tokens)
# #     print(u"Checking if target phoneme '{}' is in word '{}': {}".format(target, word, target_found))
# #     if target and not target_found:
# #         print(u"Target phoneme not found in the word. Skipping rule application.")
# #         return word

# #     # Apply the rule
# #     for i in range(len(tokens)):
# #         if matches_target(tokens[i], target, feature_bank):
# #             if matches_context(tokens, i, left_context, right_context, feature_bank):
# #                 new_tokens[i] = apply_replacement(tokens[i], replacement, feature_bank)

# #     # Convert tokens back to characters
# #     result_word = ''.join(new_tokens)
# #     return result_word

# # def matches_context(tokens, index, left_context, right_context, feature_bank):
# #     # Check left context
# #     if left_context:
# #         if index == 0 or not matches_target(tokens[index - 1], left_context, feature_bank):
# #             return False

# #     # Check right context
# #     if right_context:
# #         if index >= len(tokens) - 1 or not matches_target(tokens[index + 1], right_context, feature_bank):
# #             return False

# #     return True

# # def parse_feature_string(feature_string):
# #     feature_list = re.split(r'\s+', feature_string.strip('[]'))
# #     return set(f for f in feature_list if f)  # Remove empty strings

# # def token_to_features(token, feature_bank):
# #     return set(feature_bank.featureMap.get(token, []))

# # def matches_target(token, target, feature_bank):
# #     if not target:  # Empty target matches any token
# #         return True

# #     if len(target) == 1:  # Direct character match for single phonemes
# #         return token == target

# #     target_features = parse_feature_string(target)
# #     token_features = token_to_features(token, feature_bank)
# #     print(u"\n\n\n")
# #     print(u"Comparing token '{}' with target '{}'".format(token, target))
# #     print(u"Token features: {}, Target features: {}".format(token_features, target_features))
# #     for feature in target_features:
# #         if feature.startswith('+'):
# #             if feature[1:] not in token_features:
# #                 return False
# #         elif feature.startswith('-'):
# #             if feature[1:] in token_features:
# #                 return False
# #     return True

# # def apply_replacement(token, replacement, feature_bank):
# #     if replacement == u"Ø":
# #         return u""
# #     replacement_features = set(token_to_features(replacement, feature_bank))
# #     for char, features in feature_bank.featureMap.items():
# #         if set(features) == replacement_features:
# #             return char
# #     return replacement  # If no exact match found, return the replacement as-is

# # def process_data(data, rules, feature_bank):
# #     results = []
# #     for entry in data["test"]:
# #         underlying_form = entry[0]
# #         result_forms = [underlying_form]

# #         # Apply rules to generate each surface form
# #         for rule in rules:
# #             temp_result_forms = []
# #             for form in result_forms:
# #                 new_form = apply_rule(form, rule, feature_bank)
# #                 temp_result_forms.append(new_form)
# #                 print(u"Applying rule: {} to {} resulted in {}".format(rule, form, new_form))  # Debug statement
# #             result_forms = temp_result_forms

# #         # Fill in the "?" fields
# #         for i in range(1, len(entry)):
# #             if entry[i] == "?":
# #                 entry[i] = result_forms[i - 1]

# #         results.append(entry)

# #     return results

# # def read_rules_from_text(file_path):
# #     with codecs.open(file_path, "r", encoding="utf-8") as file:
# #         content = file.read()

# #     # Split the content into different solutions
# #     solutions = re.split(r'COST =', content)
# #     parsed_solutions = []

# #     for solution in solutions:
# #         if "rule:" in solution:
# #             rules = re.findall(r'rule:.*', solution)
# #             parsed_solutions.append(rules)

# #     return parsed_solutions

# # def main(json_filepath, text_filepath):
# #     # Load data from the JSON file
# #     with codecs.open(json_filepath, "r", encoding="utf-8") as file:
# #         data = json.load(file)

# #     # Read rules from the text file
# #     rules_sets = read_rules_from_text(text_filepath)

# #     # Create a dictionary to store all results
# #     all_results = {}

# #     # Process each set of rules and save results under different fields
# #     for idx, rules in enumerate(rules_sets):
# #         # Create a FeatureBank instance
# #         feature_bank = FeatureBank([entry[0] for entry in data["test"]])

# #         # Process the test set with the current set of rules
# #         processed_test_set = process_data(data, rules, feature_bank)

# #         # Save the results under a new field in the all_results dictionary
# #         all_results["solution_{}".format(idx+1)] = {"test": processed_test_set, "rules": rules}

# #     # Write all results to a new JSON file
# #     output_filepath = "FLAG_debugruleapplication.json"
# #     with codecs.open(output_filepath, "w", encoding="utf-8") as file:
# #         json.dump(all_results, file, ensure_ascii=False, indent=4)

# # if __name__ == "__main__":
# #     parser = argparse.ArgumentParser(description="Process phonological rules.")
# #     parser.add_argument("json_filepath", help="Path to the JSON file containing the test set.")
# #     parser.add_argument("text_filepath", help="Path to the text file containing the rules.")
# #     args = parser.parse_args()

# #     main(args.json_filepath, args.text_filepath)




'''BEST RECENT VERSION ^^^^^^^'''

# # -*- coding: utf-8 -*-
# import re
# import json
# import argparse
# import codecs
# from FLAG_our_features import *

# def parse_rule(rule):
#     match = re.match(r'rule: \[([^\]]*)\] ---> ([^/]+) / ([^_]*)_([^$]*)$', rule.strip())
#     if not match:
#         match = re.match(r'rule: ([^\[\]]+) ---> ([^/]+) / ([^_]*)_([^$]*)$', rule.strip())
#     if match:
#         target, replacement, left_context, right_context = match.groups()
#         target = target.strip()
#         replacement = replacement.strip()
#         left_context = left_context.strip()
#         right_context = right_context.strip()
#         print(u"\n\n\n")
#         print(u"Target:", target, u"\nReplacement: ", replacement, u"\nLeft and right context: ", left_context, right_context)
#         print(u"\n\n\n")
#         return target, replacement, left_context, right_context
#     else:
#         raise ValueError(u"Invalid rule format: {}".format(rule))

# def apply_rule(word, rule, feature_bank):
#     try:
#         target, replacement, left_context, right_context = parse_rule(rule)
#     except ValueError as e:
#         print(e)
#         return word

#     tokens = tokenize(word)
#     new_tokens = tokens[:]

#     # Check if the target phoneme is in the word
#     target_found = any(matches_target(token, target, feature_bank) for token in tokens)
#     print(u"Checking if target phoneme '{}' is in word '{}': {}".format(target, word, target_found))
#     if target and not target_found:
#         print(u"Target phoneme not found in the word. Skipping rule application.")
#         return word

#     # Apply the rule
#     applied = False
#     for i in range(len(tokens)):
#         if matches_target(tokens[i], target, feature_bank):
#             if matches_context(tokens, i, left_context, right_context, feature_bank):
#                 new_tokens[i] = apply_replacement(tokens[i], replacement, feature_bank)
#                 applied = True
#                 break  # Apply only once per relevant context

#     # Convert tokens back to characters
#     result_word = ''.join(new_tokens)
#     print(u"Applying rule: {} to {} resulted in {}".format(rule, word, result_word))
#     return result_word if applied else word

# def reverse_apply_rule(word, rule, feature_bank):
#     try:
#         target, replacement, left_context, right_context = parse_rule(rule)
#     except ValueError as e:
#         print(e)
#         return word

#     tokens = tokenize(word)
#     new_tokens = tokens[:]

#     # Check if the replacement phoneme is in the word
#     replacement_found = any(matches_target(token, replacement, feature_bank) for token in tokens)
#     print(u"Checking if replacement phoneme '{}' is in word '{}': {}".format(replacement, word, replacement_found))
#     if replacement and not replacement_found:
#         print(u"Replacement phoneme not found in the word. Skipping reverse rule application.")
#         return word

#     # Apply the reverse rule
#     applied = False
#     for i in range(len(tokens)):
#         if matches_target(tokens[i], replacement, feature_bank):
#             if matches_context(tokens, i, left_context, right_context, feature_bank, reverse=True):
#                 new_tokens[i] = apply_replacement(tokens[i], target, feature_bank)
#                 applied = True
#                 break  # Apply only once per relevant context

#     # Convert tokens back to characters
#     result_word = ''.join(new_tokens)
#     print(u"Reverse applying rule: {} to {} resulted in {}".format(rule, word, result_word))
#     return result_word if applied else word

# def matches_context(tokens, index, left_context, right_context, feature_bank, reverse=False):
#     # Check left context
#     if left_context:
#         if index == 0 or not matches_target(tokens[index - 1], left_context, feature_bank, reverse):
#             return False

#     # Check right context
#     if right_context:
#         if index >= len(tokens) - 1 or not matches_target(tokens[index + 1], right_context, feature_bank, reverse):
#             return False

#     return True

# def parse_feature_string(feature_string):
#     feature_list = re.split(r'\s+', feature_string.strip('[]'))
#     return set(f for f in feature_list if f)  # Remove empty strings

# def token_to_features(token, feature_bank):
#     return set(feature_bank.featureMap.get(token, []))

# def matches_target(token, target, feature_bank, reverse=False):
#     if not target:  # Empty target matches any token
#         return True

#     if len(target) == 1 and not reverse:  # Direct character match for single phonemes
#         return token == target

#     target_features = parse_feature_string(target)
#     token_features = token_to_features(token, feature_bank)
#     print(u"Comparing token '{}' with target '{}'".format(token, target))
#     print(u"Token features: {}, Target features: {}".format(token_features, target_features))
#     for feature in target_features:
#         if feature.startswith('+'):
#             if feature[1:] not in token_features:
#                 return False
#         elif feature.startswith('-'):
#             if feature[1:] in token_features:
#                 return False
#     return True

# def apply_replacement(token, replacement, feature_bank):
#     if replacement == u"Ø":
#         return u""
#     replacement_features = set(token_to_features(replacement, feature_bank))
#     for char, features in feature_bank.featureMap.items():
#         if set(features) == replacement_features:
#             return char
#     return replacement  # If no exact match found, return the replacement as-is

# def process_data(data, rules, feature_bank, prefixes):
#     results = []
#     for entry in data["test"]:
#         for i, field in enumerate(entry):
#             if field == "?":
#                 # Get the surface form from the other form in the entry
#                 surface_form = entry[1] if i == 0 else entry[0]
#                 print(u"Surface form for entry {}: {}".format(i, surface_form))
                
#                 # Determine which prefix to use
#                 prefix = prefixes[1] if i == 0 else prefixes[0]
#                 print(u"Using prefix: {}".format(prefix))
                
#                 # Remove the prefix to get the underlying form (UR)
#                 underlying_form = surface_form[len(prefix):]
#                 print(u"Underlying form: {}".format(underlying_form))
                
#                 # Generate the form with the appropriate prefix
#                 generated_form = prefix + underlying_form
#                 print(u"Generated form before applying rules: {}".format(generated_form))
                
#                 # Apply the phonological rules
#                 for rule in rules:
#                     generated_form = apply_rule(generated_form, rule, feature_bank)
                
#                 entry[i] = generated_form
        
#         results.append(entry)
#     return results

# def reverse_process_data(data, rules, feature_bank, prefixes):
#     results = []
#     for entry in data["test"]:
#         for i, field in enumerate(entry):
#             if field == "?":
#                 # Get the surface form from the other form in the entry
#                 surface_form = entry[1] if i == 0 else entry[0]
#                 print(u"Surface form for entry {}: {}".format(i, surface_form))
                
#                 # Determine which prefix to use
#                 prefix = prefixes[1] if i == 0 else prefixes[0]
#                 print(u"Using prefix: {}".format(prefix))
                
#                 # Remove the prefix to get the underlying form (UR)
#                 underlying_form = surface_form[len(prefix):]
#                 print(u"Underlying form: {}".format(underlying_form))
                
#                 # Generate the form with the appropriate prefix
#                 generated_form = prefix + underlying_form
#                 print(u"Generated form before reverse applying rules: {}".format(generated_form))
                
#                 # Apply the phonological rules in reverse
#                 for rule in reversed(rules):
#                     generated_form = reverse_apply_rule(generated_form, rule, feature_bank)
                
#                 entry[i] = generated_form
        
#         results.append(entry)
#     return results

# def read_rules_from_text(file_path):
#     with codecs.open(file_path, "r", encoding="utf-8") as file:
#         content = file.read()

#     # Split the content into different solutions
#     solutions = re.split(r'COST =', content)
#     parsed_solutions = []

#     for solution in solutions:
#         if "rule:" in solution:
#             rules = re.findall(r'rule:.*', solution)
#             parsed_solutions.append(rules)

#     return parsed_solutions

# def main(json_filepath, text_filepath):
#     # Load data from the JSON file
#     with codecs.open(json_filepath, "r", encoding="utf-8") as file:
#         data = json.load(file)

#     # Read rules from the text file
#     rules_sets = read_rules_from_text(text_filepath)

#     # Define the prefixes for the forms
#     prefixes = [u"ma", u"di"]

#     # Create a dictionary to store all results
#     all_results = {}

#     # Process each set of rules and save results under different fields
#     for idx, rules in enumerate(rules_sets):
#         # Create a FeatureBank instance
#         feature_bank = FeatureBank([entry[0] for entry in data["test"]])

#         # Process the test set with the current set of rules
#         processed_test_set = process_data(data, rules, feature_bank, prefixes)
#         reverse_processed_test_set = reverse_process_data(data, rules, feature_bank, prefixes)

#         # Save the results under a new field in the all_results dictionary
#         all_results["solution_{}".format(idx + 1)] = {
#             "test": processed_test_set,
#             "reverse_test": reverse_processed_test_set,
#             "rules": rules,
#         }

#     # Write all results to a new JSON file
#     output_filepath = "FLAG_debugruleapplication.json"
#     with codecs.open(output_filepath, "w", encoding="utf-8") as file:
#         json.dump(all_results, file, ensure_ascii=False, indent=4)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Process phonological rules.")
#     parser.add_argument("json_filepath", help="Path to the JSON file containing the test set.")
#     parser.add_argument("text_filepath", help="Path to the text file containing the rules.")
#     args = parser.parse_args()

#     main(args.json_filepath, args.text_filepath)


# -*- coding: utf-8 -*-
import re
import json
import argparse
import codecs
from FLAG_our_features import *

def parse_rule(rule):
    match = re.match(r'rule: \[([^\]]*)\] ---> ([^/]+) / ([^_]*)_([^$]*)$', rule.strip())
    if not match:
        match = re.match(r'rule: ([^\[\]]+) ---> ([^/]+) / ([^_]*)_([^$]*)$', rule.strip())
    if match:
        target, replacement, left_context, right_context = match.groups()
        target = target.strip()
        replacement = replacement.strip()
        left_context = left_context.strip()
        right_context = right_context.strip()
        # print(u"\n\n\n")
        # print(u"Target:", target, u"\nReplacement: ", replacement, u"\nLeft and right context: ", left_context, right_context)
        # print(u"\n\n\n")
        return target, replacement, left_context, right_context
    else:
        raise ValueError(u"Invalid rule format: {}".format(rule))

def apply_rule(word, rule, feature_bank):
    try:
        target, replacement, left_context, right_context = parse_rule(rule)
    except ValueError as e:
        print(e)
        return word

    tokens = tokenize(word)
    new_tokens = tokens[:]

    # Check if the target phoneme is in the word
    target_found = any(matches_target(token, target, feature_bank) for token in tokens)
    print(u"Checking if target phoneme '{}' is in word '{}': {}".format(target, word, target_found))
    if target and not target_found:
        print(u"Target phoneme not found in the word. Skipping rule application.")
        return word

    # Apply the rule
    applied = False
    for i in range(len(tokens)):
        if matches_target(tokens[i], target, feature_bank):
            if matches_context(tokens, i, left_context, right_context, feature_bank):
                new_tokens[i] = apply_replacement(tokens[i], replacement, feature_bank)
                applied = True
                break  # Apply only once per relevant context

    # Convert tokens back to characters
    result_word = ''.join(new_tokens)
    print(u"Applying rule: {} to {} resulted in {}".format(rule, word, result_word))
    return result_word if applied else word

def reverse_apply_rule(word, rule, feature_bank):
    try:
        target, replacement, left_context, right_context = parse_rule(rule)
    except ValueError as e:
        print(e)
        return word

    tokens = tokenize(word)
    new_tokens = tokens[:]

    # Check if the replacement phoneme is in the word
    replacement_found = any(matches_target(token, replacement, feature_bank) for token in tokens)
    print(u"Checking if replacement phoneme '{}' is in word '{}': {}".format(replacement, word, replacement_found))
    if replacement and not replacement_found:
        print(u"Replacement phoneme not found in the word. Skipping reverse rule application.")
        return word

    # Apply the reverse rule
    applied = False
    for i in range(len(tokens)):
        if matches_target(tokens[i], replacement, feature_bank):
            if matches_context(tokens, i, left_context, right_context, feature_bank, reverse=True):
                new_tokens[i] = apply_replacement(tokens[i], target, feature_bank)
                applied = True
                break  # Apply only once per relevant context

    # Convert tokens back to characters
    result_word = ''.join(new_tokens)
    print(u"Reverse applying rule: {} to {} resulted in {}".format(rule, word, result_word))
    return result_word if applied else word

def matches_context(tokens, index, left_context, right_context, feature_bank, reverse=False):
    # Check left context
    if left_context:
        if index == 0 or not matches_target(tokens[index - 1], left_context, feature_bank, reverse):
            return False

    # Check right context
    if right_context:
        if index >= len(tokens) - 1 or not matches_target(tokens[index + 1], right_context, feature_bank, reverse):
            return False

    return True

def parse_feature_string(feature_string):
    feature_list = re.split(r'\s+', feature_string.strip('[]'))
    return set(f for f in feature_list if f)  # Remove empty strings

def token_to_features(token, feature_bank):
    return set(feature_bank.featureMap.get(token, []))

def matches_target(token, target, feature_bank, reverse=False):
    if not target:  # Empty target matches any token
        return True

    if len(target) == 1 and not reverse:  # Direct character match for single phonemes
        return token == target

    target_features = parse_feature_string(target)
    token_features = token_to_features(token, feature_bank)
    print(u"Comparing token '{}' with target '{}'".format(token, target))
    print(u"Token features: {}, Target features: {}".format(token_features, target_features))
    print(u"\n\n\n")
    for feature in target_features:
        if feature.startswith('+'):
            if feature[1:] not in token_features:
                return False
        elif feature.startswith('-'):
            if feature[1:] in token_features:
                return False
    return True

def apply_replacement(token, replacement, feature_bank):
    if replacement == u"Ø":
        return u""
    replacement_features = set(token_to_features(replacement, feature_bank))
    for char, features in feature_bank.featureMap.items():
        if set(features) == replacement_features:
            return char
    return replacement  # If no exact match found, return the replacement as-is

def identify_affix_type(solution_text):
    # Identify if the affix is a prefix or suffix based on the solution text
    prefix_match = re.search(r'/([^/]+)/ \+ stem', solution_text)
    suffix_match = re.search(r'stem \+ /([^/]+)/', solution_text)
    if prefix_match:
        affix = prefix_match.group(1)
        return "prefix", affix
    elif suffix_match:
        affix = suffix_match.group(1)
        return "suffix", affix
    else:
        raise ValueError("Could not determine the affix type from the solution text.")

def process_data(data, rules, feature_bank, affix_type, affix):
    results = []
    for entry in data["test"]:
        for i, field in enumerate(entry):
            if field == "?":
                # Get the surface form from the other form in the entry
                surface_form = entry[1] if i == 0 else entry[0]
                print(u"Surface form for entry {}: {}".format(i, surface_form))
                
                # Remove the affix to get the underlying form (UR)
                if affix_type == "prefix":
                    underlying_form = surface_form[len(affix):]
                else:
                    underlying_form = surface_form[:-len(affix)]
                print(u"Underlying form: {}".format(underlying_form))
                
                # Generate the form with the appropriate affix
                if affix_type == "prefix":
                    generated_form = affix + underlying_form
                else:
                    generated_form = underlying_form + affix
                print(u"Generated form before applying rules: {}".format(generated_form))
                
                # Apply the phonological rules
                for rule in rules:
                    generated_form = apply_rule(generated_form, rule, feature_bank)
                
                entry[i] = generated_form
        
        results.append(entry)
    return results

def reverse_process_data(data, rules, feature_bank, affix_type, affix):
    results = []
    for entry in data["test"]:
        for i, field in enumerate(entry):
            if field == "?":
                # Get the surface form from the other form in the entry
                surface_form = entry[1] if i == 0 else entry[0]
                print(u"Surface form for entry {}: {}".format(i, surface_form))
                
                # Remove the affix to get the underlying form (UR)
                if affix_type == "prefix":
                    underlying_form = surface_form[len(affix):]
                else:
                    underlying_form = surface_form[:-len(affix)]
                print(u"Underlying form: {}".format(underlying_form))
                
                # Generate the form with the appropriate affix
                if affix_type == "prefix":
                    generated_form = affix + underlying_form
                else:
                    generated_form = underlying_form + affix
                print(u"Generated form before reverse applying rules: {}".format(generated_form))
                
                # Apply the phonological rules in reverse
                for rule in reversed(rules):
                    generated_form = reverse_apply_rule(generated_form, rule, feature_bank)
                
                entry[i] = generated_form
        
        results.append(entry)
    return results

def read_rules_from_text(file_path):
    with codecs.open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Split the content into different solutions
    solutions = re.split(r'COST =', content)
    parsed_solutions = []

    for solution in solutions:
        if "rule:" in solution:
            rules = re.findall(r'rule:.*', solution)
            parsed_solutions.append((rules, solution.strip()))

    return parsed_solutions

def main(json_filepath, text_filepath):
    # Load data from the JSON file
    with codecs.open(json_filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Read rules from the text file
    rules_sets = read_rules_from_text(text_filepath)

    # Create a dictionary to store all results
    all_results = {}

    # Process each set of rules and save results under different fields
    for idx, (rules, solution_text) in enumerate(rules_sets):
        # Create a FeatureBank instance
        feature_bank = FeatureBank([entry[0] for entry in data["test"]])

        # Identify the affix type and affix
        affix_type, affix = identify_affix_type(solution_text)
        print(u"Affix type: {}, Affix: {}".format(affix_type, affix))

        # Process the test set with the current set of rules
        processed_test_set = process_data(data, rules, feature_bank, affix_type, affix)
        reverse_processed_test_set = reverse_process_data(data, rules, feature_bank, affix_type, affix)

        # Save the results under a new field in the all_results dictionary
        all_results["solution_{}".format(idx + 1)] = {
            "test": processed_test_set,
            "reverse_test": reverse_processed_test_set,
            "rules": rules,
        }

    # Write all results to a new JSON file
    output_filepath = "FLAG_debugruleapplication.json"
    with codecs.open(output_filepath, "w", encoding="utf-8") as file:
        json.dump(all_results, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process phonological rules.")
    parser.add_argument("json_filepath", help="Path to the JSON file containing the test set.")
    parser.add_argument("text_filepath", help="Path to the text file containing the rules.")
    args = parser.parse_args()

    main(args.json_filepath, args.text_filepath)
