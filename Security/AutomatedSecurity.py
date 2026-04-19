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
    

    def find_unused_security_groups(self):
        """Find security groups not attached to any ENI"""
        sgs = self.get_all_security_groups()
        # Get all attached groups
        attached = set()
        instances = self.ec2.describe_instances()
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                for sg in instance.get('SecurityGroups', []):
                    attached.add(sg['GroupId'])
        # Also check network interfaces
        nics = self.ec2.describe_network_interfaces()
        for nic in nics['NetworkInterfaces']:
            for sg in nic.get('Groups', []):
                attached.add(sg['GroupId'])
        unused = []
        for sg in sgs:
            if sg['GroupId'] not in attached and sg['GroupName'] != 'default':
                unused.append({
                    'group_id': sg['GroupId'],
                    'group_name': sg['GroupName'],
                    'vpc_id': sg['VpcId']
                })
        return unused

    def generate_report(self):
        """Generate full audit report"""
        report = {
            'region': self.region,
            'overly_permissive': self.find_overly_permissive(),
            'unused_security_groups': self.find_unused_security_groups()
        }
        return report
    
    if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Security Group Auditor')
    parser.add_argument('--region', default='us-east-1')
    parser.add_argument('--output', help='Output JSON file')
    args = parser.parse_args()

    auditor = SecurityGroupAuditor(args.region)
    report = auditor.generate_report()

    print(f"🔒 Security Group Audit - {args.region}")
    print("=" * 50)
    print(f"Overly permissive rules (0.0.0.0/0): {len(report['overly_permissive'])}")
    for r in report['overly_permissive']:
        print(f"  - {r['group_name']} ({r['group_id']}) : {r['protocol']} port {r['port']} from {r['cidr']}")
    print(f"Unused security groups: {len(report['unused_security_groups'])}")
    for sg in report['unused_security_groups']:
        print(f"  - {sg['group_name']} ({sg['group_id']}) in VPC {sg['vpc_id']}")

    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✅ Report saved to {args.output}")
