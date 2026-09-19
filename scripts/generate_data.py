#!/usr/bin/env python3
"""
CLI script for generating synthetic financial transaction dataset with ground-truth AML/fraud typologies
and running the feature engineering pipeline.
"""

import sys
import os
import argparse
import pandas as pd

# Add backend and root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from app.services.synthetic_generator import SyntheticDataGenerator
from ml.features import FeatureEngineeringPipeline


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic fraud & AML transaction dataset.")
    parser.add_argument("--size", type=int, default=50000, help="Number of transactions to generate (default: 50000)")
    parser.add_argument("--customers", type=int, default=2500, help="Number of customers to generate (default: 2500)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility (default: 42)")
    parser.add_argument("--save-dir", type=str, default="data", help="Directory to save output CSVs (default: data)")

    args = parser.parse_args()

    os.makedirs(args.save_dir, exist_ok=True)

    print(f"=== [Phase 1] Synthetic Data Generation (Seed: {args.seed}, Size: {args.size}) ===")
    generator = SyntheticDataGenerator(seed=args.seed)
    df_cust, df_acc, df_tx = generator.generate_dataset(num_transactions=args.size, num_customers=args.customers)

    print(f"\n[Generated Summary]")
    print(f"Customers:    {len(df_cust):,}")
    print(f"Accounts:     {len(df_acc):,}")
    print(f"Transactions: {len(df_tx):,}")

    # Calculate and report Class Balance & Typology Breakdown
    print(f"\n=== [Typology Distribution & Class Balance] ===")
    typology_counts = df_tx["typology_label"].value_counts()
    typology_pcts = (df_tx["typology_label"].value_counts(normalize=True) * 100).round(2)

    df_metrics = pd.DataFrame({
        "Count": typology_counts,
        "Percentage (%)": typology_pcts
    })
    print(df_metrics.to_string())

    total_fraud = df_tx["is_fraud"].sum()
    fraud_pct = round(df_tx["is_fraud"].mean() * 100, 2)
    print(f"\nTotal Fraud Transactions: {total_fraud:,} ({fraud_pct}%)")

    # Run Feature Engineering Pipeline
    print(f"\n=== [Executing Feature Engineering Pipeline] ===")
    pipeline = FeatureEngineeringPipeline()
    df_features = pipeline.transform(df_tx, df_cust, df_acc)

    print(f"Feature Matrix Shape: {df_features.shape[0]:,} rows x {df_features.shape[1]} columns")
    null_count = df_features.isnull().sum().sum()
    print(f"Total Null Values in Feature Matrix: {null_count}")

    # Check for target label leakage in features
    feature_names = list(df_features.columns)
    print(f"Extracted Features ({len(feature_names)}):")
    print(", ".join(feature_names))

    # Save outputs to data directory
    cust_file = os.path.join(args.save_dir, "customers.csv")
    acc_file = os.path.join(args.save_dir, "accounts.csv")
    tx_file = os.path.join(args.save_dir, "transactions.csv")
    feat_file = os.path.join(args.save_dir, "features.csv")

    df_cust.to_csv(cust_file, index=False)
    df_acc.to_csv(acc_file, index=False)
    df_tx.to_csv(tx_file, index=False)
    df_features.to_csv(feat_file, index=False)

    print(f"\n=== [Saved Datasets to '{args.save_dir}/'] ===")
    print(f"- {cust_file}")
    print(f"- {acc_file}")
    print(f"- {tx_file}")
    print(f"- {feat_file}")


if __name__ == "__main__":
    main()
