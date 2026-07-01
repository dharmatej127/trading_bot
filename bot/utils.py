"""
Utility functions for output formatting, CLI coloring, and prompt confirmations.
"""

from typing import Any
import sys
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)


def print_success(message: str) -> None:
    """Prints a green success message to the CLI."""
    print(f"{Fore.GREEN}{Style.BRIGHT}{message}")


def print_error(message: str) -> None:
    """Prints a red error message to the CLI."""
    print(f"{Fore.RED}{Style.BRIGHT}Error: {message}", file=sys.stderr)


def print_info(message: str) -> None:
    """Prints a blue info message to the CLI."""
    print(f"{Fore.CYAN}{message}")


def print_warning(message: str) -> None:
    """Prints a yellow warning message to the CLI."""
    print(f"{Fore.YELLOW}{Style.BRIGHT}Warning: {message}")


def ask_confirmation(message: str) -> bool:
    """
    Asks the user for confirmation (y/n) on the console.
    
    Returns True if user confirms, False otherwise.
    """
    try:
        response = input(f"{Fore.YELLOW}{message} (y/n): ").strip().lower()
        return response in ("y", "yes")
    except (KeyboardInterrupt, EOFError):
        print("\nOperation cancelled by user.")
        return False


def print_order_request(
    symbol: str, side: str, order_type: str, quantity: float, price: float | None
) -> None:
    """
    Prints order request details in the required format.
    """
    print(f"\n{Fore.CYAN}========================")
    print(f"{Fore.CYAN}Order Request")
    print(f"{Fore.CYAN}========================")
    print(f"Symbol:   {symbol}")
    print(f"Side:     {side}")
    print(f"Type:     {order_type}")
    print(f"Quantity: {quantity}")
    if price is not None:
        print(f"Price:    {price}")
    print(f"{Fore.CYAN}========================\n")


def print_order_response(response: dict[str, Any]) -> None:
    """
    Prints order execution response details in the required format.
    """
    print(f"\n{Fore.GREEN}========================")
    print(f"{Fore.GREEN}Order Response")
    print(f"{Fore.GREEN}========================")
    print(f"Order ID:          {response.get('order_id')}")
    print(f"Status:            {response.get('status')}")
    print(f"Executed Quantity: {response.get('executed_qty')}")
    
    avg_price = response.get("avg_price")
    if avg_price is not None:
        print(f"Average Price:     {avg_price}")
    else:
        print("Average Price:     N/A")
        
    print(f"Client Order ID:   {response.get('client_order_id')}")
    print(f"Timestamp:         {response.get('update_time')}")
    print(f"{Fore.GREEN}========================\n")
    print_success("Order placed successfully.")
