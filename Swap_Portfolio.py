"""Swap Portfolio:

1. Adding new positions/removing the old ones with its parameters: legs, notional, maturity date, payment frequency,
    accounting basis.
2. Changing notional of given position (trading: buy/sell trade)
3. Calculating accrued interest
4. Calculating next coupon payment date"""


class Leg:
    def __init__(self, rate_type: str, rate, currency: str,
                 payment_frequency: str, accounting_basis: str):
        self.rate_type = rate_type
        self.rate = rate
        self.currency = currency
        self.payment_frequency = payment_frequency
        self.accounting_basis = accounting_basis

    def __str__(self):
        return (f"Rate type: {self.rate_type}, Rate: {self.rate}, Currency: {self.payment_frequency}, "
                f"Accounting basis: {self.accounting_basis} ")


class Swap:
    def __init__(self, swap_id: str, notional: float, receivable_leg, payable_leg, maturity_date):
        self.swap_id = swap_id
        self.receivable_leg = receivable_leg
        self.payable_leg = payable_leg
        self.maturity_date = maturity_date
        self.notional = notional
        self.active = True

    def __str__(self):
        return (
            f"Swap ID: {self.swap_id}, Notional:{self.notional}, Maturity date: {self.maturity_date}, "
            f"Active:{self.active}\n"
            f"Receivable leg:\n\t {self.receivable_leg}\n "
            f"Payable leg:\n\t {self.payable_leg} ")

    def buy(self, amount):
        print("\nNotional has been increased successfully\n")
        self.notional += amount

    def sell(self, amount):
        self.notional -= amount
        if self.notional >0:
            print(f"\nNotional has been decreased successfully\n")
        else:
            self.active = False
            print(f"\nPosition has been fully closed\n")



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


leg1_irs = Leg(rate_type="fixed", rate=0.01, currency="USD",
               payment_frequency="03M", accounting_basis="ACT/360")
leg2_irs = Leg(rate_type="floating", rate="SOFR", currency="USD",
               payment_frequency="03M", accounting_basis="ACT/360")
swap1_irs = Swap(maturity_date=20270620, notional=100000, payable_leg=leg1_irs, receivable_leg=leg2_irs,
                 swap_id="IRS001")

leg1_cds = Leg("Event", 0, "EUR", "03M", "30/365")
leg2_cds = Leg("Fixed", 0.05, "EUR", "03M", "30/365")

swap1_cds = Swap("CDS001", 20000, leg2_cds, leg1_cds, 20280920)

portfolio = Portfolio()
portfolio.add_swap(swap1_irs)
portfolio.add_swap(swap1_cds)

print(portfolio)

swap1_cds.sell(20000)
print(portfolio)

swap1_irs.buy(50000)
print(portfolio)
