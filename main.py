from data.transactions import transactions
from src.processing import filter_by_state, sort_by_date

print(filter_by_state(transactions))
print(sort_by_date(transactions, False))
