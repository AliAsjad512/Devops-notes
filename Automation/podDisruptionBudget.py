# K8s PDB Calculator - Suggest PodDisruptionBudget values based on replicas
import argparse

class PDBCalculator:
      @staticmethod
    def suggest_pdb(replicas, min_available_percent=50, max_unavailable_percent=25):
        """Suggest PDB values"""
        min_available = max(1, int(replicas * min_available_percent / 100))
        max_unavailable = max(1, int(replicas * max_unavailable_percent / 100))
        if min_available + max_unavailable > replicas:
            # Adjust to avoid conflict
            min_available = replicas - max_unavailable
        return {
            'min_available': min_available,
            'max_unavailable': max_unavailable,
            'recommendation': f"apiVersion: policy/v1\nkind: PodDisruptionBudget\nmetadata:\n  name: app\nspec:\n  minAvailable: {min_available}\n  # OR\n  # maxUnavailable: {max_unavailable}"
        }
 
    def from_deployment_yaml(yaml_file):
        import yaml
        with open(yaml_file, 'r') as f:
            deploy = yaml.safe_load(f)
        replicas = deploy.get('spec', {}).get('replicas', 1)
        return PDBCalculator.suggest_pdb(replicas)

   if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='K8s PDB Calculator')
    parser.add_argument('--replicas', type=int, help='Number of replicas')
    parser.add_argument('--deployment', help='Deployment YAML file')
    parser.add_argument('--min-percent', type=int, default=50)
    parser.add_argument('--max-percent', type=int, default=25)
    args = parser.parse_args()

    if args.deployment:
        pdb = PDBCalculator.from_deployment_yaml(args.deployment)
    elif args.replicas:
        pdb = PDBCalculator.suggest_pdb(args.replicas, args.min_percent, args.max_percent)
    else:
        print("❌ Provide --replicas or --deployment")
        exit(1)

    print(pdb['recommendation'])
