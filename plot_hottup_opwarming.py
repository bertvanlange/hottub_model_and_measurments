import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_single_probe(df, probe = 1):
    # Plot 'Sensor 1' against 'Timestamp'
    plt.figure(figsize=(10, 6))
    plt.plot(df['Timestamp'], df[f'Sensor {probe}'], marker='o', linestyle='-', color='b')

    # Add labels and title
    plt.xlabel('Timestamp')
    plt.ylabel(f'Sensor {probe} Reading')
    plt.title(f'Sensor {probe} Readings Over Time')

    # Show the plot
    plt.xticks(rotation=45)
    plt.tight_layout()


def plot_for_heating(df, volumme = 2):
    # sensor 1 : buiten             blouw
    # sensor 2 : koud_water         licth blouw
    # sensor 3 : heet_water         rood
    # Sensor 4 : bad_temperatuur    groen

    # temp_verschil_kachel          magenta
    # geschatte_vermogen            geel
    df['dt'] = df['Sensor 3'] - df['Sensor 2']
    df["P_kachel"] = df["dt"]*4.2*volumme
    # Plot 'Sensor 1' against 'Timestamp'
    plt.figure(figsize=(15, 8))
    plt.plot(df['Timestamp'], df['Sensor 1'], linestyle='-', color='b')
    plt.plot(df['Timestamp'], df['Sensor 2'], linestyle='-', color='c')
    plt.plot(df['Timestamp'], df['Sensor 3'], linestyle='-', color='r')
    plt.plot(df['Timestamp'], df['Sensor 4'], linestyle='-', color='g')

    plt.plot(df['Timestamp'], df['dt'], linestyle='-', color='m')
    plt.plot(df['Timestamp'], df['P_kachel'], linestyle='-', color='y')
    
    plt.legend(["T_buiten","T_water_in","T_water_uit","T_hottub","dT_kachel","Power"])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Time only
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=30))  # Interval of 30 minutes

    
    plt.ylim(0, 55)
    plt.grid(color='k', linestyle='-', linewidth=.5)

    # Add labels and title
    plt.xlabel('Timestamp')
    # plt.ylabel(f'Sensor {probe} Reading')
    # plt.title(f'Sensor {probe} Readings Over Time')

    # Show the plot
    plt.xticks(rotation=45)
    plt.tight_layout()

# i want to display the time and not the date in the plot, with a higher interval, so every half hour or so

df = pd.read_csv('temp_logger\\logs\\temperature_log.csv')

# print(df)

df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# dataframe looks like: Timestamp, sensor 1 ,sensor 2 ,sensor 3 ,sensor 4
# now i want to split the dataframe in parts, and split them when te time between the timestamps is greater than 30 minits

# Calculate the time difference between consecutive rows
df["TimeDiff"] = df["Timestamp"].diff()

# Create a group ID based on whether the time difference is greater than 30 minutes
threshold = pd.Timedelta(minutes=30)
df["Group"] = (df["TimeDiff"] > threshold).cumsum()

# Split the DataFrame into separate parts based on the group
groups = [group for _, group in df.groupby("Group")]

# Display results
# for i, group in enumerate(groups):
#     # Get the first timestamp in the group
#     first_timestamp = group["Timestamp"].iloc[0].strftime("%Y-%m-%d_%H-%M-%S")
    
#     # Drop unnecessary columns before saving
#     group_to_save = group.drop(columns=["TimeDiff", "Group"])
#     plot_for_heating(group)
#     # Save to CSV file
#     filename = f"{first_timestamp}.csv"
#     group_to_save.to_csv(filename, index=False)
#     print(f"Saved group {i + 1} to {filename}")


# Access the last group in the list
last_group = groups[-1]

# Display the last group's content
print("Last Group:")
print(last_group)
plot_for_heating(last_group)


plt.show()

