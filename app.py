from flask import Flask, render_template, request, jsonify
import random
import string
from datetime import datetime
from backend import store_chat_messages, retrieve_chat_messages, store_promo_codes

app = Flask(__name__)

#customer dashboard
@app.route('/customerdashboard')
def customer_dashboard():
    return render_template('includes/customerdashboard.html')

#account details
@app.route('/accountdetails')
def account_details():
    return render_template('includes/accountdetails.html')

# wheel
@app.route('/wheel')
def wheel():
    return render_template('includes/wheel.html')

@app.route('/spin', methods=['POST'])
def spin_wheel():
    # promo codes are alphanumeric strings of length 8
    promo_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # Append the generated promo code to the list
    generated_promo_codes.append(promo_code)

    # Store the updated promo codes in shelve
    store_promo_codes(generated_promo_codes)

    return jsonify({'promo_code': promo_code})

@app.route('/get_promo_codes')
def get_promo_codes():
    return jsonify({'promo_codes': generated_promo_codes})

@app.route('/delete_promo_code', methods=['POST'])
def delete_promo_code():
    promo_code_to_delete = request.form.get('promo_code')
    if promo_code_to_delete in generated_promo_codes:
        generated_promo_codes.remove(promo_code_to_delete)

        # Store the updated promo codes in shelve
        store_promo_codes(generated_promo_codes)

        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Promo code not found'}), 404


#coupons

# List to store generated promo codes
generated_promo_codes = []

@app.route('/mycoupons')
def my_coupons():
    return render_template('includes/mycoupons.html', promo_codes=generated_promo_codes)

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


#membership
cumulative_amounts = []

@app.route('/edit_amount_spent', methods=['POST'])
def edit_amount_spent():
    try:
        amount_spent = int(request.form.get('amount_spent'))
        cumulative_amounts.clear()
        cumulative_amounts.append(amount_spent)
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


if __name__ == '__main__':
    app.run(debug=True)
