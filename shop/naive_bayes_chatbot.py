import json
import re
import os
import math
from collections import defaultdict, Counter
import random
from .models import Product
#from django.urls import reverse

# Path to the intents JSON file within the 'shop' app
json_file_path = os.path.join(os.path.dirname(__file__), 'data', 'intents.json')

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.split()

def train_naive_bayes(intents):
    word_counts = defaultdict(Counter)
    intent_counts = Counter()
    total_words = 0
    
    for intent in intents:
        tag = intent['tag']
        for pattern in intent['patterns']:
            words = preprocess_text(pattern)
            word_counts[tag].update(words)
            intent_counts[tag] += 1
            total_words += len(words)
    
    return word_counts, intent_counts, total_words

def classify_intent(user_input, word_counts, intent_counts, total_words):
    words = preprocess_text(user_input)
    best_intent = None
    max_prob = -float('inf')
    
    for intent, count in intent_counts.items():
        log_prob = math.log(count / total_words)
        
        for word in words:
            word_prob = (word_counts[intent][word] + 1) / (sum(word_counts[intent].values()) + len(word_counts[intent]))
            log_prob += math.log(word_prob)
        
        if log_prob > max_prob:
            max_prob = log_prob
            best_intent = intent

    return best_intent

def generate_response(user_input):
    with open(json_file_path, 'r') as file:
        intents = json.load(file)["intents"]
    
    word_counts, intent_counts, total_words = train_naive_bayes(intents)
    intent = classify_intent(user_input, word_counts, intent_counts, total_words)
    print(f"Detected intent : " ,intent)
    # Response based on detected intent
    if intent == "product_search":
        product_name = extract_product_name(user_input)
        if product_name:
            return get_product_details(product_name)
        else:
            return "Sorry, I couldn't understand the product you're asking about."

    elif intent == "category_search":
        category_name = extract_category_name(user_input)
        if category_name:
            return get_products_in_category(category_name)
        else:
            return "Sorry, we dont have the products in the category you're asking about."

    elif intent == "order_status":
        return "Please provide your order ID, and I’ll check the status for you."

    elif intent == "return_policy":
        return "You can return any product within 30 days of purchase. Visit our returns page for more details."

    elif intent == "payment_inquiry":
        return "We accept credit cards, debit cards, and PayPal. Payment is secure with SSL encryption."

    elif intent == "shipping_inquiry":
        return "Shipping usually takes 5-7 business days. You can track your order on our tracking page."

    elif intent == "customer_service":
        return "I’m here to help! What do you need assistance with?"

    elif intent == "feedback":
        return "You can leave feedback on the product page or through our contact page."

    elif intent == "greeting":
        return random.choice([res["responses"] for res in intents if res["tag"] == "greeting"][0])

    elif intent == "farewell":
        return random.choice([res["responses"] for res in intents if res["tag"] == "farewell"][0])

    elif intent == "help":
        return "I’m here to help! Let me know what you need assistance with."

    # Default response if no intent is recognized
    return "I'm not sure how to respond to that."

def extract_product_name(user_input):
    words = preprocess_text(user_input)
    keywords = ["about", "product", "item", "is", "want"]
    
    for keyword in keywords:
        if keyword in words:
            product_name_start_index = words.index(keyword) + 1
            if product_name_start_index < len(words):
                product_name = " ".join(words[product_name_start_index:]).strip()
                return product_name.replace(" ", "_").capitalize()
    return " ".join(words).strip().replace(" ", "_").capitalize()

def get_product_details(product_name):
    try:
        product = Product.objects.get(name__iexact=product_name.replace(" ", "_"))
        product.name = product.name.replace('_'," ")
        product_details = f"We have {product.name} and this will cost you about Rs.{product.price}.\n"
        
       # product_link = reverse('product_detail', args=[product.slug])  # Assuming 'product_detail' is the URL name
       # product_details += f"Here is the link to the product page: {product_link}\n"
        

        return product_details
    except Product.DoesNotExist:
        return f"Sorry, we couldn't find a product named '{product_name}'."




# related to category

def extract_category_name(user_input):
    categories = ["earring", "watch", "ring", "pendant", "necklace", "bracelet"]  # Example categories; you should expand this list
    user_input = user_input.lower()
    
    for category in categories:
        if category in user_input:
            return category
    return None

def get_products_in_category(category_name):
    # Fetch products from the database based on category
    products = Product.objects.filter(category__name__iexact=category_name)
    if products.exists():
        product_details = f"Here are the available products in the '{category_name}' category:\n"
        for product in products:
            product.name = product.name.replace('_',' ')
            product_details += f"{product.name} - Rs.{product.price}\n"
        return product_details
    else:
        return f"Sorry, we couldn't find any products in the '{category_name}' category."