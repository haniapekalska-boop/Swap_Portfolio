"""Swap Portfolio:

1. Adding new positions/removing the old ones with its parameters: legs, notional, maturity date, payment frequency,
    accounting basis.
2. Changing notional of given position (trading: buy/sell trade)
3. Calculating accrued interest
4. Calculating next coupon payment date"""

import calendar
from datetime import date
from dateutil.relativedelta import relativedelta
from random import randint


class FixedLeg:
    def __init__(self, notional: float, rate: float, currency: str,
                 payment_frequency: str, accounting_basis_month: str, accounting_basis_year: str,
                 dated_date):
        self.rate = rate
        self.currency = currency
        self.payment_frequency = payment_frequency
        self.accounting_basis_month = accounting_basis_month
        self.accounting_basis_year = accounting_basis_year
        self.notional = notional
        self.dated_date = date.strptime(dated_date, "%Y.%m.%d")

    def accrued_interest(self):
        number_of_days = (date.today() - self.dated_date).days
        if self.accounting_basis_year == "360":
            interest = round(self.notional * self.rate * number_of_days / 360, 2)
            return interest

        elif self.accounting_basis_year == "365":
            interest = round(self.notional * self.rate * number_of_days / 365, 2)
            return interest

        elif self.accounting_basis_year.upper() == "ACT":
            number_of_days_year = 366 if calendar.isleap(date.today().year) else 365
            interest = round(self.notional * self.rate * number_of_days / number_of_days_year, 2)
            return interest

        else:
            raise ValueError("Year Accounting Basis must be either 360, 365 or ACT!")

    def next_payment_date(self):#to fix next payment date
        if self.accounting_basis_month.upper == "03M":
            payment_date = self.dated_date + relativedelta(months=3)
            return payment_date
        elif self.accounting_basis_month.upper == "06M":
            payment_date = self.dated_date + relativedelta(months=6)
            return payment_date
        elif self.accounting_basis_month.upper == "12M":
            payment_date = self.dated_date + relativedelta(months=12)
            return payment_date
        else:
            raise ValueError("Incorrect payment frequency!")


    def __str__(self):
        return (
            f"FIXED: Notional:{self.notional}, Rate: {self.rate}, "
            f"Currency: {self.payment_frequency.upper()}, "
            f"Accounting basis: {self.accounting_basis_year.upper()}/{self.accounting_basis_year.upper()}, "
            f"Dated date: {self.dated_date}")


class FloatingLeg:
    def __init__(self, notional: float, rate: str, currency: str,
                 payment_frequency: str, accounting_basis_month: str, accounting_basis_year: str,
                 dated_date):
        self.rate = rate
        self.currency = currency
        self.payment_frequency = payment_frequency
        self.accounting_basis_month = accounting_basis_month
        self.accounting_basis_year = accounting_basis_year
        self.notional = notional
        self.dated_date = date.strptime(dated_date, "%Y.%m.%d")

    def accrued_interest(self):
        number_of_days = (date.today() - self.dated_date).days
        rate_random = randint(1, 10)
        if self.accounting_basis_year == "360":
            interest = round(self.notional * rate_random / 100 * number_of_days / 360, 2)
            return interest

        elif self.accounting_basis_year == "365":
            interest = round(self.notional * rate_random / 100 * number_of_days / 365, 2)
            return interest

        elif self.accounting_basis_year.upper() == "ACT":
            number_of_days_year = 366 if calendar.isleap(date.today().year) else 365
            interest = round(self.notional * rate_random / 100 * number_of_days / number_of_days_year, 2)
            return interest

        else:
            raise ValueError("Year Accounting Basis must be either 360, 365 or ACT!")

    def __str__(self):
        return (
            f"FLOATING: Notional:{self.notional}, Rate: {self.rate.upper()}, "
            f"Currency: {self.payment_frequency.upper()}, "
            f"Accounting basis: {self.accounting_basis_year.upper()}/{self.accounting_basis_year.upper()}, "
            f"Dated date: {self.dated_date}")


class EventLeg:
    def __init__(self, notional: float, red_code: str, currency: str):
        self.notional = notional
        self.red_code = red_code
        self.currency = currency

    def __str__(self):
        return (
            f"EVENT: Notional:{self.notional}, "
            f"Currency: {self.currency.upper()}, "
            f"Red Code: {self.red_code.upper()}")


class ReturnLeg:
    def __init__(self, number_of_shares: float, underlying_asset: str, currency: str):
        self.number_of_shares = number_of_shares
        self.underlying_asset = underlying_asset
        self.currency = currency

    def __str__(self):
        return (
            f"RETURN: Number of shares:{self.number_of_shares}, "
            f"Currency: {self.currency.upper()}, "
            f"Red Code: {self.underlying_asset.upper()}")


class Swap:
    def __init__(self, swap_type: str, swap_id: str, receivable_leg, payable_leg, maturity_date):
        self.swap_type = swap_type
        self.swap_id = swap_id
        self.receivable_leg = receivable_leg
        self.payable_leg = payable_leg
        self.maturity_date = date.strptime(maturity_date, "%Y.%m.%d")

    def __str__(self):
        return (
            f"Swap Type: {self.swap_type.upper()} "
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


leg1_irs = FloatingLeg(1000000, "sofr", "usd", "03M",
                       "act", "365", "2025.12.25")
leg2_irs = FixedLeg(1000000, 0.01, "usd", "03m",
                    "30", "ACT", "2025.09.25")

swap1_irs = Swap(swap_type="IRS", maturity_date="2026.06.25", payable_leg=leg1_irs, receivable_leg=leg2_irs,
                 swap_id="IRS001")

leg1_cds = EventLeg(20000, "RED_CODE001", "EUR")
leg2_cds = FixedLeg(20000, 0.05, "EUR", "03M",
                    "30", "ACT", "2026.03.20")

swap1_cds = Swap("CDS", "CDS001", leg2_cds, leg1_cds, "2028.09.20")

leg1_cys = FixedLeg(6000000, 0.025, "eur", "06M",
                    "act", "act", "2025.10.15")
leg2_cys = FloatingLeg(750000, "fedl", "usd", "03M",
                       "30", "360", "2025.04.15")

swap1_cys = Swap("CYS", "CYS001", leg1_cys, leg2_cys, "2060.04.15")

leg1_trs = ReturnLeg(36, "asset001", "EUR")
leg2_trs = FixedLeg(700000, 0.05, "EUR", "06M",
                    "30", "360", "2026.02.10")
swap1_trs = Swap("TRS", "TRS001", leg2_trs, leg1_trs, "2026.08.10")

if __name__ == "__main__":
    print(leg2_irs.accrued_interest())
    print(leg2_irs.next_payment_date())
    print(leg1_irs.accrued_interest())
