import requests
import json
import os
import matplotlib.pyplot as plt

class CurrencyConverter:
    def _init_(self, api_key):
        self.api_key = api_key
        self.base_url = "https://v6.exchangerate-api.com/v6/{}/latest/{}"
        self.history = []

    def get_rates(self, base_currency):
        """Fetch real-time currency rates for the given base currency."""
        try:
            response = requests.get(self.base_url.format(self.api_key, base_currency))
            if response.status_code == 200:
                data = response.json()
                if data["result"] == "success":
                    return data["conversion_rates"]
                else:
                    print("Error: Unable to fetch conversion rates.")
            else:
                print(f"Error: HTTP {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
        return None

    def convert_currency(self, amount, from_currency, to_currencies, rates):
        """Convert an amount from one currency to multiple currencies using the provided rates."""
        results = {}
        for to_currency in to_currencies:
            if from_currency not in rates or to_currency not in rates:
                print(f"Error: Invalid currency code {to_currency}.")
                continue
            converted_amount = amount * rates[to_currency] / rates[from_currency]
            results[to_currency] = converted_amount
            self.history.append((amount, from_currency, converted_amount, to_currency))
        return results

    def show_history(self):
        """Display the history of recent conversions."""
        if not self.history:
            print("No conversions done yet.")
        else:
            print("Conversion History:")
            for record in self.history:
                print(f"{record[0]} {record[1]} = {record[2]:.2f} {record[3]}")

    def notify_rate_change(self, base_currency, target_currency, threshold):
        """Notify the user if the exchange rate changes significantly."""
        rates = self.get_rates(base_currency)
        if rates:
            rate = rates.get(target_currency, None)
            if rate and abs(rate - threshold) > 0.05 * threshold:
                print(f"Alert: The exchange rate for {base_currency} to {target_currency} has changed significantly! Current rate: {rate}")

    def plot_currency_trend(self, base_currency, target_currency):
        """Plot currency trends over time using historical data."""
        # For simplicity, using mock data (you can integrate a historical API for real data)
        days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
        rates = [1.1, 1.2, 1.15, 1.18, 1.22]  # Mock rates

        plt.figure(figsize=(8, 5))
        plt.plot(days, rates, marker="o", label=f"{base_currency} to {target_currency}")
        plt.title("Currency Rate Trend")
        plt.xlabel("Days")
        plt.ylabel("Exchange Rate")
        plt.legend()
        plt.grid()
        plt.show()

    def run(self, input_data=None):
        """Interactive menu for the currency conversion system."""
        predefined_inputs = input_data or []
        input_index = 0

        def get_input(prompt):
            nonlocal input_index
            if input_index < len(predefined_inputs):
                user_input = predefined_inputs[input_index]
                input_index += 1
                print(f"{prompt} {user_input}")
                return user_input
            else:
                raise ValueError("No more predefined inputs available.")

        while True:
            print("\nCurrency Conversion System")
            print("1. Convert Currency")
            print("2. View Conversion History")
            print("3. Rate Change Notification")
            print("4. Plot Currency Trends")
            print("5. Exit")
            try:
                choice = get_input("Enter your choice: ")
            except ValueError:
                print("Error: Input not available in the current environment.")
                break

            if choice == "1":
                from_currency = get_input("Enter the base currency code (e.g., USD): ").upper()
                to_currencies = get_input("Enter target currency codes separated by commas (e.g., EUR,GBP,JPY): ").upper().split(",")
                try:
                    amount = float(get_input("Enter the amount to convert: "))
                except ValueError:
                    print("Invalid amount. Please enter a numeric value.")
                    continue

                rates = self.get_rates(from_currency)
                if rates:
                    results = self.convert_currency(amount, from_currency, to_currencies, rates)
                    for currency, converted in results.items():
                        print(f"\n{amount} {from_currency} = {converted:.2f} {currency}")

            elif choice == "2":
                self.show_history()

            elif choice == "3":
                base_currency = get_input("Enter the base currency code (e.g., USD): ").upper()
                target_currency = get_input("Enter the target currency code (e.g., EUR): ").upper()
                try:
                    threshold = float(get_input("Enter the threshold rate for notifications: "))
                except ValueError:
                    print("Invalid threshold. Please enter a numeric value.")
                    continue
                self.notify_rate_change(base_currency, target_currency, threshold)

            elif choice == "4":
                base_currency = get_input("Enter the base currency code (e.g., USD): ").upper()
                target_currency = get_input("Enter the target currency code (e.g., EUR): ").upper()
                self.plot_currency_trend(base_currency, target_currency)

            elif choice == "5":
                print("Exiting the system. Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "_main_":
    
    API_KEY = "your_api_key_here"

    converter = CurrencyConverter(API_KEY)


    converter.run()
