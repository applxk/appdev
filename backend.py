import shelve

def store_chat_messages(messages):
    with shelve.open('chat_messages_db') as db:
        db['messages'] = messages

def retrieve_chat_messages():
    with shelve.open('chat_messages_db') as db:
        return db.get('messages', [])

def store_amount_spent(amounts):
    with shelve.open('amount_db') as db:
        db['amount'] = amounts

def retrieve_amount_spent():
    with shelve.open('amount_db') as db:
        return db.get('amount', 0)

# 👽 (delete anything related to promo_code) 👽
# 👽 (add with everything that has won_gifts) 👽

def store_won_gifts(won_gifts):
    with shelve.open('won_gifts_db') as db:
        db['won_gifts'] = won_gifts

def retrieve_won_gifts():
    with shelve.open('won_gifts_db') as db:
        return db.get('won_gifts', [])

def store_subscribed_email(email):
    subscribed_emails = retrieve_subscribed_emails()
    subscribed_emails.append(email)
    with shelve.open('subscribed_emails_db') as db:
        db['subscribed_emails'] = subscribed_emails

def retrieve_subscribed_emails():
    with shelve.open('subscribed_emails_db') as db:
        return db.get('subscribed_emails', [])
