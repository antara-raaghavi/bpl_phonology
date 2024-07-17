# #!/bin/bash

# # Set the number of CPUs
# CPUs=40

# # Start the command server in the background
# echo "Starting command server with $CPUs CPUs..."
# python command_server.py $CPUs &
# export PYTHONIOENCODING=utf-8

# # Wait for the server to start
# sleep 5

# # Create an output file
# OUTPUT_FILE="testing_output.txt"
# echo "Collecting output in $OUTPUT_FILE"

# echo >> $OUTPUT_FILE
# echo "------ Run started at $(date) ------" >> $OUTPUT_FILE
# echo >> $OUTPUT_FILE

# # Run the commands in sequence and append the outputs to the output file
# {
#     echo "Running pigLatin.py -d 3 Latin"
#     python pigLatin.py -d 3 Latin

#     echo >> $OUTPUT_FILE

#     # echo "Running driver.py Odden_68_69_Russian incremental -t 100 --timeout 24 --geometry --features sophisticated"
#     # python driver.py Odden_68_69_Russian incremental -t 100 --timeout 24 --geometry --features sophisticated

#     echo "Running driver.py Odden_Mandar_Saujas_1 incremental -t 100 --timeout 24 --geometry --features sophisticated"
#     python driver.py Odden_Mandar_Saujas_1 incremental -t 100 --timeout 24 --geometry --features sophisticated

# } >> $OUTPUT_FILE 2>&1


# echo >> $OUTPUT_FILE

# echo "------ Run ended at $(date) ------" >> $OUTPUT_FILE


# # Terminate the command server
# echo "Terminating command server..."
# python command_server.py KILL

# echo "All tasks completed. Output collected in $OUTPUT_FILE."



#V2 -- AUTOREADS TEST -- REALLY MESSY 


# #!/bin/sh

# # Set the number of CPUs
# CPUs=40

# # Start the command server in the background
# echo "Starting command server with $CPUs CPUs..."
# python command_server.py $CPUs &
# export PYTHONIOENCODING=utf-8

# sleep 5

# OUTPUT_FILE="FLAG_auto_test.txt"
# echo "Collecting output in $OUTPUT_FILE"


# echo >> $OUTPUT_FILE
# echo "------ Run started at $(date) ------" >> $OUTPUT_FILE
# echo >> $OUTPUT_FILE
# echo >> $OUTPUT_FILE

# echo "TESTING AUTOREAD GRAB -- CLEANED UP" >> $OUTPUT_FILE


# # Run the commands in sequence and append the outputs to the output file
# {




#     # echo "Running driver.py Odden_Mandar_Saujas_1 incremental -t 100 --timeout 24 --geometry --features sophisticated"
#     # python driver.py Odden_Mandar_Saujas_1 incremental -t 100 --timeout 24 --geometry --features sophisticated

    
#     # echo >> $OUTPUT_FILE

#     # echo >> $OUTPUT_FILE

#     # echo "Running driver.py Odden_Lunyole_Saujas_2 incremental -t 100 --timeout 24 --geometry --features sophisticated"
#     # python driver.py Odden_Lunyole_Saujas_2 incremental -t 100 --timeout 24 --geometry --features sophisticated
    
#     # echo "Running FLAG_small_test_auto.py"
#     # python FLAG_small_test_auto.py 




#     echo "Running driver.py Odden_Quechua_Saujas_3 incremental -t 100 --timeout 24 --geometry --features sophisticated"
#     python driver.py Odden_Quechua_Saujas_3 incremental -t 100 --timeout 24 --geometry --features sophisticated

#     # echo "Running driver.py Odden_Zoque_Saujas_11 incremental -t 100 --timeout 24 --geometry --features sophisticated"
#     # python driver.py Odden_Zoque_Saujas_11 incremental -t 100 --timeout 24 --geometry --features sophisticated

#     # echo "Running driver.py Odden_Dutch_Saujas_2 incremental -t 100 --timeout 24 --geometry --features sophisticated"
#     # python driver.py Odden_Dutch_Saujas_2 incremental -t 100 --timeout 24 --geometry --features sophisticated

#     # echo "Running driver.py Odden_Mongo_Saujas_3 incremental -t 100 --timeout 24 --geometry --features sophisticated"
#     # python driver.py Odden_Mongo_Saujas_3 incremental -t 100 --timeout 24 --geometry --features sophisticated

#     # echo "Running driver.py Odden_Sursilvan_Engadine_Saujas_4 incremental -t 100 --timeout 24 --geometry --features sophisticated"
#     # python driver.py Odden_Sursilvan_Engadine_Saujas_4 incremental -t 100 --timeout 24 --geometry --features sophisticated

# } >> $OUTPUT_FILE 2>&1

# echo >> $OUTPUT_FILE

# echo "------ Run ended at $(date) ------" >> $OUTPUT_FILE

# echo >> $OUTPUT_FILE

# # Terminate the command server
# echo "Terminating command server..."
# python command_server.py KILL

# echo "All tasks completed. Output collected in $OUTPUT_FILE."


#!/bin/sh

# Set the number of CPUs
CPUs=40

# Start the command server in the background
echo "Starting command server with $CPUs CPUs..."
python command_server.py $CPUs &
export PYTHONIOENCODING=utf-8

sleep 5

# Base name for output files
BASE_OUTPUT_FILE="FLAG_iter"

# Print initial information
echo "Collecting output in ${BASE_OUTPUT_FILE}_*.txt"

