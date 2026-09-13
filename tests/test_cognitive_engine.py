import unittest
from cognitive_engine import CognitiveEngine

class TestCognitiveEngine(unittest.TestCase):
    def setUp(self):
        self.engine = CognitiveEngine()

    def test_phd_breakdown(self):
        result = self.engine.breakdown_concept_phd_level('Quantum Computing')
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(result['layers']), 4)

    def test_mental_block_elimination(self):
        result = self.engine.eliminate_mental_block('Imposter Syndrome in Coding')
        self.assertEqual(result['status'], 'success')
        self.assertIn('Re-framed', result['resolution'])

    def test_skill_mastery(self):
        result = self.engine.build_skill_mastery_path('Machine Learning')
        self.assertEqual(result['status'], 'success')
        self.assertEqual(self.engine.learning_states['Machine Learning'], 'Initiated')

if __name__ == '__main__':
    unittest.main()
