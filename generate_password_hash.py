import getpass

import bcrypt


def main() -> None:
    password = getpass.getpass("Password: ")
    confirmation = getpass.getpass("Confirm password: ")

    if not password:
        raise SystemExit("Password cannot be empty.")
    if password != confirmation:
        raise SystemExit("Passwords do not match.")

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(rounds=12),
    ).decode("utf-8")

    print("\nSet this as APP_PASSWORD_HASH in your hosting environment:")
    print(password_hash)


if __name__ == "__main__":
    main()
