from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

def home(request):
	form = TransactionForm(data=request.POST or None)
	if request.method == 'POST':
		pk = request.POST['account']
		return balance(request, pk)
	content = {'form': form}
	return render(request, 'checkbook/index.html', content)



def balance(request, pk):
	account = get_object_or_404(Account, pk=pk) # get object or present error
	transactions = Transaction.Transactions.filter(account = pk)
	current_total = account.initial_deposit
	table_contents = {}
	for t in transactions:
		if t.type == 'Deposit':
			current_total += t.amount
			table_contents.update({t: current_total})
		else:
			current_total -= t.amount
			table_contents.update({t: current_total})
	content = {'account': account, 'table_contents': table_contents, 'balance': current_total} # create dictionary
	return render(request, 'checkbook/BalanceSheet.html', content)



def create_account(request):
	form = AccountForm(data=request.POST or None)
	if request.method == 'POST': 
		if form.is_valid():
			form.save()
			return redirect('index')
	content = {'form': form}
	return render(request, 'checkbook/CreateNewAccount.html', content)
	""" Pull all fields from account and puts inside variable form. Then checks if
		request method is post and if it is it well redirect user to index page. 
		Then sends them to create a new account"""


def transaction(request):
	form = TransactionForm(data=request.POST or None)
	if request.method == 'POST': 
		if form.is_valid():
			form.save()
			pk = request.POST['account']
			form.save()
			return balance(request, pk)
	content = {'form': form}
	return render(request, 'checkbook/AddTransaction.html', content)
	""" Pull all fields from a transaction and puts inside variable form. Then checks if
		request method is post and if it is it well redirect user to index page. 
		Then sends them to create a new account"""

