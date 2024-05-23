import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from flask import current_app


def generate_visualization():
    db = current_app.mongo.db
    data = db.common_model.find({}, {'_id': 0, 'last_seen': 1, 'operating_system': 1, 'provider': 1})
    df = pd.DataFrame(list(data))

    df['last_seen'] = pd.to_datetime(df['last_seen'], unit='s')

    # Aggregate data by operating_system and provider
    os_counts = df['operating_system'].value_counts()
    provider_counts = df['provider'].value_counts()

    # Group by date for time series visualization
    df['date'] = df['last_seen'].dt.date
    date_counts = df.groupby('date').size()

    # Set up the visualizations
    sns.set(style='whitegrid')

    # Bar chart for providers
    plt.figure(figsize=(10, 6))
    sns.barplot(x=provider_counts.index, y=provider_counts.values, palette='viridis')
    plt.title('Distribution of Providers')
    plt.xlabel('Provider')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Line plot for last_seen over time
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=date_counts.index, y=date_counts.values)
    plt.title('Hosts Seen Over Time')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()

