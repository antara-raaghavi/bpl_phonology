import re
import json
import os

def read_rules_from_text(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    rule_sets = []
    current_rules = []
    current_stems = []

    # Split the content into lines
    lines = content.splitlines()
    
    for line in lines:
        line = line.strip()
        
        # Check for rules
        if line.startswith("rule:"):
            if current_stems:
                # Save the current rule set before adding new rules
                rule_sets.append({
                    "rules": "\n".join(current_rules),
                    "stems": "\n".join(current_stems)
                })
                # Clear current rules and stems for the next rule set
                current_rules = []
                current_stems = []
            
            # Add the rule to the current set
            current_rules.append(line)
        
        # Check for stems
        elif re.search(r'/[^/]+/ \+ stem', line):
            current_stems.append(line)
    
    # If there are remaining rules and stems, add the last rule set
    if current_rules:
        rule_sets.append({
            "rules": "\n".join(current_rules),
            "stems": "\n".join(current_stems)
        })
    
    return rule_sets

def save_rules_to_json(rule_sets, output_file_path):
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(output_file_path, 'w') as file:
        json.dump(
            {u"rule_set_%d" % (i + 1): rule_set for i, rule_set in enumerate(rule_sets)},
            file,
            indent=4
        )

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        
        if file_name.endswith('.txt'):
            print("Processing file: %s" % file_path)
            
            rule_sets = read_rules_from_text(file_path)
            
            output_file_name = os.path.splitext(file_name)[0] + '.json'
            output_file_path = os.path.join(output_dir, output_file_name)
            
            save_rules_to_json(rule_sets, output_file_path)

def main():
    input_dir = "FLAG_autoread_run"
    output_dir = "FLAG_autoread_run/rules_only"
    
    process_directory(input_dir, output_dir)

if __name__ == "__main__":
    main()
    
