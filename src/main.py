import pandas as pd
import matplotlib.pyplot as plt
import os

# Create output folder
os.makedirs("output", exist_ok=True)

# ---------------------------
# FLOOD RISK ANALYSIS
# ---------------------------

flood_data = pd.read_csv("data/flood_data.csv")

def flood_risk(row):
    if row["Rainfall_mm"] > 120 or row["River_Level_m"] > 5:
        return "High Risk"
    elif row["Rainfall_mm"] > 70:
        return "Moderate Risk"
    else:
        return "Low Risk"

flood_data["Flood_Risk"] = flood_data.apply(flood_risk, axis=1)

print("\nFlood Risk Analysis\n")
print(flood_data)

# Rainfall graph
plt.figure()

rainfall_by_district = flood_data.groupby("District")["Rainfall_mm"].mean()
rainfall_by_district.plot(kind="bar")

plt.title("Average Rainfall by District")
plt.xlabel("District")
plt.ylabel("Rainfall (mm)")

plt.savefig("output/rainfall_analysis.png")
plt.show()

# ---------------------------
# DISASTER TWEET ANALYSIS
# ---------------------------

tweets = pd.read_csv("data/tweets.csv")

keywords = ["flood", "earthquake", "cyclone", "storm", "rescue"]

def detect_disaster(tweet):
    tweet = tweet.lower()
    for word in keywords:
        if word in tweet:
            return "Disaster Alert"
    return "Normal"

tweets["Alert"] = tweets["Tweet"].apply(detect_disaster)

print("\nTweet Analysis\n")
print(tweets)

# Graph for tweets
plt.figure()

tweet_counts = tweets["Alert"].value_counts()
tweet_counts.plot(kind="bar")

plt.title("Disaster Tweet Detection")
plt.xlabel("Tweet Category")
plt.ylabel("Count")

plt.savefig("output/tweet_detection.png")
plt.show()

print("\nGraphs saved in output folder.")

# ---------------------------
# DISASTER REPORT GENERATION
# ---------------------------

high_risk = flood_data[flood_data["Flood_Risk"] == "High Risk"]["District"].unique()
moderate_risk = flood_data[flood_data["Flood_Risk"] == "Moderate Risk"]["District"].unique()

total_tweets = len(tweets)
disaster_alerts = len(tweets[tweets["Alert"] == "Disaster Alert"])
normal_tweets = len(tweets[tweets["Alert"] == "Normal"])

report = f"""
DISASTER MONITORING REPORT
--------------------------

Flood Risk Summary
High Risk Districts: {', '.join(high_risk)}
Moderate Risk Districts: {', '.join(moderate_risk)}

Tweet Alert Summary
Total Tweets Analyzed: {total_tweets}
Disaster Alerts Detected: {disaster_alerts}
Normal Tweets: {normal_tweets}

Conclusion
Flood risk detected in some districts. Continuous monitoring recommended.
"""

with open("output/disaster_report.txt", "w") as file:
    file.write(report)

print("\nDisaster report generated in output folder.")