echo >> "${BASE_OUTPUT_FILE}.txt"
echo >> "${BASE_OUTPUT_FILE}.txt"
echo >> "${BASE_OUTPUT_FILE}.txt"
echo "------ Run started at $(date) ------" >> "${BASE_OUTPUT_FILE}.txt"
echo >> "${BASE_OUTPUT_FILE}.txt"

echo "TESTING AUTOREAD GRAB -- ITERATIVE SHELL" >> "${BASE_OUTPUT_FILE}.txt"
echo >> "${BASE_OUTPUT_FILE}.txt"
echo >> "${BASE_OUTPUT_FILE}.txt"

# Initialize a variable to store the command server PID
COMMAND_SERVER_PID=""

# Function to find command server PID
find_command_server_pid() {
    COMMAND_SERVER_PID=$(pgrep -f "python command_server.py $CPUs")
}

# # Function to check if command server is running
# command_server_running() {
#     find_command_server_pid
#     if [ -n "$COMMAND_SERVER_PID" ]; then
#         return 0 # Server is running
#     else
#         return 1 # Server is not running
#     fi
# }

# # Check if command server is running
# if command_server_running; then
#     echo "Command server is running with PID: $COMMAND_SERVER_PID"
# else
#     echo "Command server failed to start or terminated unexpectedly."
#     exit 1
# fi

# Run the commands in sequence and append the outputs to the output file
{

    # WHY ISNT THIS WORKING NOW IT WAS WORKING FINE YDAY

    # Define the problem names
    problem_names=(
        #morphology
        # "Odden_Mandar_Saujas_1"
        # "Odden_Dutch_Saujas_2"
        # "Odden_Quechua_Saujas_3"
        # "Odden_Somali_Saujas_4"
        "Odden_Lunyole_Saujas_5"
        "Odden_Mongo_Saujas_8"
        "Odden_Indonesian_Saujas_9"
        "Odden_Zoque_Saujas_11"
        #multiling
        "Odden_Hawaiian_Saujas_1"
        "Odden_Sursilvan_Saujas_3"
        "Odden_Warlpiri_Saujas_5"
        "Odden_Minangkabau_Saujas_6"
    )

    # Iterate over the defined problem names
    for problem_name in "${problem_names[@]}"; do
        # Create a unique output file name for each problem
        OUTPUT_FILE="${BASE_OUTPUT_FILE}_${problem_name}.txt"

        echo "Running driver.py $problem_name incremental -t 100 --timeout 24 --geometry --features sophisticated" | tee -a "$OUTPUT_FILE"
        python driver.py "$problem_name" incremental -t 100 --timeout 24 --geometry --features sophisticated >> "$OUTPUT_FILE" 2>&1
        echo >> "$OUTPUT_FILE"
        echo >> "$OUTPUT_FILE"
    done

} 2>&1 | tee -a "${BASE_OUTPUT_FILE}.txt"

echo >> "${BASE_OUTPUT_FILE}.txt"
echo "------ Run ended at $(date) ------" >> "${BASE_OUTPUT_FILE}.txt"

# Terminate the command server
echo "Terminating command server..."
python command_server.py KILL

echo "All tasks completed. Output collected in ${BASE_OUTPUT_FILE}."

# OUTPUT_FILE="FLAG_auto_test.txt"
# echo "Collecting output in $OUTPUT_FILE"

# echo >> $OUTPUT_FILE
# echo >> $OUTPUT_FILE
# echo >> $OUTPUT_FILE
# echo "------ Run started at $(date) ------" >> $OUTPUT_FILE
# echo >> $OUTPUT_FILE

# echo "TESTING AUTOREAD GRAB -- ITERATIVE SHELL" >> $OUTPUT_FILE
# echo >> $OUTPUT_FILE
# echo >> $OUTPUT_FILE

# # Run the commands in sequence and append the outputs to the output file
# {

#     # echo "Running driver.py Odden_Quechua_Saujas_3 incremental -t 100 --timeout 24 --geometry --features sophisticated"
#     # python driver.py Odden_Quechua_Saujas_3 incremental -t 100 --timeout 24 --geometry --features sophisticated

#     # echo >> $OUTPUT_FILE
#     # echo >> $OUTPUT_FILE

#     # echo "Running driver.py Odden_Somali_Saujas_4 incremental -t 100 --timeout 24 --geometry --features sophisticated"
#     # python driver.py Odden_Somali_Saujas_4 incremental -t 100 --timeout 24 --geometry --features sophisticated


#     problem_names=(
#     #morphology
#     "Odden_Mandar_Saujas_1"
#     "Odden_Dutch_Saujas_2"
#     "Odden_Quechua_Saujas_3"
#     "Odden_Somali_Saujas_4"
#     "Odden_Lunyole_Saujas_5"
#     "Odden_Mongo_Saujas_8"
#     "Odden_Indonesian_Saujas_9"
#     "Odden_Zoque_Saujas_11"
#     #multiling
#     "Odden_Hawaiian_Saujas_1"
#     "Odden_Sursilvan_Saujas_3"
#     "Odden_Warlpiri_Saujas_5"
#     "Odden_Minangkabau_Saujas_6"
#     )

#     # Iterate over the defined problem names
#     for problem_name in "${problem_names[@]}"; do
#         echo "Running driver.py $problem_name incremental -t 100 --timeout 24 --geometry --features sophisticated"
#         python driver.py "$problem_name" incremental -t 100 --timeout 24 --geometry --features sophisticated
#         echo >> $OUTPUT_FILE
#         echo >> $OUTPUT_FILE
#     done



# } >> $OUTPUT_FILE 2>&1

# echo >> $OUTPUT_FILE

# echo "------ Run ended at $(date) ------" >> $OUTPUT_FILE

# echo >> $OUTPUT_FILE


