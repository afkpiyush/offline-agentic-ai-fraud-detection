from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
import io
import datetime
from app.db.session import get_db
from app.db.models import Transaction
from app.logger import logger

router = APIRouter()


@router.post("/ingest/csv")
async def ingest_csv_transactions(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Ingests a CSV file containing batch financial transactions into PostgreSQL database.
    Validates required columns and formatting.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        required_cols = {"sender_account_id", "receiver_account_id", "amount", "timestamp"}
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            raise HTTPException(
                status_code=422,
                detail=f"CSV missing required columns: {list(missing_cols)}"
            )

        inserted_count = 0
        tx_objects = []

        for idx, row in df.iterrows():
            tx_id = str(row.get("transaction_id", f"CSV_TX_{idx+1:08d}"))
            sender = str(row["sender_account_id"])
            receiver = str(row["receiver_account_id"])
            amount = float(row["amount"])
            
            ts_val = row["timestamp"]
            if isinstance(ts_val, str):
                ts = pd.to_datetime(ts_val).to_pydatetime()
            else:
                ts = datetime.datetime.utcnow()

            location = str(row.get("location", "UNKNOWN"))
            device_id = str(row.get("device_id", "UNKNOWN"))
            channel = str(row.get("channel", "ONLINE"))
            is_fraud = bool(row.get("is_fraud", False))
            typology = str(row.get("typology_label", "legitimate"))

            tx_obj = Transaction(
                transaction_id=tx_id,
                sender_account_id=sender,
                receiver_account_id=receiver,
                amount=amount,
                currency="USD",
                timestamp=ts,
                location=location,
                device_id=device_id,
                channel=channel,
                is_fraud=is_fraud,
                typology_label=typology,
            )
            tx_objects.append(tx_obj)

        db.add_all(tx_objects)
        await db.commit()

        logger.info("Batch CSV Ingestion Successful", record_count=len(tx_objects))

        return {
            "status": "success",
            "imported_records": len(tx_objects),
            "filename": file.filename,
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Failed CSV Ingestion", error=str(e))
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
