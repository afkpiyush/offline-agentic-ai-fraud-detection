import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    JSON,
    Index,
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(64), unique=True, index=True, nullable=False)
    name = Column(String(128), nullable=False)
    kyc_status = Column(String(32), default="VERIFIED")
    risk_level = Column(String(32), default="LOW")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    accounts = relationship("Account", back_populates="customer")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String(64), unique=True, index=True, nullable=False)
    customer_id = Column(String(64), ForeignKey("customers.customer_id"), nullable=False)
    account_type = Column(String(32), default="SAVINGS")
    balance = Column(Float, default=0.0)
    status = Column(String(32), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    customer = relationship("Customer", back_populates="accounts")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(64), unique=True, index=True, nullable=False)
    sender_account_id = Column(String(64), index=True, nullable=False)
    receiver_account_id = Column(String(64), index=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(8), default="USD")
    timestamp = Column(DateTime, nullable=False, index=True)
    location = Column(String(128), nullable=True)
    device_id = Column(String(128), nullable=True)
    channel = Column(String(32), default="ONLINE")
    is_fraud = Column(Boolean, default=False, index=True)
    typology_label = Column(String(64), default="legitimate", index=True)

    alerts = relationship("Alert", back_populates="transaction")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(64), unique=True, index=True, nullable=False)
    transaction_id = Column(String(64), ForeignKey("transactions.transaction_id"), nullable=False)
    risk_score = Column(Float, nullable=False)
    status = Column(String(32), default="PENDING")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    transaction = relationship("Transaction", back_populates="alerts")
    cases = relationship("Case", back_populates="alert")


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String(64), unique=True, index=True, nullable=False)
    alert_id = Column(String(64), ForeignKey("alerts.alert_id"), nullable=False)
    status = Column(String(32), default="OPEN")  # OPEN, INVESTIGATING, ESCALATED, CLOSED
    assigned_to = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    alert = relationship("Alert", back_populates="cases")
    events = relationship("CaseEvent", back_populates="case")


class CaseEvent(Base):
    __tablename__ = "case_events"

    id = Integer
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String(64), ForeignKey("cases.case_id"), nullable=False)
    event_type = Column(String(64), nullable=False)  # ACTION, COMMENT, DISPOSITION, SAR_GENERATED
    actor = Column(String(128), nullable=False)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    case = relationship("Case", back_populates="events")


class ModelRun(Base):
    __tablename__ = "model_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String(64), unique=True, index=True, nullable=False)
    model_name = Column(String(128), nullable=False)
    model_version = Column(String(32), nullable=False)
    metrics = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# Additional Indexes for fast queries
Index("idx_tx_sender_time", Transaction.sender_account_id, Transaction.timestamp)
Index("idx_tx_receiver_time", Transaction.receiver_account_id, Transaction.timestamp)
