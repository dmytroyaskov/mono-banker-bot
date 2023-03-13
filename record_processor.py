import iso18245 as MCC
from datetime import datetime


def hide_sensitive(data, visible_symbols=4):
    tmp_str = str(data)
    tmp_str = '*' * (len(tmp_str) - visible_symbols) + tmp_str[-visible_symbols:]
    return tmp_str

def initial_data_preprocessing(transaction):
    """
    First stage of data preparation and formatting
    """
    transaction_id = transaction["data"]["statementItem"]["id"]
    # transaction_time_unix = transaction["data"]["statementItem"]["time"]
    transaction_time = datetime.fromtimestamp(transaction["data"]["statementItem"]["time"])
    description = transaction["data"]["statementItem"]["description"]
    mcc = transaction["data"]["statementItem"]["mcc"]
    # original_mcc = transaction["data"]["statementItem"]["originalMcc"]

    mcc_text = MCC.get_mcc(str(mcc)).usda_description
    # original_mcc_text = MCC.get_mcc(str(original_mcc)).usda_description

    amount = transaction["data"]["statementItem"]["amount"] / 100
    # operation_amount = transaction["data"]["statementItem"]["operationAmount"] / 100
    # currency_code = transaction["data"]["statementItem"]["currencyCode"]
    
    balance = transaction["data"]["statementItem"]["balance"] / 100
    
    return {
        "transaction_id": transaction_id,
        "transaction_time": transaction_time,
        "description": description,
        "mcc": mcc,
        "mcc_text": mcc_text,
        "amount": amount,
        "balance": balance
    }


def mono_json_response(record):
    date_time = record["transaction_time"].strftime('%Y-%m-%d %H:%M:%S')
    description = record["description"]
    category = record["mcc_text"]
    amount = record["amount"]
    balance = record["balance"]

    if amount > 0:
        transaction_type = "⬇️ Поповнення на"
    else:
        transaction_type = "⬆️ Списання"

    return f"{date_time}\n{transaction_type}: {amount} UAH\n💰Поточний баланс: {balance} UAH\n{category}\n{description}"