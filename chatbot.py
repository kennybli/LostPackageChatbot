# Lost Package Tracking Chatbot

import sys
import random

# Track if user has already requested an agent once
agent_requested_once = False


# Simulates looking up order status based on the last digit of the order ID.
# Returns one of: 'POSSIBLY_LOST', 'IN_TRANSIT', 'OUT_FOR_DELIVERY', 'DELIVERED'
def get_order_status(order_id: str) -> str:
    last_digit = int(order_id[-1])

    if last_digit == 0:
        return "POSSIBLY_LOST"
    elif 1 <= last_digit <= 3:
        return "IN_TRANSIT"
    elif 4 <= last_digit <= 6:
        return "OUT_FOR_DELIVERY"
    else:  # 7, 8, 9
        return "DELIVERED"


# Validates that the order ID is exactly 10 digits and is a number.
# Error Handling #1: Invalid order ID format
def validate_order_id(order_id: str) -> bool:
    return order_id.isdigit() and len(order_id) == 10


# Checks if user wants to speak to an agent immediately.
def check_for_agent_request(user_input: str) -> bool:
    return user_input.lower() in ["agent", "representative", "human", "speak to agent"]


# Handles agent request and also asks again on first attempt.
# Returns True if should escalate, False if gave soft redirect.
def handle_agent_request() -> bool:
    global agent_requested_once
    
    if not agent_requested_once:
        # First request - try to keep them with the chatbot
        agent_requested_once = True
        print("\nI understand you'd like to speak with an agent.")
        print("Before I connect you, I want to make sure I can't help resolve your issue.")
        print("I can assist with tracking packages, delivery updates, and escalating lost orders.")
        print("If you still want to speak with an agent, just type 'agent' again.\n")
        return False
    else:
        # Second request - escalate to agent
        return True


# Simulates connecting the user to a customer support agent.
def escalate_to_agent():
    print("\nConnecting you to a customer support agent...")
    print("A representative will be with you shortly. Thank you for your patience!")


# Ends the chatbot conversation with a closing message.
def end_conversation():
    print("Thank you for using the Lost Package Assistant. Goodbye!")
    sys.exit(0)


# Prompts the user for a yes/no response with error handling.
# Error Handling #2: Unexpected yes/no responses
# Also allows user to type "agent" at any time to skip to a human.
def get_yes_no_response(prompt: str) -> bool:
    while True:
        response = input(prompt).strip().lower()
        
        # Check if user wants to skip to an agent
        if check_for_agent_request(response):
            if handle_agent_request():
                escalate_to_agent()
                end_conversation()
            else:
                # Soft redirect given, repeats previous prompt for yes/no
                continue
        
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            return False
        else:
            print("I didn't quite understand that. Please type 'yes' or 'no'.")


# Generates a random reference number for investigation/refund requests.
def generate_reference_number(prefix: str) -> str:
    return f"{prefix}-{random.randint(1000000, 9999999)}"


# Handles filing an investigation request for a lost package.
def file_investigation(order_id: str):
    print("\nI'll file an investigation request for your package.")
    
    # Generate reference number and confirm
    ref_number = generate_reference_number("KENNY")
    print(f"\nInvestigation request submitted!")
    print(f"Reference #: {ref_number}")
    print(f"Order ID: {order_id}")
    print("You'll receive an email update within 24-48 hours.")


# Handles processing a refund request for a lost package.
def request_refund(order_id: str):
    print("\nI'll process a refund request for your order.")
    
    ref_number = generate_reference_number("KENNY")
    print(f"\nRefund request submitted!")
    print(f"Reference #: {ref_number}")
    print(f"Order ID: {order_id}")
    print("Your refund will be processed within 3-5 business days.")


# Handles the menu for a possibly lost package with self service options.
def handle_possibly_lost(order_id: str):
    print("Your package may be lost. What would you like to do?")
    print("1. File an investigation request")
    print("2. Request a refund")
    print("3. Speak to an agent")
    
    while True:
        choice = input("\nPlease enter 1, 2, or 3: ").strip()
        
        # Check for agent request
        if check_for_agent_request(choice):
            if handle_agent_request():
                escalate_to_agent()
                return
            else:
                continue
        
        if choice == "1":
            file_investigation(order_id)
            return
        elif choice == "2":
            request_refund(order_id)
            return
        elif choice == "3":
            escalate_to_agent()
            return
        else:
            print("I didn't understand that. Please enter 1, 2, or 3.")


# Main chatbot conversation flow.
def main():
    
    # Welcome message
    print("Hi! I'm here to help you track a lost or delayed package.")


    # Step 1: Get and validate order ID (with retry loop)
    while True:
        order_id = input("Please enter your 10 digit order ID: ").strip()
        
        # Check if user wants to skip to an agent
        if check_for_agent_request(order_id):
            if handle_agent_request():
                escalate_to_agent()
                end_conversation()
            else:
                # Soft redirect given, continue the loop
                continue
        
        if validate_order_id(order_id):
            break
        else:
            # Error Handling #1: Invalid order ID
            print("That doesn't look like a valid order ID number. "
                  "It should be a 10 digit number. Please try again.\n")

    # Step 2: Look up order status
    status = get_order_status(order_id)
    print()  # Adds spacing for readability

    # Step 3: Handle based on status
    if status == "POSSIBLY_LOST":
        handle_possibly_lost(order_id)

    elif status == "IN_TRANSIT":
        print("Your order is currently on the way.")
        if get_yes_no_response("Is there anything else I can help you with? "):
            print("\nI'm sorry that you're having troubles with your order.")
            if get_yes_no_response("Would you like to speak to a customer support agent? "):
                escalate_to_agent()
            else:
                print("\nAlright, please reach out if you need further assistance.")

    elif status == "OUT_FOR_DELIVERY":
        print("You should be expecting your package today.")
        if get_yes_no_response("Is there anything else I can help you with? "):
            print("\nI'm sorry that you're having troubles with your order.")
            if get_yes_no_response("Would you like to speak to a customer support agent? "):
                escalate_to_agent()
            else:
                print("\nAlright, please reach out if you need further assistance.")

    elif status == "DELIVERED":
        if get_yes_no_response("Your order shows as delivered. Have you received it? "):
            print("\nGreat! I'm glad I was able to help you today.")
            print("Please let me know if you have any other issues.")
        else:
            print("\nI'm sorry that you're having troubles with your order.")
            if get_yes_no_response("Would you like to speak to a customer support agent? "):
                escalate_to_agent()
            else:
                print("\nAlright, please reach out if you need further assistance.")

    # Closing message
    end_conversation()


if __name__ == "__main__":
    main()
