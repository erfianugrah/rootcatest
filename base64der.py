import base64
import subprocess

# Prompt the user for the paths to the PEM and DER files
pem_file_path = input('Enter the path to the PEM file: ')
der_file_path = input('Enter the path to the DER file: ')

# Run the OpenSSL command to convert the PEM file to DER format
subprocess.run(['openssl', 'x509', '-outform', 'der', '-in', pem_file_path, '-out', der_file_path], check=True)

# Read the DER file
with open(der_file_path, 'rb') as der_file:
    der_data = der_file.read()

# Encode the DER data in base64
base64_data = base64.b64encode(der_data).decode('utf-8')

print(base64_data)
