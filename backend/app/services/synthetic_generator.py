import random
import datetime
import uuid
import pandas as pd
import numpy as np


class SyntheticDataGenerator:
    """
    Seeded, reproducible synthetic financial transaction generator with injected fraud & AML typologies.
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.rng = random.Random(seed)
        self.np_rng = np.random.default_rng(seed)

        self.cities = [
            "New York", "London", "Tokyo", "Mumbai", "Singapore",
            "Frankfurt", "Hong Kong", "Sydney", "Dubai", "Toronto"
        ]
        self.channels = ["ONLINE", "MOBILE", "ATM", "POS", "WIRE"]

    def generate_dataset(self, num_transactions: int = 50000, num_customers: int = 2500):
        """Generates customers, accounts, and transactions with injected ground truth typologies."""
        self.rng.seed(self.seed)
        self.np_rng = np.random.default_rng(self.seed)

        # 1. Generate Customers
        customers = []
        for i in range(num_customers):
            c_id = f"CUST_{i+1:06d}"
            customers.append({
                "customer_id": c_id,
                "name": f"Customer_{i+1}",
                "kyc_status": "VERIFIED" if self.rng.random() > 0.05 else "PENDING",
                "risk_level": self.rng.choice(["LOW", "LOW", "LOW", "MEDIUM", "HIGH"]),
                "home_city": self.rng.choice(self.cities),
                "created_at": datetime.datetime(2025, 1, 1) + datetime.timedelta(days=self.rng.randint(0, 300)),
            })
        df_customers = pd.DataFrame(customers)

        # 2. Generate Accounts
        accounts = []
        for c in customers:
            acc_count = 1 if self.rng.random() > 0.2 else 2
            for a_idx in range(acc_count):
                acc_id = f"ACC_{c['customer_id']}_{a_idx+1}"
                accounts.append({
                    "account_id": acc_id,
                    "customer_id": c["customer_id"],
                    "account_type": "SAVINGS" if a_idx == 0 else "CHECKING",
                    "balance": round(self.rng.uniform(1000.0, 50000.0), 2),
                    "home_city": c["home_city"],
                })
        df_accounts = pd.DataFrame(accounts)
        all_account_ids = df_accounts["account_id"].tolist()

        # 3. Base Legitimate Transactions
        transactions = []
        base_time = datetime.datetime(2026, 1, 1, 8, 0, 0)
        
        # Determine number of normal vs pattern transactions
        num_normal = int(num_transactions * 0.93)
        num_fraud_budget = num_transactions - num_normal

        for i in range(num_normal):
            tx_id = f"TX_{i+1:08d}"
            sender = self.rng.choice(all_account_ids)
            receiver = self.rng.choice(all_account_ids)
            while receiver == sender:
                receiver = self.rng.choice(all_account_ids)

            # Random timestamp over 90 days
            delta_seconds = self.rng.randint(0, 90 * 86400)
            tx_time = base_time + datetime.timedelta(seconds=delta_seconds)

            sender_acc = df_accounts[df_accounts["account_id"] == sender].iloc[0]

            amount = round(float(self.np_rng.exponential(scale=150.0) + 10.0), 2)
            location = sender_acc["home_city"] if self.rng.random() > 0.1 else self.rng.choice(self.cities)
            device = f"DEV_{sender_acc['customer_id']}_1"

            transactions.append({
                "transaction_id": tx_id,
                "sender_account_id": sender,
                "receiver_account_id": receiver,
                "amount": amount,
                "currency": "USD",
                "timestamp": tx_time,
                "location": location,
                "device_id": device,
                "channel": self.rng.choice(self.channels),
                "is_fraud": False,
                "typology_label": "legitimate",
            })

        # 4. Inject Fraud & AML Typologies
        tx_counter = num_normal + 1
        
        # Typology 1: Card Fraud Burst (5% of fraud budget)
        card_burst_count = max(10, int(num_fraud_budget * 0.20))
        for _ in range(card_burst_count // 5):
            victim_acc = self.rng.choice(all_account_ids)
            stolen_device = f"DEV_UNKNOWN_{uuid.uuid4().hex[:6]}"
            anomalous_city = self.rng.choice([c for c in self.cities if c != "New York"])
            burst_start = base_time + datetime.timedelta(days=self.rng.randint(1, 80), hours=self.rng.randint(1, 5))

            for b in range(5):
                tx_id = f"TX_{tx_counter:08d}"
                tx_counter += 1
                transactions.append({
                    "transaction_id": tx_id,
                    "sender_account_id": victim_acc,
                    "receiver_account_id": self.rng.choice(all_account_ids),
                    "amount": round(self.rng.uniform(1500.0, 4900.0), 2),
                    "currency": "USD",
                    "timestamp": burst_start + datetime.timedelta(minutes=b * 2),
                    "location": anomalous_city,
                    "device_id": stolen_device,
                    "channel": "POS",
                    "is_fraud": True,
                    "typology_label": "card_fraud_burst",
                })

        # Typology 2: Structuring / Smurfing (20% of fraud budget)
        structuring_count = max(10, int(num_fraud_budget * 0.20))
        for _ in range(structuring_count // 4):
            smurf_acc = self.rng.choice(all_account_ids)
            target_acc = self.rng.choice(all_account_ids)
            struct_start = base_time + datetime.timedelta(days=self.rng.randint(1, 80))

            for s in range(4):
                tx_id = f"TX_{tx_counter:08d}"
                tx_counter += 1
                # Amount strictly under $10,000 reporting threshold ($9,200 - $9,950)
                amount = round(self.rng.uniform(9200.0, 9950.0), 2)
                transactions.append({
                    "transaction_id": tx_id,
                    "sender_account_id": smurf_acc,
                    "receiver_account_id": target_acc,
                    "amount": amount,
                    "currency": "USD",
                    "timestamp": struct_start + datetime.timedelta(hours=s * 3),
                    "location": "New York",
                    "device_id": f"DEV_{smurf_acc}",
                    "channel": "WIRE",
                    "is_fraud": True,
                    "typology_label": "structuring_smurfing",
                })

        # Typology 3: Multi-hop Layering Chains (25% of fraud budget)
        layering_count = max(15, int(num_fraud_budget * 0.25))
        for _ in range(layering_count // 4):
            chain_accs = self.rng.sample(all_account_ids, 5) # A -> B -> C -> D -> E
            layer_start = base_time + datetime.timedelta(days=self.rng.randint(1, 80))
            initial_amount = round(self.rng.uniform(50000.0, 150000.0), 2)

            curr_amount = initial_amount
            for hop in range(4):
                tx_id = f"TX_{tx_counter:08d}"
                tx_counter += 1
                transactions.append({
                    "transaction_id": tx_id,
                    "sender_account_id": chain_accs[hop],
                    "receiver_account_id": chain_accs[hop + 1],
                    "amount": round(curr_amount, 2),
                    "currency": "USD",
                    "timestamp": layer_start + datetime.timedelta(minutes=(hop + 1) * 15),
                    "location": "London",
                    "device_id": f"DEV_CHAIN_{hop}",
                    "channel": "WIRE",
                    "is_fraud": True,
                    "typology_label": "layering_chain",
                })
                curr_amount *= 0.97 # 3% fee deduction per hop

        # Typology 4: Mule Fan-In / Fan-Out Networks (25% of fraud budget)
        mule_count = max(20, int(num_fraud_budget * 0.25))
        mule_hub = self.rng.choice(all_account_ids)
        feeder_accs = self.rng.sample(all_account_ids, min(15, len(all_account_ids)))
        mule_start = base_time + datetime.timedelta(days=self.rng.randint(1, 80))

        # Fan-In to mule hub
        for feeder in feeder_accs:
            tx_id = f"TX_{tx_counter:08d}"
            tx_counter += 1
            transactions.append({
                "transaction_id": tx_id,
                "sender_account_id": feeder,
                "receiver_account_id": mule_hub,
                "amount": round(self.rng.uniform(2000.0, 8000.0), 2),
                "currency": "USD",
                "timestamp": mule_start + datetime.timedelta(minutes=self.rng.randint(5, 60)),
                "location": "Dubai",
                "device_id": f"DEV_FEEDER",
                "channel": "ONLINE",
                "is_fraud": True,
                "typology_label": "mule_fan_in",
            })

        # Typology 5: Synthetic Identity Fraud (10% of fraud budget)
        synth_count = max(10, int(num_fraud_budget * 0.10))
        for _ in range(synth_count):
            synth_acc = f"ACC_SYNTH_{self.rng.randint(1000, 9999)}"
            tx_id = f"TX_{tx_counter:08d}"
            tx_counter += 1
            transactions.append({
                "transaction_id": tx_id,
                "sender_account_id": synth_acc,
                "receiver_account_id": self.rng.choice(all_account_ids),
                "amount": round(self.rng.uniform(12000.0, 45000.0), 2),
                "currency": "USD",
                "timestamp": base_time + datetime.timedelta(days=self.rng.randint(1, 80)),
                "location": "Hong Kong",
                "device_id": f"DEV_SYNTH_{uuid.uuid4().hex[:6]}",
                "channel": "WIRE",
                "is_fraud": True,
                "typology_label": "synthetic_identity",
            })

        df_transactions = pd.DataFrame(transactions)
        df_transactions = df_transactions.sort_values(by="timestamp").reset_index(drop=True)

        return df_customers, df_accounts, df_transactions
