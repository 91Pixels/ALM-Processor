import os
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Define the directory containing the HTML files
html_directory = "C:\\Users\\modsf\\Desktop\\ReportesHtml"

# Initialize counters
passed_count = 0
no_run_count = 0
not_completed_count = 0

# Loop through all files in the directory
for filename in os.listdir(html_directory):
    if filename.endswith(".html"):
        file_path = os.path.join(html_directory, filename)
        
        # Read the HTML file
        with open(file_path, 'r') as f:
            html_content = f.read()

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all <span> tags with the specified styles
        status_spans = soup.find_all('span', style=lambda value: value and 'color:#ff0000;' in value and 'font-family:\'Eras Medium ITC\';' in value and 'font-size:9pt' in value)

        # Count occurrences
        for span in status_spans:
            status_text = span.text.strip()
            if status_text == "Passed":
                passed_count += 1
            elif status_text == "No Run":
                no_run_count += 1
            elif status_text == "Not Completed":
                not_completed_count += 1

# Create a pandas DataFrame with the counts
data = {
    'Status': ['Passed', 'No Run', 'Not Completed'],
    'Count': [passed_count, no_run_count, not_completed_count]
}
df = pd.DataFrame(data)

# Calculate percentages
total_count = df['Count'].sum()
df['Percentage'] = (df['Count'] / total_count) * 100

# Create a pie chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

ax1.pie(df['Count'], labels=df['Status'], autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures the pie chart is drawn as a circle
ax1.set_title('Execution Status Distribution')

# Display the table
ax2.axis('off')
table_columns = ['Status', 'Count']
table = ax2.table(cellText=df[table_columns].values, rowLabels=df.index, colLabels=table_columns, cellLoc='center', rowLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(12)

plt.show()