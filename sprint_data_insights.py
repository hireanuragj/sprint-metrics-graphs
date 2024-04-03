import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

def read_data(file_path):
    try:
        df = pd.read_csv(file_path, index_col=0)
        return df
    except FileNotFoundError:
        print(f"{file_path} not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"No data in {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def calculate_metrics(df):
    trend = df.iloc[:, -1] - df.iloc[:, 0]
    std_dev = df.std(axis=1)
    return trend, std_dev

def classify_teams(trend, std_dev):
    teams = {
        'improving_teams': trend[trend > 0].index.tolist(),
        'declining_teams': trend[trend < 0].index.tolist(),
        'consistent_teams': trend[trend.abs() < 0.1].index.tolist(),
        'most_consistent_team': std_dev.idxmin(),
        'least_consistent_team': std_dev.idxmax()
    }
    return teams

def create_bar_plot(data, xlabel, ylabel, title, filename):
    plt.figure(figsize=(10,6))
    bar_plot = sns.barplot(x=data.index, y=data.values, color="b")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    for p in bar_plot.patches:
        bar_plot.annotate(format(p.get_height(), '.2f'), 
                          (p.get_x() + p.get_width() / 2., p.get_height()), 
                          ha = 'center', va = 'center', 
                          xytext = (0, 10), 
                          textcoords = 'offset points')
    plt.savefig(filename)
    plt.close()

def visualize_data(df, std_dev):
    create_bar_plot(std_dev, 'Team', 'Standard Deviation of Completion Rate', 'Standard Deviation of Task Completion Rates', 'Std_Dev_Completion_Rates.jpg')
    palette = sns.color_palette("hls", len(df.index))
    color_dict = dict(zip(df.index, palette))
    color_dict['Overall'] = 'black'
    plt.figure(figsize=(10,6))
    box_plot = sns.boxplot(data=df.T, orient='h', palette=color_dict, width=0.1)
    for i in range(len(df.index)):
        min_val = df.iloc[i].min()
        max_val = df.iloc[i].max()
        avg_val = df.iloc[i].mean()
        box_plot.text(min_val, i+0.2, f'Min: {min_val:.2f}', verticalalignment='center', color='black', weight='semibold')
        box_plot.text(max_val, i+0.2, f'Max: {max_val:.2f}', verticalalignment='center', color='black', weight='semibold')
        box_plot.text(avg_val, i+0.2, f'Avg: {avg_val:.2f}', verticalalignment='center', color='red', weight='semibold')
    plt.xlabel('Completion Rate')
    plt.title('Distribution of Task Completion Rates for Each Team')
    plt.savefig('Task_Completion_Rates_Distribution.jpg')
    plt.close()
    success_rate = (df >= 0.7).mean(axis=1) * 100
    plt.figure(figsize=(10,6))
    success_rate_plot = sns.barplot(x=success_rate.index, y=success_rate.values, color="b")
    plt.xlabel('Team')
    plt.ylabel('Sprint Goal Success Rate (%)')
    plt.title('Sprint Goal Success Rate for Each Team')
    for p in success_rate_plot.patches:
        success_rate_plot.annotate(format(p.get_height(), '.2f'), 
                                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                                   ha = 'center', va = 'center', 
                                   xytext = (0, 10), 
                                   textcoords = 'offset points')
    plt.savefig('Sprint_Goal_Success_Rate.jpg')
    plt.close()

def calculate_velocity(df):
    velocity = df.mean(axis=1)
    create_bar_plot(velocity, 'Team', 'Velocity (average completion rate)', 'Velocity for Each Team', 'Velocity.jpg')
    return velocity

def main():
    df = read_data('sprint_data.csv')
    if df is not None:
        trend, std_dev = calculate_metrics(df)
        teams = classify_teams(trend, std_dev)
        visualize_data(df, std_dev)
        velocity = calculate_velocity(df)

if __name__ == "__main__":
    main()
