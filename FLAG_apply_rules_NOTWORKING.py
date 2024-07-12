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
        return target, replacement, left_context, right_context
    else:
        raise ValueError(u"Invalid rule format: {}".format(rule))

def apply_rule(word, rule, feature_bank):
    try:
        target, replacement, left_context, right_context = parse_rule(rule)
    except ValueError as e:
        print(e)
        return word

    # Tokenize the word
    tokens = tokenize(word)
    new_tokens = tokens[:]

    # Apply the rule
    for i in range(len(tokens)):
        if matches_context(tokens, i, left_context, right_context, feature_bank):
            if matches_target(tokens[i], target, feature_bank):
                new_tokens[i] = apply_replacement(tokens[i], replacement, feature_bank)

    # Convert tokens back to characters
    result_word = ''.join(new_tokens)
    return result_word

def matches_context(tokens, index, left_context, right_context, feature_bank):
    # Check left context
    if left_context:
        if index == 0 or not matches_target(tokens[index - 1], left_context, feature_bank):
            return False

    # Check right context
    if right_context:
        if index >= len(tokens) - 1 or not matches_target(tokens[index + 1], right_context, feature_bank):
            return False

    return True

def matches_target(token, target, feature_bank):
    if not target:  # Empty target matches any token
        return True
    target_features = set(token_to_features(target, feature_bank))
    token_features = set(token_to_features(token, feature_bank))
    return target_features.issubset(token_features)

def apply_replacement(token, replacement, feature_bank):
    if replacement == u"Ø":
        return u""
    replacement_features = set(token_to_features(replacement, feature_bank))
    for char, features in feature_bank.featureMap.items():
        if set(features) == replacement_features:
            return char
    return replacement  # If no exact match found, return the replacement as-is

def token_to_features(token, feature_bank):
    return feature_bank.featureMap.get(token, [])

def process_data(data, rules, feature_bank):
    results = []
    for entry in data["test"]:
        underlying_form = entry[0]
        result_forms = [underlying_form]

        # Apply rules to generate each surface form
        for rule in rules:
            temp_result_forms = []
            for form in result_forms:
                new_form = apply_rule(form, rule, feature_bank)
                temp_result_forms.append(new_form)
                print(u"Applying rule: {} to {} resulted in {}".format(rule, form, new_form))  # Debug statement
            result_forms = temp_result_forms

        # Fill in the "?" fields
        for i in range(1, len(entry)):
            if entry[i] == "?":
                entry[i] = result_forms[i - 1]

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
            parsed_solutions.append(rules)

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
    for idx, rules in enumerate(rules_sets):
        # Create a FeatureBank instance
        feature_bank = FeatureBank([entry[0] for entry in data["test"]])

        # Process the test set with the current set of rules
        processed_test_set = process_data(data, rules, feature_bank)

        # Save the results under a new field in the all_results dictionary
        all_results["solution_{}".format(idx+1)] = {"test": processed_test_set, "rules": rules}

    # Write all results to a new JSON file
    output_filepath = "processed_data_all_solutions.json"
    with codecs.open(output_filepath, "w", encoding="utf-8") as file:
        json.dump(all_results, file, ensure_ascii=False, indent=4)


def test_rule_application():
    feature_bank = FeatureBank(["x", "i", "dh", "a", "y"])
    input_word = "x i dh a y"
    rule = "rule: t ---> d / [ -liquid -sibilant ] _ [ +vowel ]"

    # Expected output is the same as input because there is no 't'
    expected_output = "x i dh a y"

    # Tokenize the input
    tokens = tokenize(input_word)

    # Apply the rule
    result = apply_rule(input_word, rule, feature_bank)

    # Debugging: Show tokens and rule application process
    print("Tokens:", tokens)
    print("Applying rule: {} to {} resulted in {}".format(rule, input_word, result))

    # Check if the output matches the expected output
    assert result == expected_output, "Test failed: expected {}, got {}".format(expected_output, result)

