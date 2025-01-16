# ANSI escape codes for more colors and styles
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

RESET = "\033[0m"  # Reset the color

# Example: Printing text with various colors
print(f"{BLACK}This is black text.{RESET}")
print(f"{RED}This is red text.{RESET}")
print(f"{GREEN}This is green text.{RESET}")
print(f"{YELLOW}This is yellow text.{RESET}")
print(f"{BLUE}This is blue text.{RESET}")
print(f"{MAGENTA}This is magenta text.{RESET}")
print(f"{CYAN}This is cyan text.{RESET}")
print(f"{WHITE}This is white text.{RESET}")

# Bright colors
print(f"{BRIGHT_BLACK}This is bright black text.{RESET}")
print(f"{BRIGHT_RED}This is bright red text.{RESET}")
print(f"{BRIGHT_GREEN}This is bright green text.{RESET}")
print(f"{BRIGHT_YELLOW}This is bright yellow text.{RESET}")
print(f"{BRIGHT_BLUE}This is bright blue text.{RESET}")
print(f"{BRIGHT_MAGENTA}This is bright magenta text.{RESET}")
print(f"{BRIGHT_CYAN}This is bright cyan text.{RESET}")
print(f"{BRIGHT_WHITE}This is bright white text.{RESET}")
