#!/bin/bash

# Initialize an empty array to hold unique applicant names
declare -a applicants
declare -a states
max_applicants=20

echo "Welcome to the Raffle Draw Applicant System!"
echo "You can enter up to $max_applicants applicants."

while [ ${#applicants[@]} -lt $max_applicants ]; do
    read -p "Enter the applicant's name: " name
    # Check for duplicate names
    if [[ " ${applicants[@]} " =~ " ${name} " ]]; then
        echo "This name has already been entered. Please enter a unique name."
        continue
    fi

    read -p "Enter the applicant's state: " state
    # Validate state
    if [[ "$state" == "Canberra" ]]; then
        echo "Canberra is not eligible. Please enter a different state."
        continue
    fi

    # Add valid entry to the arrays
    applicants+=("$name")
    states+=("$state")
    echo "Applicant $name from $state added successfully."

    # Check if the user wants to continue or reach the max
    if [ ${#applicants[@]} -lt $max_applicants ]; then
        read -p "Do you want to add another applicant? (yes/no): " continue_input
        if [[ "$continue_input" != "yes" ]]; then
            break
        fi
    fi
done

# Save the applicants to S298900.txt
output_file="S298900.txt"
{
    echo "Raffle Draw Applicants:"
    for i in "${!applicants[@]}"; do
        echo "${applicants[$i]} - ${states[$i]}"
    done
} > "$output_file"

echo "Applicants saved to $output_file."