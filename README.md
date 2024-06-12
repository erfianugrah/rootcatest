# OpenSSL Certificate Generation Tool

This tool automates the process of generating a Root Certificate Authority (CA) and a Leaf certificate using OpenSSL, with the ability to customize distinguished name (DN) values such as domain, country, state, locality, organization, and organizational unit. It also outputs the certificates in base64-encoded DER format.

## Prerequisites

- Python 3.x installed on your system.
- OpenSSL command-line tool installed.

## Installation

No installation is required. You just need to have Python and OpenSSL installed on your system.

## Usage

To use this tool, run the script from the command line and provide the necessary arguments:

```bash
python generate_certs.py --domain example.com --country US --state California --locality San Francisco --organization MyOrg --organizational_unit MyUnit --days 3650
```

### Arguments

- `--domain`: The domain name for the leaf certificate. **Required**.
- `--country`: Country Name. Default is 'SG'.
- `--state`: State or Province Name. Default is 'Singapore'.
- `--locality`: Locality Name. Default is 'Singapore'.
- `--organization`: Organization Name. Default is 'Erfi Corp'.
- `--organizational_unit`: Organizational Unit Name. Default is 'Erfi Proxy'.
- `--days`: Validity period for the leaf certificate in days. Default is 3650.

## Output

Upon successful execution, the tool generates several files:

- A Root CA private key (`<subdomain>_rootCA.key`) and certificate (`<subdomain>_rootCA.pem`).
- A Leaf private key (`<subdomain>_leaf.key`) and certificate (`<subdomain>_leaf.pem`).
- A PKCS#12 file containing both the Leaf certificate and its private key (`<subdomain>_certs.p12`). The password for this file is hardcoded as `"yourPKCS12Password"` in the script.
- Base64-encoded DER versions of the Leaf (`<subdomain>_leaf_base64.txt`) and Root CA (`<subdomain>_rootCA_base64.txt`) certificates.

## Note

- Ensure that OpenSSL is correctly installed and accessible from your command line.
- The PKCS#12 password is set within the script. Change it according to your security requirements.
- This script does not handle cleanup of temporary files created during the certificate generation process. Manual deletion may be required if needed.
