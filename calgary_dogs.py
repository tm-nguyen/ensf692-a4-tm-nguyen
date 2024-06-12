import pandas as pd

# calgary_dogs.py
# AUTHOR NAME: Tien Nguyen
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

def format_data(df):
    """
    The formats the data by stripping whitespace from column names and breed names,
    then converting breed names to uppercase, and creating a multi-index DataFrame.

    The def arguments:
        DataFrame df: DataFrame to format.
    Returns:
        DataFrame: Formatted DataFrame.
    """
    # Ensure correct data formatting by removing leading or trailing whitespace from column names
    df.columns = df.columns.str.strip()
    # Convert breed names to uppercase and remove leading or trailing whitespace
    df['Breed'] = df['Breed'].str.upper().str.strip()

    # Create a multi-index DataFrame
    df.set_index(['Breed', 'Year', 'Month'], inplace=True)
    df.sort_index(inplace=True)
    return df

def user_input(df):
    """
    Prompts the user to enter a dog breed and validates the input.
    
    The def arguments:
       DataFrame df: The dataFrame containing the dog breeds.
    Returns:
        String breed: The valid breed name
    """
    while True:
        try:
            # Prompt user to enter a dog breed and convert to uppercase and strip whitespace
            breed = input("Please enter a dog breed: ").upper().strip()
            # Check if breed is in data
            if breed not in df.index.get_level_values('Breed'):
                # Raise an error if the breed is not found
                raise ValueError("Dog breed not found in the data. Please try again.")
            # Return the prompt user to enter a dog breed 
            return breed
        # Catch ValueError exception and assign it to variable `e`
        except ValueError as e:
            # Print the error message
            print(e)

def calculate_percent(df, breed_data, year):
    """
    Calculates the percent of breed registrations in a specific year.
    
    The def arguments:
        DataFrame df: The dataFrame containing the dog breeds.
        DataFrame breed_data: The data for the specific breed.
        integer year: The year for the calculation.

    Returns:
        String: Percent of registrations or "not in the list" if there is no data.
    """
    # Sum the total of the all breed registrations in the specified year
    total_in_year = df.groupby('Year')['Total'].sum().loc[year]
    # Check if there are no registrations in the year data
    if total_in_year == 0:
        # Return the message that not in the list
        return "not in the list"
    # Take the total breed registrations in the year data
    breed_total_in_year = breed_data.loc[breed_data.index.get_level_values('Year') == year, 'Total'].sum()
    # Calculate the percentage the total of the breed registration in year with the total years.
    percent = (breed_total_in_year / total_in_year) * 100
    # Result will be returned at percentage with 6 decimal places.
    return f"{percent:.6f}%"

def data_analyze(df, breed):
    """
    Analyzes the data of the selected breed and prints the results.
    
    The def arguments:
        DataFrame df: The dataFrame containing the dog breeds.
        String breed: The breed name.

    Returns:
        DataFrame: Data for the specific breed.
    """
    # Use IndexSlice for the dog breed data slicing
    idx = pd.IndexSlice
    # Filter the DataFrame to get data for the selected breed
    breed_data = df.loc[idx[breed, :, :]]
    # Set the unique years in which the breed appears
    unique_years = breed_data.index.get_level_values('Year').unique()
    # Show the total breed registrations
    total = breed_data['Total'].sum()
    # Print the breed was found in the top breed for years
    print(f"The {breed} was found in the top breeds for years:  ", end="")
    # Use for loop to loop through the  each unique year the breed appears
    for year in unique_years:
        # Print the year the the breed appeared.
        print(year, end=" ")
    # Print the white line only  
    print()   
    # Print the total breed registrations
    print(f"There have been {total} {breed} dogs registered total.")
    
    # Loop through the year 2021, 2022, and 2023 to calculate for the breed in each specified year
    for y in [2021, 2022, 2023]:
        # Calculate the percentage for each year based on the data.
        percent = calculate_percent(df, breed_data, y)
        # Print the mesaage to show the registration percentage.
        print(f"The {breed} was {percent} of top breeds in {y}.")
    
    # The total registration of all breeds across all years.
    all_total = df['Total'].sum()
    # Calculation the overall percentage over the all total of breeds.
    overall_percent = (total / all_total) * 100
    # Show the message for the overall percentage of brees with 6 decimal places.
    print(f"The {breed} was {overall_percent:.6f}% of top breeds across all years.")
    # Return the breeds data
    return breed_data

def most_popular_months(data):
    """
    Finds the most popular months for the selected breed registrations.
    
    The def arguments:
        DataFrame data: The data for the specific breed.

    Returns:
        String: The most popular months.
    """
    # Count the number breed of registrations for each month
    month_counts = data.index.get_level_values('Month').value_counts()
    # Find the maximum count of the breed registrations in any month
    max_count = month_counts.max()
    # Get the months with the maximum count of registrations
    most_popular = month_counts[month_counts == max_count].index
    # Return the string of most popular months, joined by a space, then sort months by alphabet order
    return " ".join(str(month) for month in sorted(most_popular))

def main():

    # Import data here
    print("ENSF 692 Dogs of Calgary")

    # File path to excel file location
    path = 'CalgaryDogBreeds.xlsx'
    # Data formatting to read the excel file
    df = pd.read_excel(path)
    df = format_data(df)
    
    # Apply masking operation to filter out rows if they are less than 20.
    mask = df['Total'] > 20
    df = df[mask]

    # User input stage
    # The breed to call the def user_input that prompt the user to enter a breed dog name.
    breed = user_input(df)

    # Data anaylsis stage
    # The data to call the def analyze that will analyze, calculate the percentage of the total of breeds
    data = data_analyze(df, breed)
    # Find the most popular months for the selected breed
    popular_months = most_popular_months(data)
    # Print the most popular months for the selected breed
    print(f"Most popular month(s) for {breed} dogs:  {popular_months}")

if __name__ == '__main__':
    main()
