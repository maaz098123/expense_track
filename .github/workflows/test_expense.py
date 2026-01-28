import os
import json
import expense

def setup_function():
    with open("expense.txt","w") as f:
        json.dump([],f)


def test_add_expense():
    expense.add_expenses("Food",50)
    data = expense.load_expenses()

    assert len(data) == 1
    assert data[0]["description"] == "Food"
    assert data[0]["amount"] == 50
   
    data = expense.load_expenses()
    assert len(data) == 0