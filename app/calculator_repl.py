########################
# Calculator REPL       #
########################

import colorama
from colorama import Fore, Style
from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory


def calculator_repl():
    """
    Command-line interface for the calculator.

    Implements a Read-Eval-Print Loop (REPL) that continuously prompts the user
    for commands, processes arithmetic operations, and manages calculation history.
    """
    try:
        # Initialize the Calculator instance
        calc = Calculator()

        # Register observers for logging and auto-saving history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print("Calculator started. Type 'help' for commands.")

        while True:
            #initialize colorama for colored terminal output
            colorama.init()
            try:
                # Prompt the user for a command
                print(Fore.MAGENTA)
                command = input("\nEnter command: ").lower().strip()
                print(Style.RESET_ALL)


                if command == 'help':
                    # Display available commands
                    print("\nAvailable commands:")
                    print("add, subtract, multiply, divide, power, root," 
                          + "modulus ,int_divide, percent, abs_diff- Perform calculations")
                    print("  history - Show calculation history")
                    print("  clear - Clear calculation history")
                    print("  undo - Undo the last calculation")
                    print("  redo - Redo the last undone calculation")
                    print("  save - Save calculation history to file")
                    print("  load - Load calculation history from file")
                    print("  exit - Exit the calculator")
                    continue

                if command == 'exit':
                    # Attempt to save history before exiting
                    try:
                        calc.save_history()
                        print(Fore.GREEN)
                        print("History saved successfully.")
                        print(Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED)
                        print(f"Warning: Could not save history: {e}")
                        print(Style.RESET_ALL)
                    print("Goodbye!")
                    break

                if command == 'history':
                    # Display calculation history
                    history = calc.show_history()
                    if not history:
                        print(Fore.RED)
                        print("No calculations in history")
                        print(Style.RESET_ALL)
                    else:
                        print("\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}")
                    continue

                if command == 'clear':
                    # Clear calculation history
                    calc.clear_history()
                    print(Fore.GREEN)
                    print("History cleared")
                    print(Style.RESET_ALL)
                    continue

                if command == 'undo':
                    # Undo the last calculation
                    if calc.undo():
                        print(Fore.GREEN)
                        print("Operation undone")
                        print(Style.RESET_ALL)

                    else:
                        print(Fore.RED)
                        print("Nothing to undo")
                        print(Style.RESET_ALL)
                    continue

                if command == 'redo':
                    # Redo the last undone calculation
                    if calc.redo():
                        print(Fore.GREEN)
                        print("Operation redone")
                        print(Fore.GREEN)
                    else:
                        print(Fore.RED)
                        print("Nothing to redo")
                        print(Style.RESET_ALL)
                    continue

                if command == 'save':
                    # Save calculation history to file
                    try:
                        calc.save_history()
                        print(Fore.GREEN)
                        print("History saved successfully")
                        print(Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED)
                        print(f"Error saving history: {e}")
                        print(Style.RESET_ALL)
                    continue

                if command == 'load':
                    # Load calculation history from file
                    try:
                        calc.load_history()
                        print(Fore.GREEN)
                        print("History loaded successfully")
                        print(Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED)
                        print(f"Error loading history: {e}")
                        print(Style.RESET_ALL)
                    continue

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root',
                                'modulus', 'int_divide', 'percent', 'abs_diff']:
                    # Perform the specified arithmetic operation
                    try:
                        print("\nEnter numbers (or 'cancel' to abort):")
                        print(Fore.YELLOW)
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print("Operation cancelled")
                            continue
                        print(Fore.YELLOW)
                        b = input("Second number: ")
                        print(Style.RESET_ALL)
                        if b.lower() == 'cancel':
                            print("Operation cancelled")
                            continue

                        # Create the appropriate operation instance using the Factory pattern
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # Perform the calculation
                        result = calc.perform_operation(a, b)

                        # Normalize the result if it's a Decimal
                        if isinstance(result, Decimal):
                            result = result.normalize()
                        
                        print(Fore.CYAN)
                        print(f"\nResult: {result}")
                        print(Style.RESET_ALL)
                    except (ValidationError, OperationError) as e:
                        # Handle known exceptions related to validation or operation errors
                        print(Fore.RED)
                        print(f"Error: {e}")
                        print(Style.RESET_ALL)
                    except Exception as e:
                        # Handle any unexpected exceptions
                        print(Fore.RED)
                        print(f"Unexpected error: {e}")
                        print(Style.RESET_ALL)
                    continue

                # Handle unknown commands
                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                # Handle Ctrl+C interruption gracefully
                print(Fore.RED)
                print("\nOperation cancelled")
                print(Style.RESET_ALL)

                continue
            except EOFError:
                # Handle end-of-file (e.g., Ctrl+D) gracefully
                print(Fore.RED)
                print("\nInput terminated. Exiting...")
                print(Style.RESET_ALL)
                break
            except Exception as e:
                # Handle any other unexpected exceptions
                print(Fore.RED)
                print(f"Error: {e}")
                print(Style.RESET_ALL)
                continue

    except Exception as e:
        # Handle fatal errors during initialization
        print(Fore.Red)
        print(f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        print(Style.RESET_ALL)
        raise
