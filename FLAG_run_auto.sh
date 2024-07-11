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

OUTPUT_FILE="FLAG_auto_test.txt"
echo "Collecting output in $OUTPUT_FILE"

echo >> $OUTPUT_FILE
echo >> $OUTPUT_FILE
echo >> $OUTPUT_FILE
echo "------ Run started at $(date) ------" >> $OUTPUT_FILE
echo >> $OUTPUT_FILE

echo "TESTING AUTOREAD GRAB -- LANGSPECIFIC SUBSTITUTIONS" >> $OUTPUT_FILE
echo >> $OUTPUT_FILE
echo >> $OUTPUT_FILE

# Run the commands in sequence and append the outputs to the output file
{

    echo "Running driver.py Odden_Quechua_Saujas_3 incremental -t 100 --timeout 24 --geometry --features sophisticated"
    python driver.py Odden_Quechua_Saujas_3 incremental -t 100 --timeout 24 --geometry --features sophisticated

    echo >> $OUTPUT_FILE
    echo >> $OUTPUT_FILE

    echo "Running driver.py Odden_Somali_Saujas_4 incremental -t 100 --timeout 24 --geometry --features sophisticated"
    python driver.py Odden_Somali_Saujas_4 incremental -t 100 --timeout 24 --geometry --features sophisticated


} >> $OUTPUT_FILE 2>&1

echo >> $OUTPUT_FILE

echo "------ Run ended at $(date) ------" >> $OUTPUT_FILE

echo >> $OUTPUT_FILE

# Terminate the command server
echo "Terminating command server..."
python command_server.py KILL

echo "All tasks completed. Output collected in $OUTPUT_FILE."
