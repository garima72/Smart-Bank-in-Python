
from datetime import datetime
from pathlib import Path


class SmartBank:
    """Mini banking system with proper file-based storage."""

    def __init__(self, username: str):
        self.username = username

        # ==========================
        # FIX: Always create data folder
        # ==========================
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)

        # User-specific files
        self.balance_file = self.data_dir / f"{username}_balance.txt"
        self.pin_file = self.data_dir / f"{username}_pin.txt"
        self.history_file = self.data_dir / f"{username}_history.txt"

        self.balance = 0.0
        self.pin = "1234"

        self._load_data()

    # ==========================
    # LOAD DATA SAFELY
    # ==========================
    def _load_data(self):
        # ---- Balance ----
        if self.balance_file.exists():
            try:
                data = self.balance_file.read_text().strip()
                self.balance = float(data) if data else 0.0
            except ValueError:
                self.balance = 0.0
        else:
            self.save_balance()

        # ---- PIN ----
        if self.pin_file.exists():
            data = self.pin_file.read_text().strip()
            self.pin = data if data else "1234"
        else:
            self.save_pin()

    # ==========================
    # SAVE FUNCTIONS
    # ==========================
    def save_balance(self):
        self.balance_file.write_text(str(self.balance))

    def save_pin(self):
        self.pin_file.write_text(self.pin)

    def add_history(self, entry: str):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(f"[{time}] {entry}\n")

    # ==========================
    # AUTH SYSTEM
    # ==========================
    def verify_pin(self):
        for i in range(3):
            pin = input("Enter PIN: ").strip()
            if pin == self.pin:
                return True
            print(f"❌ Wrong PIN ({i+1}/3)")
        return False

    # ==========================
    # INPUT HANDLER
    # ==========================
    def get_amount(self):
        while True:
            try:
                amt = float(input("Enter amount: ").strip())
                if amt <= 0:
                    print("❌ Amount must be greater than 0")
                    continue
                return amt
            except ValueError:
                print("❌ Invalid input! Enter a number (e.g. 500)")

    # ==========================
    # BANK FEATURES
    # ==========================
    def check_balance(self):
        print(f"\n💰 Balance: ₹{self.balance:.2f}\n")

    def deposit(self):
        amt = self.get_amount()
        self.balance += amt
        self.save_balance()
        self.add_history(f"Deposited + ₹{amt:.2f}")
        print(f"✅ Deposited! Balance: ₹{self.balance:.2f}")

    def withdraw(self):
        amt = self.get_amount()

        if amt > self.balance:
            print("❌ Insufficient balance")
            return

        self.balance -= amt
        self.save_balance()
        self.add_history(f"Withdrawn - ₹{amt:.2f}")
        print(f"✅ Withdraw successful! Balance: ₹{self.balance:.2f}")

    def show_history(self):
        print("\n📜 Transaction History\n")

        if not self.history_file.exists():
            print("No history found.")
            return

        lines = self.history_file.read_text().splitlines()

        if not lines:
            print("No transactions yet.")
            return

        for i, line in enumerate(lines, 1):
            print(f"{i}. {line}")

    def change_pin(self):
        current = input("Enter current PIN: ").strip()

        if current != self.pin:
            print("❌ Wrong PIN")
            return

        new_pin = input("Enter new PIN: ").strip()
        confirm = input("Confirm PIN: ").strip()

        if new_pin != confirm:
            print("❌ PIN mismatch")
            return

        if not new_pin.isdigit() or len(new_pin) != 4:
            print("❌ PIN must be 4 digits")
            return

        self.pin = new_pin
        self.save_pin()
        print("✅ PIN updated successfully!")

    def add_interest(self):
        try:
            rate = float(input("Enter interest rate (%): ").strip())

            if rate <= 0:
                print("❌ Invalid rate")
                return

            interest = self.balance * rate / 100
            self.balance += interest

            self.save_balance()
            self.add_history(f"Interest + ₹{interest:.2f} ({rate}%)")

            print(f"💹 Interest added: ₹{interest:.2f}")
            print(f"New Balance: ₹{self.balance:.2f}")

        except ValueError:
            print("❌ Invalid input")


# ==========================
# MAIN PROGRAM
# ==========================
def main():
    users = ["user1", "user2", "user3"]

    print("\n🏦 SMARTBANK SYSTEM")
    print("====================")

    print("\nAvailable Users:")
    for u in users:
        print("•", u)

    username = input("\nEnter username: ").strip()

    if username not in users:
        print("❌ User not found")
        return

    bank = SmartBank(username)

    print("\n🔐 Login Required")
    if not bank.verify_pin():
        print("🚫 Too many attempts")
        return

    print(f"\n✅ Welcome {username}!")

    while True:
        print("\n====================")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transaction History")
        print("5. Change PIN")
        print("6. Add Interest")
        print("7. Exit")
        print("====================")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            bank.check_balance()
        elif choice == "2":
            bank.deposit()
        elif choice == "3":
            bank.withdraw()
        elif choice == "4":
            bank.show_history()
        elif choice == "5":
            bank.change_pin()
        elif choice == "6":
            bank.add_interest()
        elif choice == "7":
            print("👋 Thanks for using SmartBank!")
            break
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()

       