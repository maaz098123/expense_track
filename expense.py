import os
from datetime import datetime
import argparse
import json


EXPENSE_FILE = "expense.txt"

if not os.path.exists(EXPENSE_FILE):
    with open(EXPENSE_FILE,"w")as f:
        json.dump([],f)
        

def load_expenses():
    with open(EXPENSE_FILE,"r") as f:
        return json.load(f)

def save_expenses(expenses):
    with open(EXPENSE_FILE,"w")as f:
        json.dump(expenses,f,indent=4)


def add_expenses(description,amount):
    if amount<=0:
        print("Amount must be positive")
        return
    
    expenses = load_expenses()
    expense_id = (max([e["id"]for e in expenses])+1)if expenses else 1
    expense={
        "id":expense_id,
        "date":datetime.now().strftime("%Y-%m-%d"),
        "description":description,
        "amount":amount
    }

    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expenses added successfully(ID:{expense_id})")

def update_expenses(expense_id,description=None,amount=None) :
    expenses = load_expenses()
    for e in expenses:
        if e["id"] == expense_id:
            if description:
              e["description"] = description
            if amount:
                e["amount"] = amount
                print("Amount must be positive")
                return
            e["amount"] = amount
            save_expenses(expenses)
            print(f"Expense ID {expense_id} update successfully")
            return
        print(f"Expense ID {expense_id} not found")

def delete_expenses(expense_id):
    expenses= load_expenses()
    new_expenses = [e for e in expenses if e["id"]!=expense_id]
    if len(new_expenses) == len(expenses):
        print(f"Expense ID {expense_id} not found")
    else:
        save_expenses(new_expenses)
        print(f"Expense ID {expense_id} deleted successfully")


def list_expenses():
    expenses =load_expenses()
    if not expenses:
        print("No expenses found")
        return
    print(f"{'ID':<4} {'DATE':<12} {'DESCRIPTION':<20} ${'AMOUNT':<10}")
    for e in expenses:
        print(f"{e['id']:<4} {e['date']:<12} {e['description']:<20} ${e["amount"]:<10}")


def summary(month=None):
    expenses=load_expenses()
    total= 0 
    filtered = []
    for e in expenses:
        if month:
            if datetime.strptime(e["date"], "%Y-%m-%d").month == month:
                filtered.append(e)
                total += e["amount"]
        else:
            total +=e["amount"]
    if month:
        print(f"Total expenses for month {month}:${total}")
    else:
        print(f"Total expenses: ${total}")


parser = argparse.ArgumentParser(description = "Simple Expense Tracker")
subparsers = parser.add_subparsers(dest="command")

parser_add = subparsers.add_parser("add")
parser_add.add_argument("--description",required=True)
parser_add.add_argument("--amount",type=float,required=True)

parser_update = subparsers.add_parser("update")
parser_update.add_argument("--id",type=int,required=True)
parser_update.add_argument("--description")
parser_update.add_argument("--amount",type=float)

parser_delete = subparsers.add_parser("delete")
parser_delete.add_argument("--id", type=int, required=True)

# List
subparsers.add_parser("list")

# Summary
parser_summary = subparsers.add_parser("summary")
parser_summary.add_argument("--month", type=int)

args = parser.parse_args()

if args.command == "add":
    add_expenses(args.description,args.amount)
elif args.command == "update":
    update_expenses(args.amount,args.description,args.id)
elif args.command == "delete":
    delete_expenses(args.id)
elif args.command == "list":
    list_expenses()
elif args.command == "summary":
    summary(args.month)
else:
    parser.print_help()

print(load_expenses())
