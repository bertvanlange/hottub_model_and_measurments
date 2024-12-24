import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('temp_logger\\logs\\temperature_log.csv')

print(df)

df['Timestamp'] = pd.to_datetime(df['Timestamp'])

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

def plot_rate_temp_change(df,probe = 1):
    # Convert the 'Timestamp' column to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Calculate the time difference between consecutive rows
    df['TimeDiff'] = df['Timestamp'].diff().dt.total_seconds()

    # Calculate the temperature difference between consecutive rows (Sensor 1)
    df['TempDiff'] = df[f'Sensor {probe}'].diff()

    # Calculate the rate of change of temperature (in degrees per second)
    df['RateOfChange'] = df['TempDiff'] / df['TimeDiff']

    # Drop the first row, since its rate of change will be NaN
    df = df.dropna(subset=['RateOfChange'])

    # Plot the rate of temperature change over time
    plt.figure(figsize=(10, 6))
    plt.plot(df['Timestamp'], df['RateOfChange'], marker='o', linestyle='-', color='b')

    # Add titles and labels
    plt.title('Rate of Temperature Change Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature Change Rate (°C/s)')
    plt.xticks(rotation=45)

    # Show the plot
    plt.tight_layout()


plot_single_probe(df)

plot_rate_temp_change(df)

# volume = 700
# plot_power(df,volume)

plt.show()

