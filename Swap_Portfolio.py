"""Swap Portfolio:

1. Adding new positions/removing the old ones with its parameters: legs, notional, maturity date, payment frequency,
    accounting basis.
2. Changing notional of given position (trading: buy/sell trade)
3. Calculating accrued interest
4. Calculating next coupon payment date"""

from datetime import date


class FixedLeg:
    def __init__(self, notional: float, rate: float, currency: str,
                 payment_frequency: str, accounting_basis_month: str, accounting_basis_year: str):
        self.rate = rate
        self.currency = currency
        self.payment_frequency = payment_frequency
        self.accounting_basis_month = accounting_basis_month
        self.accounting_basis_year = accounting_basis_year
        self.notional = notional

    def accrued_interest(self, notional, rate):
        pass

    def __str__(self):
        return (
            f"Notional:{self.notional}, Rate: {self.rate}, "
            f"Currency: {self.payment_frequency.upper()}, "
            f"Accounting basis: {self.accounting_basis_year.upper()}/{self.accounting_basis_year.upper()}")


class FloatingLeg:
    def __init__(self, notional: float, rate: str, currency: str,
                 payment_frequency: str, accounting_basis_month: str, accounting_basis_year: str):
        self.rate = rate
        self.currency = currency
        self.payment_frequency = payment_frequency
        self.accounting_basis_month = accounting_basis_month
        self.accounting_basis_year = accounting_basis_year
        self.notional = notional

    def accrued_interest(self, notional, rate):
        pass

    def __str__(self):
        return (
            f"Notional:{self.notional}, Rate: {self.rate.upper()}, "
            f"Currency: {self.payment_frequency.upper()}, "
            f"Accounting basis: {self.accounting_basis_year.upper()}/{self.accounting_basis_year.upper()}")


class Swap:
    def __init__(self, swap_id: str, receivable_leg, payable_leg, maturity_date: date):
        self.swap_id = swap_id
        self.receivable_leg = receivable_leg
        self.payable_leg = payable_leg
        self.maturity_date = maturity_date #all dates to fix

    def __str__(self):
        return (
            f"Swap ID: {self.swap_id}, "
            f"Maturity date: {self.maturity_date}\n "
            f"Receivable leg:\n\t {self.receivable_leg}\n "
            f"Payable leg:\n\t {self.payable_leg} ")

    def trade(self, direction: str, amount):
        if direction.upper() == "BUY":
            self.receivable_leg.notional += amount
            self.payable_leg.notional += amount
            print(f"\nPosition has been increased successfully by {amount}")
        elif direction.upper() == "SELL":
            self.receivable_leg.notional -= amount
            self.payable_leg.notional -= amount
            if self.receivable_leg.notional <= 0 or self.payable_leg.notional <= 0:
                self.receivable_leg.notional = 0
                self.payable_leg.notional = 0
                print("\nPosition has been fully closed\n")
            else:
                print(f"\nPosition has been decreased successfully by {amount}")
        else:
            raise ValueError("Direction must be either BUY or SELL")


class Portfolio:
    def __init__(self):
        self.positions = []

    def add_swap(self, position):
        self.positions.append(position)
        print("Position added successfully.")

    def trade(self, swap_id, direction, amount):
        for position in self.positions:
            if position.swapi_id == swap_id:
                position.trade(direction, amount)
                return
        raise ValueError(f"{swap_id} not found")

    def __str__(self):
        print("\n**********PORTFOLIO**********\n")
        return "\n\n".join(str(position) for position in self.positions)


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


leg1_irs = FloatingLeg(1000000, "sofr", "usd", "12M",
                       "act", "365")
leg2_irs = FixedLeg(1000000, 0.01, "usd", "12M",
                    "30", "360")

swap1_irs = Swap(maturity_date="20-06-2026", payable_leg=leg1_irs, receivable_leg=leg2_irs,
                 swap_id="IRS001")

leg1_cds = FixedLeg(20000, 0, "EUR", "03M", "30",
                    "365")
leg2_cds = FixedLeg(20000, 0.05, "EUR", "03M",
                    "30", "ACT")

swap1_cds = Swap("CDS001", leg2_cds, leg1_cds, 20280920)

leg1_cys = FixedLeg(6000000, 0.025, "eur", "06M",
                    "act", "act")
leg2_cys = FloatingLeg(750000, "fedl", "usd", "12M",
                       "30", "360")

swap1_cys = Swap("CYS001", leg1_cys, leg2_cys, 20600415)

leg1_trs = FixedLeg(36, 0, "EUR", "06M",
                    "act", "360")
leg2_trs = FixedLeg(700000, 0.05, "EUR", "06M",
                    "30", "360")
swap1_trs = Swap("TRS001", leg2_trs, leg1_trs, 20260810)

portfolio = Portfolio()
portfolio.add_swap(swap1_irs)
portfolio.add_swap(swap1_cds)
portfolio.add_swap(swap1_cys)
portfolio.add_swap(swap1_trs)

print(portfolio)

swap1_irs.trade("BUY", 150000)
swap1_cds.trade("Buy", 10000)
swap1_cds.trade("sell", 30000)

print(portfolio)
