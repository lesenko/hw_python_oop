import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        records = self.records
        list = (record.amount for record in records if record.date == today)
        return sum(list)

    def get_week_stats(self):
        today_date = dt.datetime.now().date()
        week_ago = today_date - dt.timedelta(days=7)
        sum_week = 0
        for record in self.records:
            if week_ago <= record.date <= today_date:
                sum_week += record.amount
        return sum_week

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
        if self.get_today_balance() <= 0:
            return 'Хватит есть!'
        else:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {self.get_today_balance()} кКал')


class CashCalculator(Calculator):
    USD_RATE = 72.96
    EURO_RATE = 86.13
    RUB_RATE = 1

    def get_today_cash_remained(self, currency='rub') -> None:
        currencies = {'usd': ('USD', CashCalculator.USD_RATE),
                      'eur': ('Euro', CashCalculator.EURO_RATE),
                      'rub': ('руб', CashCalculator.RUB_RATE)}
        if self.get_today_balance() == 0:
            return 'Денег нет, держись'
        elif currency not in currencies:
            return 'В калькуляторе нет такой валюты. Укажите usd, eur или rub.'
        else:
            name, rate = currencies[currency]
            today_cash = round((self.get_today_balance()) / rate, 2)
            if today_cash > 0:
                return f'На сегодня осталось {today_cash} {name}'
            else:
                today_cash_abs = abs(today_cash)
                return f'Денег нет, держись: твой долг - {today_cash_abs} {name}'


cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('rub'))
# должно напечататься
# На сегодня осталось 555 руб 