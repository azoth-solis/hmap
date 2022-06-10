import ipaddress

def extract_addresses(login_attempts):
    addresses = [] 
    for login_attempt in login_attempts: 
        try:
            address = login_attempt.split('from ')[1].split(' port')[0]
            if type(ipaddress.ip_address(address)) == ipaddress.IPv4Address:
                addresses.append(address)
        except Exception as oops:
            with open('oops.txt', 'a') as f:
                f.writelines(str(oops) + '\n')
    return [address for address in set(addresses)]

def extract_usernames(addresses, login_attempts):
    mappings = []
    for address in addresses:
        usernames = []
        for login_attempt in login_attempts:
            try:
                if address in login_attempt:
                    username = login_attempt.split('invalid user ')[1].split()[0]
                    if username.isalpha() and not username == 'Failed':
                        usernames.append(username)
            except Exception as oops:
                with open('oops.txt', 'a') as f:
                    f.writelines(str(oops) + '\n')
        usernames = [username for username in set(usernames)]
        mappings.append({address: usernames})
    return mappings

with open('failed_password_attempts.txt', 'r') as f:
    login_attempts = f.read().split(',')

addresses = extract_addresses(login_attempts)
mappings = extract_usernames(addresses, login_attempts)

with open('address_to_username_mappings.txt', 'w') as f:
    for mapping in mappings:
        f.writelines(str(mapping) + '\n')
