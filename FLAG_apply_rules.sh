#!/bin/bash

# Base directories
json_dirs=("../../datasets/phon_morph_problems/morphology" "../../datasets/phon_morph_problems/multilingual")
text_dir="FLAG_autoread_run"
output_dir="FLAG_autoread_run/results"
log_file="FLAG_apply_rules.txt"

python_script="FLAG_apply_rules_NOTWORKING.py"


extract_first_word() {
    local json_file="$1"
    
    # Extract value of the "source_language" key
    first_word=$(jq -r '.source_language' "$json_file" 2>/dev/null)
    
    if [ -z "$first_word" ]; then
        echo "Warning: Unable to extract first word from ${json_file}"
        return 1
    fi
    
    echo "${first_word}"
}

for json_dir in "${json_dirs[@]}"; do
    # Ensure JSON directory exists
    if [ ! -d "${json_dir}" ]; then
        echo "Error: Directory not found - ${json_dir}"
        continue
    fi
    

    for json_file in "${json_dir}"/*.json; do
        if [ ! -f "${json_file}" ]; then
            echo "Warning: No JSON files found in ${json_dir}"
            continue
        fi
        

        first_word=$(extract_first_word "${json_file}")
        if [ -z "${first_word}" ]; then
            echo "Warning: Unable to extract first word from ${json_file}"
            continue
        fi

        text_file=$(find "${text_dir}" -type f -name "FLAG_iter_Odden_${first_word}_Saujas*.txt" | head -n 1)
        if [ -z "${text_file}" ]; then
            echo "Warning: No text file found for ${first_word}"
            continue
        fi
        
        json_filename=$(basename "${json_file}")
        output_file="${output_dir}/${json_filename%.json}_ruleapplied.json"
        
        echo "Processing ${json_file} and ${text_file}..."
        python "${python_script}" "${json_file}" "${text_file}" > "${output_file}" 2>> "${log_file}"
        
        echo "Results written to ${output_file}"
        echo "Log appended to ${log_file}"
        echo "----------------------------------------"
    done
done

echo "All files processed."
