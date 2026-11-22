
def mask_card_number(number):
    """
    Masks a card number, showing only the last four characters.
    Handles invalid inputs safely.
    """
    if not isinstance(number, str):
        return "Invalid card number"

    digits = number.replace(' ', '').replace('-', '')

    if len(digits) < 4:
        return "Invalid card number"

    return '*' * 12 + digits[-4:]


def parse_transaction(line):
    """
    Parses date,category,amount safely.
    Returns ('unknown', 0) for invalid input.
    """
    if not isinstance(line, str):
        return ("unknown", 0)

    parts = line.split(',')

    if len(parts) != 3:
        return ("unknown", 0)

    category = parts[1].strip()
    amount = parts[2].strip()

    if not category or not amount:
        return ("unknown", 0)

    try:
        return category.lower(), int(amount)
    except ValueError:
        return ("unknown", 0)


def parse_statement_total(text):
    """
    Extracts the statement total safely.
    Returns 0 for invalid input.
    """
    if not isinstance(text, str) or ':' not in text:
        return 0

    amount = text.split(':', 1)[1].strip()
    amount = amount.replace(',', '')

    try:
        return int(amount)
    except ValueError:
        return 0


def main():
    print("==== Running mask_card_number ====")
    value = input("Enter a card number (e.g. 4111 1111 1111 1234): ")
    print("Masked card number:", mask_card_number(value))

    print("\n==== Running parse_transaction ====")
    value = input("Enter a transaction as DATE,CATEGORY,AMOUNT (e.g. 2026-11-05,dining,1550): ")
    print("Category and amount:", parse_transaction(value))

    print("\n==== Running parse_statement_total ====")
    value = input("Enter the statement total line (e.g. Total: 12,500): ")
    print("Statement total:", parse_statement_total(value))


if __name__ == "__main__":
    main()
