from ldap3 import Server, Connection, ALL, NTLM


def authenticate(username, password):
    # LDAP server configuration
    username = username.split("@")[0]  # Extract username without domain
    domain_name = "unionbankcameroon.com"
    ldap_server_address = (
        "unionbankcameroon.com"  # Replace with your LDAP server address
    )

    # Base DN for your Active Directory domain
    base_dn = "dc=unionbankcameroon,dc=com"
    # User principal name format
    user_dn = f"{username}@{domain_name}"

    try:
        # Create server instance
        server = Server(ldap_server_address, get_info=ALL)

        # Attempt to bind with user credentials using NTLM (for Active Directory)
        conn = Connection(server, user=user_dn, password=password, authentication=NTLM)

        if not conn.bind():
            print("Invalid credentials")
            return False

        print("Authentication successful")

        # Optionally, search for user attributes
        search_filter = f"(sAMAccountName={username})"
        conn.search(base_dn, search_filter, attributes=["displayName", "mail"])

        if conn.entries:
            print("User details:", conn.entries[0])

        conn.unbind()
        return True

    except Exception as e:
        print("Error:", str(e))
        return False


# Example usage
if __name__ == "__main__":
    authenticate("dev.ubc", "SuperSecretPassword123")
