import subprocess

# Generate Root CA key
subprocess.call(['openssl', 'genrsa', '-out', 'rootCA.key', '4096'])

# Generate Root CA certificate with CA extensions
subprocess.call(['openssl', 'req', '-x509', '-new', '-nodes', '-key', 'rootCA.key', '-sha256', '-days', '1024', '-out', 'rootCA.pem', '-config', 'openssl.cnf', '-extensions', 'v3_ca'])

# Generate leaf key
subprocess.call(['openssl', 'genrsa', '-out', 'leaf.key', '4096'])

# Generate leaf certificate request
subprocess.call(['openssl', 'req', '-new', '-key', 'leaf.key', '-out', 'leaf.csr', '-config', 'openssl.cnf'])

# Generate leaf certificate signed with root CA certificate
subprocess.call(['openssl', 'x509', '-req', '-in', 'leaf.csr', '-CA', 'rootCA.pem', '-CAkey', 'rootCA.key', '-CAcreateserial', '-out', 'leaf.pem', '-days', '3650', '-sha256', '-extfile', 'v3.ext'])
