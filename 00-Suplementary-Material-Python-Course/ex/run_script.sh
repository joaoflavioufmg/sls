#!/bin/sh

# self-deleting shell script: rm $0
# rm $0

# To execute permission: chmod +x script-name.sh    ...or...
# To execute permission: chmod 750 script-name.sh   ...then...
# To run your script, enter: ./script-name.sh

python "var.py"
python "hello.py"

echo "

------------------
(program exited with code: $?)"

# echo "Press return to continue"

#to be more compatible with shells like dash
# dummy_var=""
# read dummy_var

# Para rodar em segundo plano e gerar um log: nohup ./run_script.sh > log_script.txt &
