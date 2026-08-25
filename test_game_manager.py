import unittest

from game_manager import calc_profit, judge_profit


class TestGameManager(unittest.TestCase):

    def test_calc_profit(self):
        result = calc_profit(
            price=11000,
            cost=7000,
            parts=500,
            shipping=410,
            fee=1000
        )

        self.assertEqual(result, 2090)

    def test_judge_profit_enough(self):
        result = judge_profit(3000)

        self.assertEqual(result, "利益十分")

    def test_judge_profit_positive(self):
        result = judge_profit(2999)

        self.assertEqual(result, "利益あり")

    def test_judge_profit_positive_lower_boundary(self):
        result = judge_profit(1)
        self.assertEqual(result, "利益あり")

    def test_judge_profit_zero(self):
        result = judge_profit(0)

        self.assertEqual(result, "収支ゼロ")

    def test_judge_profit_loss(self):
        result = judge_profit(-1)
        self.assertEqual(result, "赤字")


if __name__ == "__main__":
    unittest.main()