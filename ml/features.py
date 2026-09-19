import pandas as pd
import numpy as np


class FeatureEngineeringPipeline:
    """
    Computes temporal, velocity, amount deviation, geo/device mismatch,
    and counterparty novelty features without target label leakage.
    """

    def transform(self, df_transactions: pd.DataFrame, df_customers: pd.DataFrame = None, df_accounts: pd.DataFrame = None) -> pd.DataFrame:
        """Takes raw transaction DataFrame and extracts engineered ML features."""
        df = df_transactions.copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values(by="timestamp").reset_index(drop=True)

        # 1. Temporal & Time-of-Day Features
        df["hour"] = df["timestamp"].dt.hour
        df["day_of_week"] = df["timestamp"].dt.dayofweek
        df["is_night_time"] = ((df["hour"] >= 0) & (df["hour"] <= 5)).astype(int)

        # 2. Velocity Features (Rolling Window 1h, 24h, 7d per sender_account_id)
        # Using vectorized pandas rolling operations
        df = df.set_index("timestamp")

        # 1h window
        sender_grp = df.groupby("sender_account_id")
        df["velocity_count_1h"] = sender_grp["amount"].rolling("1h").count().values
        df["velocity_sum_1h"] = sender_grp["amount"].rolling("1h").sum().values

        # 24h window
        df["velocity_count_24h"] = sender_grp["amount"].rolling("24h").count().values
        df["velocity_sum_24h"] = sender_grp["amount"].rolling("24h").sum().values

        # 7d window
        df["velocity_count_7d"] = sender_grp["amount"].rolling("7d").count().values
        df["velocity_sum_7d"] = sender_grp["amount"].rolling("7d").sum().values

        df = df.reset_index()

        # 3. Amount Z-Score & Deviation Features
        cust_stats = df.groupby("sender_account_id")["amount"].agg(["mean", "std"]).reset_index()
        cust_stats.rename(columns={"mean": "amount_mean", "std": "amount_std"}, inplace=True)
        cust_stats["amount_std"] = cust_stats["amount_std"].fillna(1.0).replace(0.0, 1.0)

        df = df.merge(cust_stats, on="sender_account_id", how="left")
        df["amount_zscore"] = (df["amount"] - df["amount_mean"]) / df["amount_std"]
        df["amount_ratio_to_mean"] = df["amount"] / (df["amount_mean"] + 1e-5)

        # 4. Structuring Threshold Distance Feature ($10,000 reporting threshold)
        df["dist_to_10k_threshold"] = np.abs(10000.0 - df["amount"])
        df["is_near_10k_threshold"] = ((df["amount"] >= 9000.0) & (df["amount"] < 10000.0)).astype(int)

        # 5. Counterparty Novelty (Is this receiver new for the sender?)
        df["pair"] = df["sender_account_id"] + "->" + df["receiver_account_id"]
        df["is_first_time_counterparty"] = (~df.duplicated(subset=["pair"], keep="first")).astype(int)

        # 6. Device & Location Novelty Indicator
        df["sender_device_pair"] = df["sender_account_id"] + "->" + df["device_id"].fillna("UNKNOWN")
        df["is_novel_device"] = (~df.duplicated(subset=["sender_device_pair"], keep="first")).astype(int)

        df["sender_loc_pair"] = df["sender_account_id"] + "->" + df["location"].fillna("UNKNOWN")
        df["is_novel_location"] = (~df.duplicated(subset=["sender_loc_pair"], keep="first")).astype(int)

        # Drop intermediate pair columns
        df.drop(columns=["pair", "sender_device_pair", "sender_loc_pair"], inplace=True, errors="ignore")

        # Select final clean feature columns
        feature_cols = [
            "transaction_id", "sender_account_id", "receiver_account_id", "amount", "timestamp",
            "hour", "day_of_week", "is_night_time",
            "velocity_count_1h", "velocity_sum_1h",
            "velocity_count_24h", "velocity_sum_24h",
            "velocity_count_7d", "velocity_sum_7d",
            "amount_zscore", "amount_ratio_to_mean",
            "dist_to_10k_threshold", "is_near_10k_threshold",
            "is_first_time_counterparty", "is_novel_device", "is_novel_location",
            "is_fraud", "typology_label"
        ]

        return df[feature_cols]
