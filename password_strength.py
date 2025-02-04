import re

def check_password_strength(password):
    """
    Check the strength of the given password based on length, 
    uppercase, lowercase, numeric, and special characters.

    :param password: The password to check.
    :return: A message indicating whether the password is strong or weak.
    """
    strength = {
        "length": len(password) >= 8,
        "uppercase": any(c.isupper() for c in password),
        "lowercase": any(c.islower() for c in password),
        "number": any(c.isdigit() for c in password),
        "special": any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for c in password)
    }

    # If password length is greater than 12, check all strength criteria
    if len(password) > 12:
        print("Your password is long, but it still doesn't contain the following required elements:")
        if not strength["uppercase"]:
            print("- uppercase letter")
        if not strength["lowercase"]:
            print("- lowercase letter")
        if not strength["number"]:
            print("- number")
        if not strength["special"]:
            print("- special character")

    print("\nPassword Strength Check:")
    print(f"✔ Minimum 8 characters: {'✔' if strength['length'] else '❌'}")
    print(f"✔ Contains uppercase letter: {'✔' if strength['uppercase'] else '❌'}")
    print(f"✔ Contains lowercase letter: {'✔' if strength['lowercase'] else '❌'}")
    print(f"✔ Contains number: {'✔' if strength['number'] else '❌'}")
    print(f"✔ Contains special character: {'✔' if strength['special'] else '❌'}")

    # Final strength evaluation
    if all(strength.values()):
        return "Your password is STRONG."
    else:
        return "Your password is WEAK. Please improve your password security."

