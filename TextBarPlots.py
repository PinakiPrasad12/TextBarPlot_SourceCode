import pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib import colors

# Load the datasets
eo_1 = pd.read_csv('eo_1.csv')
eo_2 = pd.read_csv('eo_2.csv')
eo_3 = pd.read_csv('eo_3.csv')
eo_4 = pd.read_csv('eo_4.csv')
#eo_pr = pd.read_csv('eo_pr.csv')
#eo_xx = pd.read_csv('eo_xx.csv')

# Combine the datasets, considering only the specified columns
datasets = [eo_1, eo_2, eo_3, eo_4]
data_combined = pd.concat([df[['STATE', 'ORGANIZATION', 'REVENUE_AMT', 'ASSET_AMT']] for df in datasets])

# Mapping for state abbreviations to full names in capital letters
state_abbreviations = {
    "AL": "ALABAMA", "AK": "ALASKA", "AZ": "ARIZONA", "AR": "ARKANSAS", "CA": "CALIFORNIA", 
    "CO": "COLORADO", "CT": "CONNECTICUT", "DE": "DELAWARE", "FL": "FLORIDA", "GA": "GEORGIA", 
    "HI": "HAWAII", "ID": "IDAHO", "IL": "ILLINOIS", "IN": "INDIANA", "IA": "IOWA", "KS": "KANSAS", 
    "KY": "KENTUCKY", "LA": "LOUISIANA", "ME": "MAINE", "MD": "MARYLAND", "MA": "MASSACHUSETTS", 
    "MI": "MICHIGAN", "MN": "MINNESOTA", "MS": "MISSISSIPPI", "MO": "MISSOURI", "MT": "MONTANA", 
    "NE": "NEBRASKA", "NV": "NEVADA", "NH": "NEW HAMPSHIRE", "NJ": "NW JRSY", "NM": "NEW MEXICO", 
    "NY": "NEW YORK", "NC": "N CRLNA", "ND": "NORTH DAKOTA", "OH": "OHIO", "OK": "OKLAHOMA", 
    "OR": "OREGON", "PA": "PENNSYLVANIA", "RI": "RHODE ISLAND", "SC": "SOUTH CAROLINA", 
    "SD": "SOUTH DAKOTA", "TN": "TENNESSEE", "TX": "TEXAS", "UT": "UTAH", "VT": "VERMONT", 
    "VA": "VIRGINIA", "WA": "WASHINGTON", "WV": "WEST VIRGINIA", "WI": "WISCNSN", "WY": "WYOMING"
}
# Replace state abbreviations with full names in the combined dataset
data_combined['STATE'] = data_combined['STATE'].map(state_abbreviations)

# Aggregate the data to calculate the sum of 'ORGANIZATION', 'REVENUE_AMT', and 'ASSET_AMT' for each state
aggregated_data = data_combined.groupby('STATE').agg({
    'ORGANIZATION': 'sum',
    'REVENUE_AMT': 'sum',
    'ASSET_AMT': 'sum'
}).reset_index()

# Create the lists
states = aggregated_data['STATE'].tolist()
non_profit_counts = aggregated_data['ORGANIZATION'].tolist()
total_revenue = aggregated_data['REVENUE_AMT'].tolist()
total_asset = aggregated_data['ASSET_AMT'].tolist()

