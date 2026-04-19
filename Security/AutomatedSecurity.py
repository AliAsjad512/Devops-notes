import boto3
import argparse
import ipaddress
from collections import defaultdict

class SecurityGroupAuditor:
    def __init__(self, region='us-east-1'):
        self.ec2 = boto3.client('ec2', region_name=region)
        self.region = region

    def get_all_security_groups(self):
        """Get all security groups in the region"""
        response = self.ec2.describe_security_groups()
        return response['SecurityGroups']

    def find_overly_permissive(self):
        """Find rules with 0.0.0.0/0 or ::/0"""
        sgs = self.get_all_security_groups()
        findings = []
        for sg in sgs:
            for rule in sg.get('IpPermissions', []):
                for ip_range in rule.get('IpRanges', []):
                    cidr = ip_range.get('CidrIp')
                    if cidr == '0.0.0.0/0':
                        findings.append({
                            'group_id': sg['GroupId'],
                            'group_name': sg['GroupName'],
                            'port': rule.get('FromPort'),
                            'protocol': rule.get('IpProtocol'),
                            'cidr': cidr,
                            'description': ip_range.get('Description', '')
                        })
                for ipv6_range in rule.get('Ipv6Ranges', []):
                    cidr = ipv6_range.get('CidrIpv6')
                    if cidr == '::/0':
                        findings.append({
                            'group_id': sg['GroupId'],
                            'group_name': sg['GroupName'],
                            'port': rule.get('FromPort'),
                            'protocol': rule.get('IpProtocol'),
                            'cidr': cidr,
                            'description': ipv6_range.get('Description', '')
                        })
        return findings