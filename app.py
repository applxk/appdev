from flask import Flask, render_template, request, jsonify, redirect, url_for
from random import choice # 👽(add thisss) 👽
from datetime import datetime
from backend import store_chat_messages, retrieve_chat_messages, retrieve_amount_spent, store_amount_spent, retrieve_won_gifts, store_won_gifts, store_subscribed_email, retrieve_subscribed_emails
# 👽(add  retrieve_won_gifts, store_won_gifts) 👽

app = Flask(__name__)

#customer dashboard
@app.route('/customerdashboard')
def customer_dashboard():
    return render_template('includes/customerdashboard.html')

#account details
@app.route('/accountdetails')
def account_details():
    return render_template('includes/accountdetails.html')

# 👽(copy everything from #wheel & #coupons) 👽
# 👽(also delete anything related to promo_code) 👽
# wheel
@app.route('/wheel')
def wheel():
    return render_template('includes/wheel.html')

free_gifts = [
    "Reglow sticker set",
    "Metal straw sets",
    "bamboo cutlery sets",
    "Reglow water bottle",
    "Reglow tote bag",
    "Reglow plushie"
]

@app.route('/spin', methods=['POST'])
def spin_wheel():
    # Choose a random free gift
    selected_gift = choice(free_gifts)

    # Store the won gift
    won_gifts = retrieve_won_gifts()
    won_gifts.append(selected_gift)
    store_won_gifts(won_gifts)

    return jsonify({'gift': selected_gift})

@app.route('/get_won_gifts')
def get_won_gifts():
    won_gifts = retrieve_won_gifts()
    return jsonify({'won_gifts': won_gifts})

@app.route('/delete_gift', methods=['POST'])
def delete_gift():
    gift_to_delete = request.form.get('gift')
    won_gifts = retrieve_won_gifts()

    if gift_to_delete in won_gifts:
        won_gifts.remove(gift_to_delete)
        store_won_gifts(won_gifts)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Gift not found'}), 404

#coupons

@app.route('/mycoupons')
def my_coupons():
    won_gifts = retrieve_won_gifts()
    return render_template('includes/mycoupons.html', won_gifts=won_gifts)


#chatbot

# List to store chat messages
chat_messages = []


@app.route('/')
def home():
    return render_template('includes/index.html', current_url=request.path)


@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form.get('user_input')

    if user_input:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted_message = f'[{timestamp}] User: {user_input}'

        chat_messages.append(formatted_message)

        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Empty message'})


@app.route('/get_messages')
def get_messages():
    return jsonify({'messages': chat_messages})

def chatbot_response(user_message):
    user_message_lower = user_message.lower()

    if any(greeting in user_message_lower for greeting in ['hi', 'hello', 'hey']):
        return "Greetings! 👋 How may I help you?"

    elif 'how are you' in user_message_lower:
        return "I'm just a chatbot, but thanks for asking! 😊"

    elif any(greeting in user_message_lower for greeting in ['bye', 'goodbye', 'see you']):
        return "Bye! Have a good day! 👋"

    elif any(greeting in user_message_lower for greeting in ['thank you', 'thanks']):
        return "You're welcome! Have a good day! 👋"

    elif 'paper bag' in user_message_lower:
        reference_link = 'https://www.example.com/products/paper-bag'
        return f"Sure! You can find details about the paper bag [here]({reference_link}). <br> Are there any other inquiries?"

    elif 'polymailer' in user_message_lower:
        reference_link = 'https://www.example.com/products/polymailer'
        return f"Sure! You can find details about the polymailer [here]({reference_link}). <br> Are there any other inquiries?"

    elif 'plastic bag' in user_message_lower:
        reference_link = 'https://www.example.com/products/plastic-bag'
        return f"Sure! You can find details about the plastic bag [here]({reference_link}). <br> Are there any other inquiries?"

    else:
        if not is_english(user_message_lower):
            return "Sorry, I only understand English. Please use Google Translate and send the response. Thank you."

        return "I'm not sure how to respond to that. 😓 Can you please be more specific?"

