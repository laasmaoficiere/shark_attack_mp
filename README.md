# Shark Attack Quest
## Project Description
For this challenge our task was to examine a data set regarding shark attacks in various parts of the world and to draw our conclusions based on previously determined hypothesis.
# Presentation
https://docs.google.com/presentation/d/1ZMm_1ivZLIj3kjznha2dCt9mWRTPAsJr69qDQP09s5E/edit#slide=id.p1
### Data Description
- **Source**: [Shark Attack File Incident Log](https://www.sharkattackfile.net/incidentlog.htm)
- **Format**: Excel
- **Structure**:
  
  - Date: Date when the attack happened
  - Year: The year the attack happened
  - Type: Type of shark attack (provoked or unprovoked)
  - Country: Country where the attack happened
  - State: State (or region) where the attack happened
  - Location: Location where the attack occurred
  - Activity: Activity being conducted when the attack happened
  - Name: Name of the person who suffered the attack
  - Sex: Gender of the person who suffered the attack
  - Age: Age of the person who suffered the attack
  - Injury: Description of the injury sustained during the attack
  - Time: Time when the attack occurred
  - Species: Species of shark involved in the attack
  - Source: Original source of the information
  - PDF: Link to the PDF file describing the attack

## Data Cleaning Steps

  - Standardizing column names
  - Drowpping the rows with all NA/zero values
  - Dropping duplicated rows 
  - Dropping columns not relevant for our project:
    - Name - does not give valuable input for our hypothesis
    - Date - we use the data in the Year column instead
    - Location - we focus on more general scope (Country/State)
    - Species - not relevant for our hypothesis

## Exploratory Data Analysis

- Obtaining the value counts for country, activity, age and time categories
- Visualising categorical variables using graphs - pie and bar charts - number of attacks per country and per time of day
- Visualising numerical variables using histograms - attacks over the past 20 years
- Creating pivot table to compare two variables - activity and fatality
