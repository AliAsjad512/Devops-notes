import subprocess
import argparse
import logging
import sys
import os
from pathlib import Path

class SSLRenewer:
    def __init__(self, certbot_path='certbot'):
        self.certbot = certbot_path
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def check_cert_expiry(self, domain):
        """Check certificate expiry using openssl"""
        try:
            result = subprocess.run(
                ['openssl', 's_client', '-servername', domain, '-connect', f'{domain}:443'],
                input='QUIT\n', text=True, capture_output=True, timeout=10
            )
            # Extract expiry from output (simplified)
            for line in result.stderr.split('\n'):
                if 'notAfter=' in line:
                    return line.split('notAfter=')[1]
            return None
        except Exception as e:
            self.logger.error(f"Failed to check cert for {domain}: {e}")
            return None
    def renew_cert(self, domain, email, webroot_path=None, test_mode=False):
        """Renew certificate using certbot"""
        cmd = [self.certbot, 'certonly']
        if webroot_path:
            cmd.extend(['--webroot', '-w', webroot_path])
        else:
            cmd.append('--standalone')
        cmd.extend(['-d', domain, '--email', email, '--non-interactive', '--agree-tos'])
        if test_mode:
            cmd.append('--test-cert')
        self.logger.info(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            self.logger.info(f"✅ Certificate renewed for {domain}")
            return True
        else:
            self.logger.error(f"Renewal failed: {result.stderr}")
            return False
    def deploy_cert(self, domain, cert_path, key_path, reload_cmd=None):
        """Deploy certificate to web server"""
        # Example: copy certs to nginx location
        target_cert = f"/etc/nginx/ssl/{domain}.crt"
        target_key = f"/etc/nginx/ssl/{domain}.key"
        subprocess.run(['cp', cert_path, target_cert], check=True)
        subprocess.run(['cp', key_path, target_key], check=True)
        if reload_cmd:
            subprocess.run(reload_cmd, shell=True, check=True)
        self.logger.info(f"✅ Deployed certificate to {target_cert}")
    if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SSL Certificate Renewer')
    parser.add_argument('--domain', required=True, help='Domain to renew')
    parser.add_argument('--email', required=True, help='Email for Let\'s Encrypt')
    parser.add_argument('--webroot', help='Webroot path for HTTP-01 challenge')
    parser.add_argument('--test', action='store_true', help='Use staging environment')
    parser.add_argument('--reload-cmd', help='Command to reload web server (e.g., "systemctl reload nginx")')
    args = parser.parse_args()

    renewer = SSLRenewer()
    success = renewer.renew_cert(args.domain, args.email, args.webroot, args.test)
    if success and args.reload_cmd:
        subprocess.run(args.reload_cmd, shell=True, check=True)
        print("✅ Web server reloaded")


