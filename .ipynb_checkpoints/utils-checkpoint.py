"""
Utils to calculate customer impact (delinquency).

Author: Preston Robinette
Updated: 12.15.24

Notes:
- generate_mock_data
- eval_data
- generate_plot
- generate_pie_chart
"""
import pandas as pd
import matplotlib.pyplot as plt
import random

random.seed(12)


def generate_mock_data(num_customers: int=20) -> pd.DataFrame:
    """Generate mock data to measure customer impact.

    pivot_date: ??
    customer_id: the unique identifier of the customer
    approved_at: when the customer was approved
    days_delinquent: the number of days the customer has been delinquent
    monthly_recurr_revenue: The montly revenue fragile collects from the device.
    device_value: the value of the device on fragile's balance sheet

    Args:
        num_customers: number of customers to generate data for.

    Returns:
        data: the pd.DataFrame of generated data

    """
    #
    # DATA Generation: Generate fake data to demonstrate
    # the thermostat.
    #
    device_prices = [800, 1200, 2000, 3000]
    #
    # ??
    #
    pivot_dates = [f"2024-{random.randint(1, 12)}-{random.randint(1, 31)}" for _ in range(num_customers)]
    #
    # unique customer id
    #
    customer_ids = [i+1 for i in range(num_customers)]
    #
    # The date the customer was approved
    #
    dates = [(pivot_date.split("-")[1], pivot_date.split("-")[2]) for pivot_date in pivot_dates]
    approved_dates = [f"2024-{random.randint(int(m), 12)}-{random.randint(int(d), 31)}" for m, d in dates]
    #
    # days delinquent
    #
    probs = [1 if random.random() > 0.75 else 0 for _ in range(num_customers)]
    days_delinquent = [random.randint(0, 65) for _ in range(num_customers)]
    days_delinquent = [p*dd for p, dd in zip(probs, days_delinquent)]
    #
    # randomly select device values and 
    # monthly recurring revenue (mrr)
    #
    device_values = [random.choice(device_prices) for _ in range(num_customers)]
    monthly_recurr_revenue = [round(d_value/12, 2) for d_value in device_values]
    #
    # create a pandas dataframe from the generated data
    #
    data = {
        "pivot_date": pivot_dates,
        "customer_id": customer_ids,
        "approved_at": approved_dates,
        "days_delinquent": days_delinquent,
        "monthly_recurr_revenue": monthly_recurr_revenue,
        "device_value": device_values,
    }
    
    return pd.DataFrame(data)


def eval_data(data: pd.DataFrame, threshold: int = 90) -> pd.DataFrame:
    """Generate a thermostat to measure delinquency.

    A customer is considered delinquent when they are not making
    timely payments. 

    Args:
        data: contains pivot_date, costumer_id, approved_at,
            days_delinquent, monthly_recurr_revenue, device_value

    Returns:
        Updated dataframe containing:
        - daily_recurrent_revenue: mrr/31
        - cost_to_fragile: daily_recurrent_revenue * days_delinquent
        - thermostat: green, yellow, red
    """
    #
    # calculate daily revenue
    #
    data['daily_recurrent_revenue'] = round(data['monthly_recurr_revenue'] / 31, 2)
    #
    # calculate cost to fragile
    #
    data['cost_to_fragile'] = data['daily_recurrent_revenue'] * data['days_delinquent']
    #
    # measure impact
    #
    def _measure_impact(cost):
        if cost == 0:
            return "green"
        elif cost <= 75:
            return "yellow"
        else:
            return "red"
            
    data['thermostat'] = data.apply(lambda row: _measure_impact(row['cost_to_fragile']), axis=1)

    return data


def generate_plot(data: pd.DataFrame) -> tuple:
    """Plot breaking down customer impact.

    Args:
        data: data containing thermostat values to plot

    Returns:
        plot of impact to Fragile.
    """
    #
    # create bar chart
    #
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(
            data['customer_id'], 
            data['cost_to_fragile'], 
            color=data['thermostat']
        )
    #
    # annotate for days
    #
    for bar, days in zip(bars, data['days_delinquent']):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            f"{days}d",
            ha='center', va='bottom', fontsize=10
        )
    #
    # xlabels
    #
    ax.set_xticks(data['customer_id'])
    ax.set_xticklabels(data['customer_id'], rotation=45, fontsize=10)
    
    
    ax.set_ylabel("Current Total Cost to Fragile ($)", fontsize=20)
    ax.set_xlabel("Customer ID", fontsize=20)
    ax.set_title("Customer Impact to Fragile", fontsize=20)
    #
    # legend labels
    #
    legend_labels = {
        "green": "No Impact",
        "yellow": "Medium Impact",
        "red": "High Impact"
    }
    handles = [
        plt.Line2D([0], [0], color=color, lw=10, label=label) 
        for color, label in legend_labels.items()
    ]
    ax.legend(handles=handles, title="Impact Levels", fontsize=12, title_fontsize=14)
    #
    # tight layout
    #
    plt.tight_layout()

    return fig, ax
    

def generate_pie_chart(data: pd.DataFrame) -> plt.Figure:
    """Pie chart for the percentage distribution of impact levels.

    Args:
        data: data containing thermostat values to plot

    Returns:
        plt.Figure: Matplotlib figure object.
    """
    #
    # group data
    #
    impact_counts = data['thermostat'].value_counts()
    #
    # define labels
    #
    labels = {
        "green": "No Impact",
        "yellow": "Medium Impact",
        "red": "High Impact"
    }
    colors = {
        "green": "green",
        "yellow": "yellow",
        "red": "red"
    }
    #
    # map labels to impact
    #
    pie_labels = [labels[key] for key in impact_counts.index]
    pie_colors = [colors[key] for key in impact_counts.index]
    #
    # generate plot
    #
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        impact_counts,
        labels=pie_labels,
        colors=pie_colors,
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 12}
    )
    #
    # set titel
    #
    ax.set_title("Impact to Fragile Business", fontsize=20)

    return fig



    