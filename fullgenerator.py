import argparse
import subprocess
import tempfile
import os
import base64

def generate_openssl_cnf(domain, country, state, locality, organization, organizational_unit):
    return f"""
[ req ]
default_bits = 4096
prompt = no
default_md = sha256
distinguished_name = dn

[ dn ]
C = {country}
ST = {state}
L = {locality}
O = {organization}
OU = {organizational_unit}
CN = {domain}

[ v3_req ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = {domain}

[ v3_ca ]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer:always
basicConstraints = critical,CA:true
keyUsage = critical,keyCertSign,cRLSign
"""

def generate_v3_ext(domain):
    return f"""
authorityKeyIdentifier=keyid,issuer:always
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = {domain}
"""

def convert_pem_to_der_and_base64_encode(pem_file_path, der_file_path):
    subprocess.run(['openssl', 'x509', '-outform', 'der', '-in', pem_file_path, '-out', der_file_path], check=True)
    with open(der_file_path, 'rb') as der_file:
        der_data = der_file.read()
    base64_data = base64.b64encode(der_data).decode('utf-8')
    return base64_data

def write_base64_to_file(base64_data, output_path):
    with open(output_path, 'w') as file:
        file.write(base64_data)
    print(f"Base64-encoded DER content written to {output_path}:\n{base64_data}\n")

def main(domain, country, state, locality, organization, organizational_unit, days):
    # Extract the subdomain from the full domain name
    subdomain = domain.split('.')[0]

    root_key = f'{subdomain}_rootCA.key'
    root_cert = f'{subdomain}_rootCA.pem'
    leaf_key = f'{subdomain}_leaf.key'
    leaf_cert = f'{subdomain}_leaf.pem'
    
    openssl_cnf_content = generate_openssl_cnf(domain, country, state, locality, organization, organizational_unit)
    v3_ext_content = generate_v3_ext(domain)

    with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmpfile:
        tmpfile.write(openssl_cnf_content)
        openssl_cnf_path = tmpfile.name

    with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmpfile:
        tmpfile.write(v3_ext_content)
        v3_ext_path = tmpfile.name

    try:
        subprocess.call(['openssl', 'genrsa', '-out', root_key, '4096'])
        subprocess.call(['openssl', 'req', '-x509', '-new', '-nodes', '-key', root_key, '-sha256', '-days', '1024', '-out', root_cert, '-config', openssl_cnf_path, '-extensions', 'v3_ca'])
        subprocess.call(['openssl', 'genrsa', '-out', leaf_key, '4096'])
        subprocess.call(['openssl', 'req', '-new', '-key', leaf_key, '-out', f'{subdomain}_leaf.csr', '-config', openssl_cnf_path])
        subprocess.call(['openssl', 'x509', '-req', '-in', f'{subdomain}_leaf.csr', '-CA', root_cert, '-CAkey', root_key, '-CAcreateserial', '-out', leaf_cert, '-days', str(days), '-sha256', '-extfile', v3_ext_path])

        leaf_der_path = leaf_cert.replace('.pem', '.der')
        root_der_path = root_cert.replace('.pem', '.der')

        leaf_base64 = convert_pem_to_der_and_base64_encode(leaf_cert, leaf_der_path)
        root_base64 = convert_pem_to_der_and_base64_encode(root_cert, root_der_path)

        leaf_base64_file = f'{subdomain}_leaf_base64.txt'
        root_base64_file = f'{subdomain}_rootCA_base64.txt'

        write_base64_to_file(leaf_base64, leaf_base64_file)
        write_base64_to_file(root_base64, root_base64_file)

        print(f"Leaf Certificate Base64 DER written to {leaf_base64_file}")
        print(f"Root CA Certificate Base64 DER written to {root_base64_file}")
    finally:
        os.remove(openssl_cnf_path)
        os.remove(v3_ext_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Root CA and Leaf certificates with dynamic DN values and output base64 DER.')
    parser.add_argument('--domain', required=True, help='The domain name for the leaf certificate.')
    parser.add_argument('--country', default='SG', help='Country Name')
    parser.add_argument('--state', default='Singapore', help='State or Province Name')
    parser.add_argument('--locality', default='Singapore', help='Locality Name')
    parser.add_argument('--organization', default='Erfi Corp', help='Organization Name')
    parser.add_argument('--organizational_unit', default='Erfi Proxy', help='Organizational Unit Name')
    parser.add_argument('--days', type=int, default=3650, help='Validity period for the leaf certificate.')
    args = parser.parse_args()

    main(args.domain, args.country, args.state, args.locality, args.organization, args.organizational_unit, args.days)
