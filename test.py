import unittest
import main
from parameterized import parameterized


class TestWFF(unittest.TestCase):

    @parameterized.expand([
        ['(p3 ∨ ¬p212)', True],
        ['((p3 ∧ p8) → p212) ∨ p145', False],
        ['(((p3 ∧ p8) → p212) ∨ p145)', True],
        ['¬(p → p212)', False],
        ['((p8 ∨ (p212 → p3)) → p145)', True],
        ['(((p8 ∨ (p212 → p3)) → p145) ∧ (((p3 ∧ p8) → p212) ∨ p145))', True],
        ['(p212 ⊃ p8)', False],
        ['(p8 ∧ p3)', True],
        ['((p8 ∧ p8))', False],
        ['¬¬¬¬¬𝛼', False],
        ['¬¬¬¬¬p3', True],
        ['(p8 ∧ (p8 ∧ (p8 ∧ p8)))', True],
        ['(p212)', False],
        ['((p3 ∨ p212) ← ¬p145)', False],
        ['(p8 ∧ p7)', False],
        ['(𝛼 → 𝛽)', False]

    ])
    def test_wff(self, input: str, expected: bool):
        wff_validator = main.WffValidator()
        self.assertEqual(wff_validator.validate((input)), expected)


if __name__ == '__main__':
    test = TestWFF()
    test.run()
