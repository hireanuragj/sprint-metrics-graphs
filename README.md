# sprint-metrics-graphs
Python code that you can run with input as a CSV file and generate sprint data metrics for your teams. 

## About
This program was created to generate unique sprint metrics apart from sprint completion hit rates. 

## How to Use
Replace the team and sprint level values in the 'sprint_data.csv' file with your team's data. Would recommend using any spreadsheet program to do this.
Run the Python program and it will generate 4 .jpg files in the same folder.

## Input
Uses a CSV file where each sprint's completion rate is input as a float number converted from the percentage.

## Output
Currently generates 4 images:
- Sprint Goal Success Rate for Each Team (where the success rate is defined as >70% completion)
- Velocity for Each Team
- Distribution of Task Completion Rates for Each Team
- Standard Deviation of Task Completion Rates
