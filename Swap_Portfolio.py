"""Swap Portfolio:

1. Adding new positions/removing the old ones with its parameters: legs, notional, maturity date, payment frequency,
    accounting basis.
2. Changing notional of given position (trading: buy/sell trade)
3. Calculating accrued interest
4. Calculating next coupon payment date"""


class Leg:
    def __init__(self, notional: float, rate_type: str, rate, currency: str,
                 payment_frequency: str, accounting_basis: str):
        self.rate_type = rate_type
        self.rate = rate
        self.currency = currency
        self.payment_frequency = payment_frequency
        self.accounting_basis = accounting_basis
        self.notional = notional
        self.active = True

    def __str__(self):
        return (
            f"Notional:{self.notional},Rate type: {self.rate_type}, Rate: {self.rate}, "
            f"Currency: {self.payment_frequency}, "
            f"Accounting basis: {self.accounting_basis}, Active:{self.active}\n")

    def buy(self, amount):
        self.notional += amount
        return f"\nNotional has been increased successfully by {amount}" #to fix

    def sell(self, amount):
        self.notional -= amount
        if self.notional > 0:
            return f"\nNotional has been decreased successfully by {amount}\n" #to fix
        else:
            self.notional = 0
            self.active = False
            print(f"\nPosition has been fully closed\n")


class Swap:
    def __init__(self, swap_id: str, receivable_leg, payable_leg, maturity_date):
        self.swap_id = swap_id
        self.receivable_leg = receivable_leg
        self.payable_leg = payable_leg
        self.maturity_date = maturity_date

    def __str__(self):
        return (
            f"Swap ID: {self.swap_id}, Maturity date: {self.maturity_date}\n "
            f"Receivable leg:\n\t {self.receivable_leg}\n "
            f"Payable leg:\n\t {self.payable_leg} ")


class Portfolio:
    def __init__(self):
        self.positions = []

    def add_swap(self, position):
        self.positions.append(position)
        print("Position added successfully.")

    def __str__(self):
        print("\n**********PORTFOLIO**********\n")
        return "\n\n".join(str(pos) for pos in self.positions)


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


class CrossCurrencySwap(Swap):
    def __init__(self, swap_id: str, leg_1: float, leg_2: str, maturity_date, receivable_leg,
                 payable_leg):
        super().__init__(swap_id, receivable_leg, payable_leg, maturity_date)
        self.swap_id = swap_id
        self.leg_1 = leg_1
        self.leg_2 = leg_2
        self.maturity_date = maturity_date


class TotalReturnSwap(Swap):
    def __init__(self, swap_id: str, equity_leg: float, financing_leg: str, maturity_date, receivable_leg,
                 payable_leg):
        super().__init__(swap_id, receivable_leg, payable_leg, maturity_date)
        self.swap_id = swap_id
        self.equity_leg = equity_leg
        self.financing_leg = financing_leg
        self.maturity_date = maturity_date


leg1_irs = Leg(1000000, "floating", "sofr", "usd", "12M",
               "act/365")
leg2_irs = Leg(1000000, "fixed", 0.01, "usd", "12M",
               "30/360")
swap1_irs = Swap(maturity_date=20270620, payable_leg=leg1_irs, receivable_leg=leg2_irs,
                 swap_id="IRS001")

leg1_cds = Leg(20000, "Event", 0, "EUR", "03M", "30/365")
leg2_cds = Leg(20000, "Fixed", 0.05, "EUR", "03M",
               "30/365")

swap1_cds = Swap("CDS001", leg2_cds, leg1_cds, 20280920)

leg1_cys = Leg(6000000, "fixed", "0.025", "eur", "06M",
               "act/act")
leg2_cys = Leg(750000, "float", "fedl", "usd", "12M",
               "30/360")

swap1_cys = Swap("CYS001", leg1_cys, leg2_cys, 20600415)

leg1_trs = Leg(36, "equity", 0, "EUR", "06M", "act/365")
leg2_trs = Leg(700000, "Fixed", 0.05, "EUR", "06M",
               "30/365")
swap1_trs = Swap("TRS001", leg2_trs, leg1_trs, 20260810)


portfolio = Portfolio()
portfolio.add_swap(swap1_irs)
portfolio.add_swap(swap1_cds)
portfolio.add_swap(swap1_cys)
portfolio.add_swap(swap1_trs)

print(portfolio)

leg1_irs.sell(200)
leg2_irs.sell(200)

leg1_cys.buy(5200)
leg2_cys.buy(5200)

print(portfolio)
