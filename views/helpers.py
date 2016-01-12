def to_money(amount):
    return '' if amount is None else '${:,.2f}'.format(amount)
