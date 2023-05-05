def calculate_total(items):
    total = 0
    for item in items:
        total += item['quantity'] * item['price']
    return total

if __name__ == '__main__':
    items = [
        {'name': 'Categorie A', 'quantity': 2, 'price': 2000},
        {'name': 'Categorie A1', 'quantity': 1, 'price': 2000},
        {'name': 'Categirie B', 'quantity': 3, 'price': 3000},
    ]
    total_amount = calculate_total(items)
    print(f'Total amount: {total_amount}')
