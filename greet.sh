#! /bin/bash
#the script prompts the user for the first and last names. It then prints "Hello <firstname> <lastname>"
echo -n "Enter your first name :"
read firstname

echo -n "Enter your last name :" 
read lastname

echo "Hello $firstname $lastname"

#you can execute as a script or run using the bash command in the terminal.
#first ensure you're in the directory where the file is located.
#To execute as a script, check that the file is executable using `ls -l greet.sh`. If an `x` is in the first part of the output, it is.
#If not, change the file permission to executeable using `chmod +x greetnew.sh`.
#run the script using `.\greet.sh

#To run using bash, simply type `bash greet.sh` in the terminal.
