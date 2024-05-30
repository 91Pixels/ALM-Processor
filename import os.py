import os
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# --- Styling Options ---
pie_colors = ['lightgreen', 'lightcoral', 'lightskyblue', 'lightgray']
explode = (0.1, 0, 0, 0)
pie_shadow = True
pie_textprops = {'fontsize': 12}
table_fontsize = 10
table_cell_colors = {
    0: 'lightgreen',
    1: 'lightcoral'
}
# --- End Styling Options ---

def adjust_pie_labels(ax, wedges, texts, autotexts, threshold=0.1):
    """Adjusts the positions of percentage labels in a pie chart to reduce overlap."""
    for i, autotext in enumerate(autotexts):
        bbox = autotext.get_window_extent()
        center = wedges[i].center

        for other_autotext in autotexts[i + 1:]:
            other_bbox = other_autotext.get_window_extent()
            # Check for overlap based on the threshold
            if bbox.x0 < other_bbox.x1 and bbox.x1 > other_bbox.x0 and \
               bbox.y0 < other_bbox.y1 and bbox.y1 > other_bbox.y0:
                autotext.set_position((center[0] * 1.1, center[1] * 1.1))


# Define the directory containing the HTML files
html_directory = "C:\\Users\\modsf\\Desktop\\ReportesHtml"

# Initialize counters
passed_count = 0
no_run_count = 0
not_completed_count = 0
failed_count = 0

# List to store processed file names
processed_files = []

# Loop through all files in the directory
for filename in os.listdir(html_directory):
    if filename.endswith(".html"):
        file_path = os.path.join(html_directory, filename)
        processed_files.append(filename)

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
            elif status_text == "Failed": 
                failed_count += 1
            elif status_text == "No Run":
                no_run_count += 1
            elif status_text == "Not Completed":
                not_completed_count += 1

# Create a pandas DataFrame with the counts
data = {
    'Status': ['Passed', 'Failed', 'No Run', 'Not Completed'], 
    'Count': [passed_count, failed_count, no_run_count, not_completed_count]
}
df = pd.DataFrame(data)

# Calculate percentages
total_count = df['Count'].sum()
df['Percentage'] = (df['Count'] / total_count) * 100

# Create a pie chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

wedges, texts, autotexts = ax1.pie(df['Count'], labels=df['Status'], autopct='%1.1f%%', startangle=90, colors=pie_colors, explode=explode, shadow=pie_shadow, textprops=pie_textprops)
ax1.axis('equal')
ax1.set_title('Execution Status Distribution')

# Adjust pie labels to avoid overlap
adjust_pie_labels(ax1, wedges, texts, autotexts)

# Display the table
ax2.axis('off')
table_columns = ['Status', 'Count']
table = ax2.table(cellText=df[table_columns].values, rowLabels=df.index, colLabels=table_columns, cellLoc='center', rowLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(table_fontsize)

table.scale(1, 1.5) 
for row_index, color in table_cell_colors.items():
    for col_index in range(len(table_columns)): 
        table[(row_index, col_index)].set_facecolor(color) 


# Display the list of processed files
fig.suptitle(f"Processed Files: {', '.join(processed_files)}", fontsize=8, y=0.95)

plt.subplots_adjust(wspace=0.4)  
fig.suptitle('HTML Report Summary', fontsize=14, y=0.98)  

plt.show()

