import cs50


def main():
    # Prompt user for number of card until we get non-negative integer.
    while True:
        print("Number: ", end="")
        card_number = cs50.get_int()
        if card_number >= 0:
            break
    if check_card_number(card_number):
        print(check_card_provider(card_number))
    else:
        print("INVALID")
    exit(0)

def check_card_number(card_number):
    sum_of_digits = 0
    # Reverse card number for easier identification of second-to-last digit.
    reversed_card_number = ''.join(reversed(str(card_number)))
    for i in range(len(reversed_card_number)):
        # Multiply every other digit.
        if i % 2 != 0:
            multiplied = int(reversed_card_number[i]) * 2
            # Sum up digits together.
            for digit in str(multiplied):
                sum_of_digits += int(digit)
        else:
            sum_of_digits += int(reversed_card_number[i])
    # Check if the total modulo 10 is congruent to 0.
    return sum_of_digits % 10 == 0


def check_card_provider(card_number):
    card_number = str(card_number)
    # Check if card number is valid American Express card.
    if (len(card_number) == 15 and
            (int(card_number[:2]) == 34 or int(card_number[:2]) == 37)):
        return "AMEX"
    # Check if card number is valid Master Card card.
    elif len(card_number) == 16 and int(card_number[:2]) in range(51, 56):
        return "MASTERCARD"
    # Check if card number is valid Visa card.
    elif (int(card_number[0]) == 4 and
            (len(card_number) == 13 or len(card_number) == 16)):
        return "VISA"
    else:
        return "INVALID"


if __name__ == "__main__":
    main()
