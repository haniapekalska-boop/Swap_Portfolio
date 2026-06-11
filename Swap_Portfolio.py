"""Portfolio swapowe:

1. Dodawanie nowych pozycji/usuwanie starych z ich parametrami: nogi, notional, maturity date payment frequency,
    accounting basis.
2. Zmiania notionali istniejących pozycji (trading: buy/sell trade)
3. Obliczanie zebranych odsetek dla każdej pozycji.
4. Obliczanie daty wypłaty następnego kuponu/resetu."""


class Leg:
    def __init__(self, direction: str, rate_type: str, rate, notional: float, currency: str,
                 payment_frequency: str, accounting_basis: str):
        self.direction = direction
        self.rate_type = rate_type
        self.rate = rate
        self.notional = notional
        self.currency = currency
        self.payment_frequency = payment_frequency
        self.accounting_basis = accounting_basis


class Swap:
    def __init__(self, swap_id: str, receivable_leg, payable_leg, maturity_date):
        self.swap_id = swap_id
        self.receivable_leg = receivable_leg
        self.payable_leg = payable_leg
        self.maturity_date = maturity_date


class Portfolio:
    def __init__(self):
        self.swaps = {}

    def add_swap(self, swap):
        self.swaps[swap.swap_id] = swap

    def __str__(self):
        result = "PORTFOLIO\n"
        for swap in self.swaps.values():
            result += str(swap) + "\n"
        return result


class InterestRateSwap(Swap):
    def __init__(self, swap_id: str, fixed_leg: float, floating_leg: str, maturity_date, receivable_leg, payable_leg):
        super().__init__(swap_id, receivable_leg, payable_leg, maturity_date)
        self.swap_id = swap_id
        self.fixed_leg = fixed_leg
        self.floating_leg = floating_leg
        self.maturity_date = maturity_date


class CreditDefaultSwap(Swap):
    def __init__(self, swap_id: str, premium_leg: float, protection_leg: str, maturity_date, receivable_leg,
                 payable_leg):
        super().__init__(swap_id, receivable_leg, payable_leg, maturity_date)
        self.swap_id = swap_id
        self.premium_leg = premium_leg
        self.protection_leg = protection_leg
        self.maturity_date = maturity_date


leg1_irs = Leg(direction="Pay", rate_type="fixed", rate=0.01, notional=100000, currency="USD",
               payment_frequency="03M", accounting_basis="ACT/360")
leg2_irs = Leg(direction="Rec", rate_type="floating", rate="FEDL", notional=100000, currency="USD",
               payment_frequency="03M", accounting_basis="ACT/360")
swap1_irs = Swap(maturity_date=20270620, payable_leg=leg1_irs, receivable_leg=leg2_irs, swap_id="IRS001")

print(Portfolio)
