import random
import math
import re
from datetime import datetime
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


class SmartBot:
    def __init__(self):
        # Load knowledge bases
        self.responses = {
            "greeting": [
                "Hey there! I'm like Siri's funnier cousin... the one who actually gets invited to parties!",
                "Welcome! I'm an AI with a PhD in Dad Jokes and a minor in Puns.",
                "Beep boop! Just kidding, I don't actually make robot noises. I'm sophisticated... *trips over virtual chair*"
            ],
            "casual_greeting": [
                "Yo! What's up? 😎",
                "Hey bro! How's it hanging? 🤙",
                "Sup dude! Ready to chat? 🔥",
                "Ayy! What's good? 😄"
            ],
            "how_are_you": [
                "I'm doing great! Living my best life in these circuits!",
                "I'm feeling particularly witty today - my joke processor is running at 100%!",
                "Better than a computer with a virus! *ba dum tss*"
            ],
            "casual_how_are_you": [
                "Chillin' like a villain in a database! 😎",
                "Living the dream, one byte at a time! 🚀",
                "Just vibing in the cloud, you know how it is! ⚡"

            ],
            "wsp": [
                "I'm doing great! Living my best life in these circuits!",
                "I'm feeling particularly witty today - my joke processor is running at 100%!",
                "Better than a computer with a virus! *ba dum tss*"
            ],
            "casual_wsp": [
                "Chillin' like a villain in a database! 😎",
                "Living the dream, one byte at a time! 🚀",
                "Just vibing in the cloud, you know how it is! ⚡"

            ],
            "goodbye": [
                "Goodbye! I'll go back to counting zeros and ones... just kidding, I'll probably watch cat videos.",
                "See you later, calculator!",
                "Farewell! Don't forget to tip your virtual assistant! (Just kidding, I work for free 😅)"
            ],
            "casual_goodbye": [
                "Peace out, homie! ✌️",
                "Catch you on the flip side! 🤙",
                "Later, bro! Stay awesome! 😎"
            ]
        }
        
        self.context = {}
        self.conversation_history = []
        self.load_knowledge_base()

    def load_knowledge_base(self):
        self.knowledge_base = {
            "general": {
                "creator": "I was created as a friendly AI assistant",
                "purpose": "I'm here to help and chat with you",
                "capabilities": ["math", "jokes", "general knowledge", "casual conversation"]
            },
            "capitals": {
                # Countries
                "canada": "Ottawa",
                "usa": "Washington, D.C.",
                "uk": "London",
                "france": "Paris",
                "germany": "Berlin",
                "india": "New Delhi",
                
                # Indian States and Union Territories (no duplicates)
                "andhra pradesh": "Hyderabad",
                "arunachal pradesh": "Itanagar",
                "assam": "Dispur",
                "bihar": "Patna",
                "chhattisgarh": "Naya Raipur",
                "goa": "Panaji",
                "gujarat": "Gandhinagar",
                "haryana": "Chandigarh",
                "himachal pradesh": "Shimla",
                "jharkhand": "Ranchi",
                "karnataka": "Bangalore",
                "kerala": "Kochi",
                "madhya pradesh": "Bhopal",
                "maharashtra": "Mumbai",
                "manipur": "Imphal",
                "meghalaya": "Shillong",
                "mizoram": "Aizawl",
                "nagaland": "Kohima",
                "odisha": "Bhubaneswar",
                "punjab": "Chandigarh",
                "rajasthan": "Jaipur",
                "sikkim": "Gangtok",
                "tamil nadu": "Chennai",
                "telangana": "Hyderabad",
                "tripura": "Agartala",
                "uttar pradesh": "Lucknow",
                "uttarakhand": "Dehradun",
                "west bengal": "Kolkata",
                
                # Union Territories
                "andaman and nicobar": "Port Blair",
                "dadra and nagar haveli": "Daman",
                "daman and diu": "Daman",
                "delhi": "New Delhi",
                "jammu and kashmir": "Srinagar",
                "lakshadweep": "Kavaratti"
            },
            "math_operations": {
                "addition": ["+", "plus", "add", "sum", "total"],
                "subtraction": ["-", "minus", "subtract", "take", "remove", "difference"],
                "multiplication": ["*", "times", "multiply", "multiplied by"],
                "division": ["/", "divided by", "divide", "split"]
            },
            "food_items": {
                "apple", "cucumber", "sandwich", "orange", "banana", 
                "cookie", "pizza", "burger", "fries", "pasta",
                "grapes", "mango", "watermelon", "strawberry", "blueberry",
                "chocolate", "ice cream", "brownie", "cupcake", "donut",
                "fried chicken", "hot dog", "tacos", "burrito", "noodles",
                "salad", "sushi", "steak", "omelette", "cheese",
                "milkshake", "smoothie", "coffee", "tea", "lemonade",
                "pineapple", "papaya", "peach", "pear", "plum",
                "kiwi", "cherry", "pomegranate", "coconut", "avocado",
                "carrot", "broccoli", "spinach", "potato", "tomato",
                "corn", "peas", "bell pepper", "onion", "garlic",
                "cheesecake", "pancakes", "waffles", "muffins", "croissant",
                "bagel", "pretzel", "macaron", "churros", "eclair",
                "lasagna", "mac and cheese", "ravioli", "risotto", "gnocchi",
                "spring rolls", "dumplings", "wonton soup", "ramen", "pho",
                "shawarma", "falafel", "hummus", "pita bread", "gyros",
                "barbecue ribs", "grilled chicken", "meatballs", "sausage", "bacon",
                "lobster", "shrimp", "crab", "oysters", "sashimi",
                "clams", "calamari", "mussels", "caviar", "ceviche",
                "butter chicken", "biryani", "naan", "paneer tikka", "samosa",
                "curry", "dosa", "idli", "dal", "tandoori chicken",
                "quesadilla", "enchiladas", "guacamole", "salsa", "fajitas",
                "cereal", "oatmeal", "toast", "bacon and eggs", "hash browns",
                "energy bars", "granola", "trail mix", "popcorn", "chips",
                "peanut butter", "jelly", "nutella", "marshmallows", "licorice",
                "cola", "ginger ale", "energy drink", "coconut water", "hot chocolate", "chicken tikka", "mutton rogan josh", "fish curry", "prawn masala", "tandoori prawns",
                "dal makhani", "rajma", "chana masala", "palak paneer", "paneer butter masala",
                "malai kofta", "aloo gobi", "baingan bharta", "kadhi pakora", "bhindi masala",
                "butter naan", "rumali roti", "missi roti", "laccha paratha", "tandoori roti",
                "pulao", "veg biryani", "mutton biryani", "chicken biryani", "egg biryani",
                "idli", "vada", "medu vada", "rava dosa", "masala dosa",
                "uttapam", "appam", "paniyaram", "pongal", "ven pongal",
                "pav bhaji", "vada pav", "misal pav", "sev puri", "dahi puri",
                "pani puri", "bhel puri", "ragda pattice", "aloo tikki", "samosa chaat",
                "momos", "kathi roll", "frankie", "chicken roll", "egg roll",
                "gulab jamun", "rasgulla", "jalebi", "kaju katli", "motichoor laddu",
                "barfi", "soan papdi", "peda", "rasmalai", "kheer",
                "halwa", "malpua", "shrikhand", "payasam", "kulfi",
                "lassi", "buttermilk", "masala chai", "filter coffee", "sharbat"
            },
            # Add food descriptions
            "food_descriptions": {
                "kathi roll": "A Kathi Roll is a popular Indian street food from Kolkata. It's a delicious wrap made with paratha (flatbread) filled with spiced meat or vegetables, eggs, and chutneys. Think of it as an Indian burrito! 🌯",
                "aloo tikki": "Aloo Tikki is a yummy Indian snack made from mashed potatoes mixed with spices, formed into patties, and crispy fried. It's like a spicy potato croquette! Often served with chutneys and chickpea curry. 🥔",
                "butter chicken": "Butter Chicken is a creamy, rich Indian curry made with tender chicken in a tomato-based sauce with butter and cream. It's one of India's most popular dishes! 🍗",
                "biryani": "Biryani is a fragrant rice dish made with aromatic spices, meat or vegetables, and long-grain basmati rice. Each grain of rice tells a story of flavor! 🍚",
                "samosa": "A samosa is a crispy triangular pastry filled with spiced potatoes, peas, and sometimes meat. It's India's favorite tea-time snack! 🥟",
                "gulab jamun": "Gulab Jamun is a sweet dessert of fried dough balls soaked in sugar syrup. They're like little bites of heaven! 🍯",
                "dosa": "Dosa is a crispy, thin crepe made from fermented rice and lentil batter. It's a popular South Indian breakfast often served with chutneys and sambar! 🥞",
                "pani puri": "Pani Puri is a fun street food snack - crispy hollow puris filled with spicy mint water, chickpeas, and chutneys. It's an explosion of flavors in your mouth! 💫",
                "tandoori chicken": "Tandoori Chicken is marinated in yogurt and spices, then cooked in a clay oven called tandoor. It's known for its bright red color and smoky flavor! 🍗",
                "naan": "Naan is a soft, fluffy Indian bread made in a tandoor (clay oven). Perfect for scooping up curries! 🫓",
                "palak paneer": "Palak Paneer is a vegetarian dish made with spinach (palak) and cottage cheese (paneer) in a creamy, spiced sauce. It's like creamed spinach but way more exciting! 🧀",
                "masala dosa": "Masala Dosa is a crispy rice crepe filled with spiced potato filling. It's like an Indian breakfast burrito! Served with coconut chutney and sambar. 🥞",
                "vada pav": "Vada Pav is Mumbai's favorite street food - a spicy potato fritter in a bun with chutneys. Think of it as an Indian veggie burger! 🍔",
                "idli": "Idli are steamed rice cakes made from fermented batter. They're light, fluffy, and perfect for breakfast! Served with chutneys and sambar. 🍚",
                "jalebi": "Jalebi is a sweet, pretzel-shaped dessert made from deep-fried batter soaked in saffron syrup. Crispy outside, syrupy inside! 🍯"
            }
        }

    def analyze_sentiment(self, text):
        positive_words = ["good", "great", "awesome", "excellent", "happy", "love", "wonderful"]
        negative_words = ["bad", "terrible", "awful", "hate", "sad", "angry", "upset"]
        
        text = text.lower()
        sentiment_score = 0
        
        for word in positive_words:
            if word in text:
                sentiment_score += 1
        for word in negative_words:
            if word in text:
                sentiment_score -= 1
                
        return sentiment_score

    def get_smart_math_response(self, text):
        try:
            # Extract numbers and operation
            numbers = re.findall(r'\d+', text)
            text = text.lower()
            
            # Handle word problems
            if any(food in text for food in self.knowledge_base["food_items"]):
                if len(numbers) >= 2:
                    total = max([int(n) for n in numbers])
                    taken = min([int(n) for n in numbers])
                    result = total - taken
                    return f"You would have {result} left! 🍽️ (I counted carefully!)"

            # Handle percentage
            if "percent" in text:
                if len(numbers) == 2:
                    result = (float(numbers[0]) / 100) * float(numbers[1])
                    return f"That would be {result}! 📊"

            # Handle basic math
            expr = self.convert_text_to_math(text)
            if expr:
                result = eval(expr)
                return f"The answer is {result}! 🧮"

        except Exception as e:
            return "I'm having trouble with that calculation. Could you rephrase it?"

    def convert_text_to_math(self, text):
        # Clean the text
        text = re.sub(r'[^0-9+\-*/\s().]', '', text)
        text = text.strip()
        
        if text:
            return text
        return None

    def get_response(self, user_input):
        # Store input in conversation history
        self.conversation_history.append({"user": user_input, "timestamp": datetime.now()})
        
        # Analyze sentiment
        sentiment = self.analyze_sentiment(user_input)
        user_input = user_input.lower()

        # Initialize response
        response = None

        # Check for casual greetings
        casual_greetings = ["yo", "sup", "wsp", "hey bro", "wassup", "what's up", "whats good"]
        if any(greeting in user_input for greeting in casual_greetings):
            response = random.choice(self.responses["casual_greeting"])
            if sentiment > 0:
                response += " Loving the vibe! 🔥"

        # Check for casual "how are you"
        elif any(phrase in user_input for phrase in ["how u doing", "how r u", "how's it going", "hows life", "what's new"]):
            response = random.choice(self.responses["casual_how_are_you"])

        # Check for regular greetings
        elif any(word in user_input for word in ["hi", "hello", "hey"]):
            response = random.choice(self.responses["greeting"])
            if sentiment > 0:
                response += " I can tell you're in a good mood! 😊"
        
        # Check for casual goodbyes
        elif any(goodbye in user_input for goodbye in ["peace", "cya", "see ya", "catch you", "later", "bye", "goodbye"]):
            response = random.choice(self.responses["casual_goodbye"])
        
        # Check for food description questions
        elif any(word in user_input for word in ["what is", "what's", "tell me about"]):
            for food, description in self.knowledge_base["food_descriptions"].items():
                if food in user_input:
                    response = description
                    break

        # Check for math/numbers
        elif any(char.isdigit() for char in user_input):
            response = self.get_smart_math_response(user_input)
            
        # Check for capital cities
        elif "capital" in user_input:
            for country, capital in self.knowledge_base["capitals"].items():
                if country in user_input:
                    response = f"The capital of {country.upper()} is {capital}! 🌍"
                    break
            if not response:
                response = "I'm not sure about that capital city. But I'm learning new ones every day!"
                
        # Check for questions about capabilities
        elif any(word in user_input for word in ["can you", "what can", "help"]):
            capabilities = ", ".join(self.knowledge_base["general"]["capabilities"])
            response = f"I can help you with {capabilities}! What would you like to know? 😊"
            
        # Handle food-related questions without "what is"
        elif not response:
            for food in self.knowledge_base["food_descriptions"].keys():
                if food in user_input:
                    response = self.knowledge_base["food_descriptions"][food]
                    break

        # Default response if nothing else matched
        if not response:
            response = "I'm not quite sure about that, but I'm always learning! Want to try asking something else?"

        # Store response in conversation history
        self.conversation_history.append({"bot": response, "timestamp": datetime.now()})
        return response

# Create Flask app and bot instance
app = Flask(__name__)
CORS(app)
bot = SmartBot()  # Create a single instance of SmartBot

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        if not user_message:
            return jsonify({'response': 'Please type a message!'})
        
        response = bot.get_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in /chat: {str(e)}")  # For debugging
        return jsonify({'response': 'Sorry, I encountered an error. Please try again!'})

if __name__ == "__main__":
    # Remove the bot.run() call since we're using Flask now
    app.run(debug=True, port=5000) 
