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