# Run the test
test_rule_application()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process phonological rules.")
    parser.add_argument("json_filepath", help="Path to the JSON file containing the test set.")
    parser.add_argument("text_filepath", help="Path to the text file containing the rules.")
    args = parser.parse_args()

    main(args.json_filepath, args.text_filepath)


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
#         return target, replacement, left_context, right_context
#     else:
#         raise ValueError(u"Invalid rule format: {}".format(rule))

# def apply_rule(word, rule, feature_bank):
#     try:
#         target, replacement, left_context, right_context = parse_rule(rule)
#     except ValueError as e:
#         print(e)
#         return word
    
#     # Tokenize the word
#     tokens = tokenize(word)
#     new_tokens = tokens[:]
    
#     # Apply the rule
#     for i in range(len(tokens)):
#         if matches_context(tokens, i, left_context, right_context, feature_bank):
#             if matches_target(tokens[i], target, feature_bank):
#                 new_tokens[i] = apply_replacement(tokens[i], replacement, feature_bank)
    
#     # Convert tokens back to characters
#     result_word = ''.join(new_tokens)
#     return result_word

# def matches_context(tokens, index, left_context, right_context, feature_bank):
#     # Check left context
#     if left_context:
#         if index == 0 or not matches_target(tokens[index - 1], left_context, feature_bank):
#             return False
    
#     # Check right context
#     if right_context:
#         if index == len(tokens) - 1 or not matches_target(tokens[index + 1], right_context, feature_bank):
#             return False
    
#     return True

# def matches_target(token, target, feature_bank):
#     target_features = set(token_to_features(target, feature_bank))
#     token_features = set(token_to_features(token, feature_bank))
    
#     return target_features.issubset(token_features)

# def apply_replacement(token, replacement, feature_bank):
#     if replacement == u"Ø":
#         return u""
#     replacement_features = set(token_to_features(replacement, feature_bank))
#     for char, features in feature_bank.featureMap.items():
#         if set(features) == replacement_features:
#             return char
#     return replacement  # If no exact match found, return the replacement as-is

# def process_data(data, rules, feature_bank):
#     results = []
#     for entry in data["test"]:
#         underlying_form = entry[0]
#         result_forms = [underlying_form]
        
#         # Apply rules to generate each surface form
#         for rule in rules:
#             temp_result_forms = []
#             for form in result_forms:
#                 new_form = apply_rule(form, rule, feature_bank)
#                 temp_result_forms.append(new_form)
#                 print(u"Applying rule: {} to {} resulted in {}".format(rule, form, new_form))  # Debug statement
#             result_forms = temp_result_forms
        
#         # Fill in the "?" fields
#         for i in range(1, len(entry)):
#             if entry[i] == "?":
#                 entry[i] = result_forms[i - 1]
        
#         results.append(entry)
    
#     return results


# def token_to_features(token, feature_bank):
#     return feature_bank.featureMap.get(token, [])


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
    
#     # Create a dictionary to store all results
#     all_results = {}

#     # Process each set of rules and save results under different fields
#     for idx, rules in enumerate(rules_sets):
#         # Create a FeatureBank instance
#         feature_bank = FeatureBank([entry[0] for entry in data["test"]])
        
#         # Process the test set with the current set of rules
#         processed_test_set = process_data(data, rules, feature_bank)
        
#         # Save the results under a new field in the all_results dictionary
#         all_results["solution_{}".format(idx+1)] = {"test": processed_test_set, "rules": rules}
    
#     # Write all results to a new JSON file
#     output_filepath = "FLAG_testapplysolution.json"
#     with codecs.open(output_filepath, "w", encoding="utf-8") as file:
#         json.dump(all_results, file, ensure_ascii=False, indent=4)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Process phonological rules.")
#     parser.add_argument("json_filepath", help="Path to the JSON file containing the test set.")
#     parser.add_argument("text_filepath", help="Path to the text file containing the rules.")
#     args = parser.parse_args()

#     main(args.json_filepath, args.text_filepath)