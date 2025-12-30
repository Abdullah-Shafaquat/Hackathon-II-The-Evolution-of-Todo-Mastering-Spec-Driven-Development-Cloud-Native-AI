"""Main entry point for Todo Console App"""

import sys
import signal
from src import console_ui


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully (T110, T111)."""
    print("\nGoodbye!")
    sys.exit(0)


def setup_signal_handlers() -> None:
    """Register signal handlers for graceful shutdown (T110)."""
    signal.signal(signal.SIGINT, signal_handler)


def run_main_loop() -> None:
    """Run the main application loop (T112, T113)."""
    while True:
        console_ui.display_menu()
        choice = console_ui.get_menu_choice()

        if choice == 1:
            console_ui.prompt_add_task()
        elif choice == 2:
            console_ui.prompt_view_tasks()
        elif choice == 3:
            console_ui.prompt_update_task()
        elif choice == 4:
            console_ui.prompt_delete_task()
        elif choice == 5:
            console_ui.prompt_toggle_completion()
        elif choice == 6:
            break  # Exit loop


def main() -> None:
    """Main entry point for Todo Console App (T114)."""
    setup_signal_handlers()
    console_ui.display_welcome()
    run_main_loop()
    console_ui.display_goodbye()


if __name__ == "__main__":
    main()  # T115
