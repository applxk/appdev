import shelve

def store_chat_messages(messages):
    with shelve.open('chat_messages_db') as db:
        db['messages'] = messages

def retrieve_chat_messages():
    with shelve.open('chat_messages_db') as db:
        return db.get('messages', [])

def store_amount_spent(amount):
    with shelve.open('amount_db') as db:
        db['amount'] = amount

def retrieve_amount_spent():
    with shelve.open('amount_db') as db:
        return db.get('amount', 0)

def store_promo_codes(promo_codes):
    with shelve.open('promo_codes_db') as db:
        db['promo_codes'] = promo_codes

def retrieve_promo_codes():
    with shelve.open('promo_codes_db') as db:
        return db.get('promo_codes', [])