def is_english(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

#chatbot backend
@app.route('/chatbotbackend_viewer')
def chatbotbackend_viewer():
    return render_template('includes/chatbotbackend.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']

    # Generate chatbot response
    response = chatbot_response(user_message)

    # Append user and chatbot messages to chat_messages list
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_formatted_message = f'[{timestamp}] User: {user_message}'
    chat_messages.append(user_formatted_message)

    chatbot_formatted_message = f'[{timestamp}] Chatbot: {response}'
    chat_messages.append(chatbot_formatted_message)

    # Store messages using shelves
    store_chat_messages(chat_messages)

    return response

@app.route('/delete_message', methods=['POST'])
def delete_message():
    index_to_delete = int(request.form.get('index'))

    if 0 <= index_to_delete < len(chat_messages):
        deleted_message = chat_messages.pop(index_to_delete)

        # Store the updated chat messages in shelve
        store_chat_messages(chat_messages)

        return jsonify({'success': True, 'deleted_message': deleted_message})
    else:
        return jsonify({'success': False, 'message': 'Invalid index'}), 400


#membership
cumulative_amounts = retrieve_amount_spent() or []

@app.route('/edit_amount_spent', methods=['POST'])
def edit_amount_spent():
    try:
        amount_spent = int(request.form.get('amount_spent'))

        # Append the new amount to the cumulative_amounts list
        cumulative_amounts.append(amount_spent)

        # Store the updated cumulative amounts in shelve
        store_amount_spent(cumulative_amounts)

        return jsonify(success=True)

    except ValueError as ve:
        return jsonify(error=f"Invalid amount provided: {str(ve)}")

    except Exception as e:
        return jsonify(error=f"An error occurred: {str(e)}")

def calculate_total_amount_spent():
    return sum(cumulative_amounts)

@app.route('/get_amount_spent')
def get_amount_spent():
    total_amount_spent = calculate_total_amount_spent()
    return jsonify({'amount_spent': total_amount_spent})

@app.route('/update_amount_spent', methods=['POST'])
def update_amount_spent():
    try:
        amount_spent = int(request.form.get('amount_spent'))

        # Store the cumulative amount directly
        cumulative_amounts.clear()
        cumulative_amounts.append(amount_spent)

        return jsonify(success=True)

    except ValueError as ve:
        return jsonify(error=f"Invalid amount provided: {str(ve)}")

    except Exception as e:
        return jsonify(error=f"An error occurred: {str(e)}")

@app.route('/reset_amount_spent', methods=['POST'])
def reset_amount_spent():
    cumulative_amounts.clear()  # Clear the list to reset the cumulative amount
    return jsonify(success=True)

@app.route('/membership')
def membership():
    return render_template('includes/membership.html')

#membership backend
@app.route('/membershipbackend')
def membership_backend():
    return render_template('includes/membershipbackend.html')


#shipping and delivery
@app.route('/shippinganddelivery')
def shipping_and_delivery():
    return render_template('includes/shippinganddelivery.html')

#terms and conditions
@app.route('/termsandconditions')
def terms_and_conditions():
    return render_template('includes/termsandconditions.html')

#newsletter thank you page
@app.route('/newsletterthankyou')
def newsletter_thank_you():
    return render_template('includes/newsletterthankyou.html')

#newsletter backend
@app.route('/newsletterbackend', methods=['GET'])
def newsletter_backend():
    # Retrieve subscribed emails using the function
    subscribed_emails = retrieve_subscribed_emails()

    # Pass the function as a variable to the template
    return render_template('includes/newsletterbackend.html', retrieve_subscribed_emails=retrieve_subscribed_emails, subscribed_emails=subscribed_emails)

@app.route('/subscribe_to_newsletter', methods=['POST'])
def subscribe_to_newsletter():
    email = request.form.get('email')

    # Store the email in the Shelve database
    store_subscribed_email(email)

    print(f"Subscribed email: {email}")

    return redirect(url_for('newsletter_thank_you'))

@app.route('/delete_subscribed_email', methods=['POST'])
def delete_subscribed_email():
    email_to_delete = request.form.get('email')
    subscribed_emails = retrieve_subscribed_emails()

    if email_to_delete in subscribed_emails:
        subscribed_emails.remove(email_to_delete)

        # Store the updated subscribed emails in shelve
        store_subscribed_email(subscribed_emails)

        return redirect(url_for('newsletter_backend'))
    else:
        return jsonify({'success': False, 'message': 'Email not found'}), 404

if __name__ == '__main__':

    # List to store chat messages
    chat_messages = retrieve_chat_messages()

    app.run(debug=True)
