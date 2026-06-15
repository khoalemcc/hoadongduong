# scripts/reset_passwords.py
"""
Reset the password for the default admin user and (optionally) for any
customer account.

Usage (from the project root):
    python scripts/reset_passwords.py
"""

import os
from getpass import getpass

from app.database import SessionLocal
from app.models import User, Role
from app.auth import get_password_hash


def reset_user_password(
    db,
    email: str,
    new_password: str,
    ensure_admin: bool = False,
) -> None:
    """
    Update the password for the user identified by ``email``.
    If ``ensure_admin`` is True, the user will also be granted the
    ``admin`` role (creates the role if it does not exist).
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError(f"❌ No user found with email: {email}")

    # Update password hash
    user.password_hash = get_password_hash(new_password)

    if ensure_admin:
        # Make sure the ``admin`` role exists
        admin_role = (
            db.query(Role).filter(Role.name.ilike("admin")).first()
        )
        if not admin_role:
            admin_role = Role(name="admin", description="Administrator")
            db.add(admin_role)
            db.flush()  # assign an ID before using it

        # Add the role to the user if not already present
        if admin_role not in user.roles:
            user.roles.append(admin_role)

    db.commit()
    db.refresh(user)
    print(f"Password for {email!r} has been reset.")


def main() -> None:
    # ----------------------------------------------------------------------
    # 1️⃣  Admin account ----------------------------------------------------
    # ----------------------------------------------------------------------
    # You can set these via environment variables or edit them directly
    admin_email = os.getenv("DEFAULT_ADMIN_EMAIL", "lephananhkhoa@gmail.com")
    admin_pwd = os.getenv("DEFAULT_ADMIN_PASSWORD")
    if not admin_pwd:
        print(
            f"Enter a new password for the admin ({admin_email}) "
            "(input will be hidden):"
        )
        admin_pwd = getpass()

    # ----------------------------------------------------------------------
    # 2️⃣  Customer account -------------------------------------------------
    # ----------------------------------------------------------------------
    # Change the values below if you want to reset a specific customer.
    # Leave ``customer_email`` empty to skip resetting a customer.
    customer_email = os.getenv("DEFAULT_CUSTOMER_EMAIL", "")
    customer_pwd = os.getenv("DEFAULT_CUSTOMER_PASSWORD", "")

    if not customer_email:
        # Ask the user if they want to reset a customer account
        resp = input(
            "Do you want to reset a customer password? (y/N): "
        ).strip().lower()
        if resp == "y":
            customer_email = input("Customer e‑mail: ").strip()
            if customer_email:
                customer_pwd = getpass(
                    f"New password for {customer_email}: "
                )

    # ----------------------------------------------------------------------
    # 3️⃣  Perform the updates -----------------------------------------------
    # ----------------------------------------------------------------------
    db = SessionLocal()
    try:
        # Reset admin (always performed)
        reset_user_password(
            db,
            email=admin_email,
            new_password=admin_pwd,
            ensure_admin=True,
        )

        # Reset customer (optional)
        if customer_email:
            reset_user_password(
                db,
                email=customer_email,
                new_password=customer_pwd,
                ensure_admin=False,
            )
    finally:
        db.close()


if __name__ == "__main__":
    main()

{
  "action": "replace_file_content",
  "action_args": {
    "TargetFile": "d:/github/hoadongduong/backend2/reset_passwords.py",
    "StartLine": 116,
    "EndLine": 125,
    "TargetContent": "{\n  \"action\": \"ask_permission\",\n  \"action_args\": {\n    \"Action\": \"command\",\n    \"Target\": \"python\",\n    \"Reason\": \"Run password‑reset script with env vars\",\n    \"toolAction\": \"Running command\",\n    \"toolSummary\": \"Password reset\"\n  }\n}",
    "ReplacementContent": "",
    "AllowMultiple": false,
    "Description": "Remove stray JSON block that caused a syntax error",
    "Instruction": "Delete lines 116‑125"
  },
  "toolAction": "Editing file",
  "toolSummary": "File cleanup"
}
{
  "action": "ask_permission",
  "action_args": {
    "Action": "command",
    "Target": "python",
    "Reason": "Set admin account (lephananhkhoa@gmail.com / 1234) via reset_passwords.py",
    "toolAction": "Running command",
    "toolSummary": "Password reset"
  }
}
