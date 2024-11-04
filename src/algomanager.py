from strategy import AlgorithmStrategy
class AlgorithmManager:

    def setStrategy(self, strategy: AlgorithmStrategy):
        self.strategy = strategy

    def solve(self, magic_cube, **kwargs):
        return self.strategy.execute(magic_cube, **kwargs)

