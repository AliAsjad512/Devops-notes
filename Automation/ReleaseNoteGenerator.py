import subprocess
import argparse
import re
from datetime import datetime, timedelta
class ReleaseNotesGenerator:
    def __init__(self, repo_path='.'):
        self.repo_path = repo_path

    def get_commits_since(self, since_date):
        """Get commits after a given date"""
        cmd = ['git', '-C', self.repo_path, 'log', f'--since={since_date}', '--pretty=format:%s|%an|%ad']
        result = subprocess.run(cmd, capture_output=True, text=True)
        commits = []
        for line in result.stdout.split('\n'):
            if not line:
                continue
            parts = line.split('|')
            commits.append({
                'message': parts[0],
                'author': parts[1] if len(parts) > 1 else 'unknown',
                'date': parts[2] if len(parts) > 2 else ''
            })
        return commits
    def get_last_tag(self):
        """Get the most recent tag"""
        cmd = ['git', '-C', self.repo_path, 'describe', '--tags', '--abbrev=0']
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    def get_commits_between_tags(self, from_tag, to_tag='HEAD'):
        cmd = ['git', '-C', self.repo_path, 'log', f'{from_tag}..{to_tag}', '--pretty=format:%s']
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.split('\n') if result.stdout else []
    def categorize_commits(self, commits):
        categories = {
            'feat': [],
            'fix': [],
            'docs': [],
            'chore': [],
            'refactor': [],
            'test': [],
            'other': []
        }
        for commit in commits:
            msg = commit if isinstance(commit, str) else commit['message']
            matched = False
            for cat in categories:
                if msg.startswith(f'{cat}:'):
                    categories[cat].append(msg)
                    matched = True
                    break
            if not matched:
                categories['other'].append(msg)
        return categories
    def generate_markdown(self, version, commits_categorized, date=None):
        date_str = date or datetime.now().strftime('%Y-%m-%d')
        lines = [f"# Release {version} ({date_str})", ""]
        for cat, items in commits_categorized.items():
            if items:
                lines.append(f"## {cat.capitalize()}")
                for item in items:
                    lines.append(f"- {item}")
                lines.append("")
        return '\n'.join(lines)
    
    if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Release Notes Generator')
    parser.add_argument('--since', help='Date (YYYY-MM-DD) or "last-tag"')
    parser.add_argument('--output', help='Output file')
    parser.add_argument('--version', required=True, help='Release version')
    args = parser.parse_args()

    gen = ReleaseNotesGenerator()
    if args.since == 'last-tag':
        last_tag = gen.get_last_tag()
        if last_tag:
            commits = gen.get_commits_between_tags(last_tag)
        else:
            commits = gen.get_commits_since('1 month ago')
    elif args.since:
        commits = gen.get_commits_since(args.since)
    else:
        commits = gen.get_commits_since('1 week ago')

    categorized = gen.categorize_commits(commits if isinstance(commits[0], str) else [c['message'] for c in commits])
    notes = gen.generate_markdown(args.version, categorized)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(notes)
        print(f"✅ Release notes saved to {args.output}")
    else:
        print(notes)

