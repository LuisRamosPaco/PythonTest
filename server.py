from flask import Flask, render_template, request, url_for, redirect
from bank_account import BankAccount as ba
from forms import CreateAccountForm, AbonoRetiroForm, TransferenciaForm

app = Flask(__name__)
app.secret_key = "thisisatestNotsurewhatthistextis"

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/create', methods=['GET', 'POST'])
def create_account():
    create_account_form = CreateAccountForm()

    if request.method == 'POST' and create_account_form.validate_on_submit():
        tipo = request.form.get('tipo')
        moneda = request.form.get('moneda')
        nombre = request.form.get('nombre')
        new_account = ba()
        new_account.create(tipo=tipo, moneda=moneda, nombre=nombre)
        return redirect(url_for('create_account'))
    return render_template('create.html', form=create_account_form)


@app.route('/abono_retiro', methods=['GET', 'POST'])
def abono_retiro():
    bank_account = ba()
    cuentas = bank_account.get_list_accounts()
    abono_retiro_form = AbonoRetiroForm()
    if request.method == 'POST' and abono_retiro_form.validate_on_submit():
        cuenta = request.form.get('cuenta')
        importe = request.form.get('monto')
        if request.form.__contains__('deposito'):
            bank_account.movements(cuenta, 'D', importe)
        elif request.form.__contains__('retiro'):
            bank_account.movements(cuenta, 'R', importe)
        return redirect(url_for('abono_retiro'))

    return render_template('abono_retiro.html', nro_cuentas=cuentas, form=abono_retiro_form)


@app.route('/transferencias', methods=['GET', 'POST'])
def transferencias():
    bank_account = ba()
    cuentas = bank_account.get_list_accounts()
    transferencias_form = TransferenciaForm()
    if request.method == 'POST' and transferencias_form.validate_on_submit():
        nro_cuenta_retiro = request.form.get('cuenta_retiro')
        nro_cuenta_deposito = request.form.get('cuenta_deposito')
        monto = request.form.get('monto')
        bank_account.movements(nro_cuenta_retiro, 'R', monto)
        bank_account.movements(nro_cuenta_deposito, 'D', monto)
        return redirect(url_for('transferencias'))

    return render_template('transferencia.html', nro_cuentas=cuentas, form=transferencias_form)


@app.route('/saldos')
def saldos():
    saldos_headers = ('Cuenta', 'Tipo', 'Moneda', 'Nombre', 'Saldo')
    saldos = ba()
    table = saldos.balance()
    return render_template('saldos.html', titles_table=saldos_headers, table=table)


@app.route('/movimientos/<string:nro_cuenta>')
def movimientos(nro_cuenta):
    movimientos_headers = ('Nro Cuenta', 'Fecha', 'Movimiento', 'Moneda')
    account_movements = ba()
    transacciones = account_movements.account_movements(nro_cuenta)
    return render_template('movimientos.html', titles_table=movimientos_headers, movimientos=transacciones)


if __name__ == "__main__":
    app.run(debug=True)