# Convert 'REVENUE_AMT' and 'ASSET_AMT' from dollars to billions and integer representation
total_revenue = [int(revenue // 1e9) for revenue in total_revenue]
total_asset = [int(asset // 1e9) for asset in total_asset]

###############################################################################


# Create empty lists for the subsets
subset_1_states = []
subset_1_non_profit_counts = []
subset_1_total_revenue = []
subset_1_total_asset = []

subset_2_states = []
subset_2_non_profit_counts = []
subset_2_total_revenue = []
subset_2_total_asset = []

subset_3_states = []
subset_3_non_profit_counts = []
subset_3_total_revenue = []
subset_3_total_asset = []

# Iterate through the non_profit_counts and divide the data into subsets
for i, count in enumerate(non_profit_counts):
    if 0 <= count <= 30000:
        subset_1_states.append(states[i])
        subset_1_non_profit_counts.append(count)
        subset_1_total_revenue.append(total_revenue[i])
        subset_1_total_asset.append(total_asset[i])
    elif 30001 <= count <= 80000:
        subset_2_states.append(states[i])
        subset_2_non_profit_counts.append(count)
        subset_2_total_revenue.append(total_revenue[i])
        subset_2_total_asset.append(total_asset[i])
    elif count > 80000:
        subset_3_states.append(states[i])
        subset_3_non_profit_counts.append(count)
        subset_3_total_revenue.append(total_revenue[i])
        subset_3_total_asset.append(total_asset[i])


###############################################################################
def plotBars(states, non_profit_counts, total_revenue, k):  
    # Combine the lists into a list of tuples and sort by total revenue
    combined_list = sorted(zip(states, non_profit_counts, total_revenue), key=lambda x: x[2])

    # Unpack the sorted tuples back into individual lists
    states, non_profit_counts, total_revenue = zip(*combined_list)

    # Normalize total revenue for color mapping
    norm = colors.Normalize(vmin=min(total_revenue), vmax=max(total_revenue))
    color_map = plt.cm.get_cmap('Reds')
    
    # Create figure and axis with adjusted size for clarity
    fig, ax = plt.subplots(figsize=(16, 9)) 

    # Define fixed y positions based on k
    fixed_y_pos = {1: 1000, 2: 2500, 3: 8000}
    
    # Plot each state's name as a bar with evenly spaced letters
    for i, (state, count, revenue) in enumerate(zip(states, non_profit_counts, total_revenue)):
        total_height = count
        space_per_char = total_height / len(state)
        y_pos = fixed_y_pos.get(k, 1000)

        for char in state:
            ax.text(i, y_pos, char, fontsize=20, verticalalignment='bottom', 
                    horizontalalignment='center', rotation='vertical', 
                    weight='bold', color=color_map(norm(revenue)+0.15))
            y_pos += space_per_char

    # Remove the solid line at y = 0
    ax.axhline(y=0, color='black', linewidth=0)
    
    # Set x and y limits to add some space at the bottom and top
    ax.set_xlim(-0.5, len(states) - 0.5)
    ax.set_ylim(0, max(non_profit_counts) * 1.1)
    
    # Hide x and y axis ticks labels, leave only the tick marks
    ax.set_xticks(range(len(states)))
    ax.set_yticks(range(0, max(non_profit_counts) + 1, max(non_profit_counts) // 10))
    ax.tick_params(axis='x', length=5, which='major', labelsize=12)
    ax.tick_params(axis='y', which='major', labelsize=12)
    
    # Adding axis labels with larger font size
    plt.xlabel('States in US', fontsize=16) 
    plt.ylabel('Number of non-profits', fontsize=16)  
    
    # Remove all spines except the left and bottom ones
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Create a horizontal colorbar at the bottom of the plot with reduced height
    scalar_map = cm.ScalarMappable(norm=norm, cmap=color_map)
    scalar_map.set_array([])
    cbar = fig.colorbar(scalar_map, ax=ax, orientation='horizontal', pad=0.1, aspect=40)  # Increased aspect ratio
    cbar.set_label('Total Revenue (in billions)', fontsize=16)
    cbar.ax.tick_params(labelsize=14)  # Adjust tick label size
    
    # Show plot
    plt.tight_layout()  
    plt.title ("Text-Bar Plots Showing the No. of Non-Profits in each State across the US (List "+str(k)+")", fontsize=20)
    plt.savefig('PlotList_'+str(k)+'.png')
    plt.show()
    
plotBars(subset_1_states, subset_1_non_profit_counts, subset_1_total_revenue, 1)
plotBars(subset_2_states, subset_2_non_profit_counts, subset_2_total_revenue, 2)
plotBars(subset_3_states, subset_3_non_profit_counts, subset_3_total_revenue, 3)
