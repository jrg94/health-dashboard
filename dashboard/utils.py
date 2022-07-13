import pandas as pd

def load_data():
    """
    A helper function for getting the data in some decent state. 
    """
    df = pd.read_csv("https://raw.githubusercontent.com/jrg94/personal-data/main/health/weightlifting.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Volume"] = df["Weight"] * df["Total Reps"]
    df["Projected 1RM"] = df["Weight"] * (1 + (df["Reps"] / 30))
    return df
