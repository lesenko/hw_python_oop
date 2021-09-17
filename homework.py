import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        today_amount = (record.amount for record in self.records
                        if record.date == today)
        return sum(today_amount)

    def get_week_stats(self):
        today_date = dt.datetime.now().date()
        week_ago = today_date - dt.timedelta(days=7)
        week_amount = (record.amount for record in self.records
                       if week_ago <= record.date <= today_date)
        return sum(week_amount)

    def get_today_balance(self):
        today_balance = self.limit - self.get_today_stats()
        return today_balance


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.today().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        balance_calories = self.get_today_balance()
        if balance_calories <= 0:
            return 'Хватит есть!'
        else:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{balance_calories} кКал')


class CashCalculator(Calculator):
    USD_RATE = 72.96
    EURO_RATE = 86.13
    RUB_RATE = 1

    def get_today_cash_remained(self, currency='rub') -> None:
        currencies = {'usd': ('USD', CashCalculator.USD_RATE),
                      'eur': ('Euro', CashCalculator.EURO_RATE),
                      'rub': ('руб', CashCalculator.RUB_RATE)}
        balance_cash = self.get_today_balance()
        if balance_cash == 0:
            return 'Денег нет, держись'
        elif currency not in currencies:
            return 'Такой валюты нет. Укажите usd, eur или rub.'
        else:
            name, rate = currencies[currency]
            today_cash = round((balance_cash) / rate, 2)
            if today_cash > 0:
                return f'На сегодня осталось {today_cash} {name}'
            else:
                today_cash_abs = abs(today_cash)
                return ('Денег нет, держись: твой долг - '
                        f'{today_cash_abs} {name}')
