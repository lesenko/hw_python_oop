import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
   
    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        sum_today = 0
        for record in self.records:
            if record.date == today:
                sum_today += record.amount
        return sum_today

    def get_week_stats(self):
        week_ago = dt.datetime.now().date() - dt.timedelta(days=7)
        today_date = dt.datetime.now().date()
        sum_week = 0
        for record in self.records:
            if record.date >= week_ago and record.date <= today_date:
                sum_week += record.amount
        return sum_week


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.today().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        today_calories = self.limit - self.get_today_stats()
        if today_calories <= 0:
            return 'Хватит есть!'
        else:
            return ('Сегодня можно съесть что-нибудь ещё, '
            f'но с общей калорийностью не более {today_calories} кКал')


class CashCalculator(Calculator):
    USD_RATE = 72.96
    EURO_RATE = 86.13
    RUB_RATE = 1

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency='rub') -> None:
        currencies = {'usd': ('USD', CashCalculator.USD_RATE),
                      'eur': ('Euro', CashCalculator.EURO_RATE),
                      'rub': ('руб', CashCalculator.RUB_RATE)}
        name, rate = currencies[currency]
        today_cash = round((self.limit - self.get_today_stats()) / rate, 2)
        if today_cash == 0:
            return 'Денег нет, держись'
        elif today_cash > 0:
            return f'На сегодня осталось {today_cash} {name}'
        else:
            today_cash_abs = abs(today_cash)
            return f'Денег нет, держись: твой долг - {today_cash_abs} {name}'


cash_calculator = CaloriesCalculator(1000)

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

print(cash_calculator.get_calories_remained())