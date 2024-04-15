import database as db
from datetime import datetime


class BankAccount:
    def __init__(self):
        pass

    def balance(self):
        cursor = db.connection.cursor()
        sql = "SELECT * FROM cuenta"
        cursor.execute(sql)
        result = cursor.fetchall()
        # dict_cuentas = []
        # column_name = [column[0] for column in cursor.description]
        # for record in result:
        #     dict_cuentas.append(dict(zip(column_name, record)))
        cursor.close()
        return result

    def movements(self, nro_cuenta, tipo, importe):
        tipo_value = tipo
        if tipo == 'R':
            balance = self.get_balance(nro_cuenta)
            if float(balance) >= float(importe):
                tipo_value = 'R'
            else:
                return "No enough money"
        cursor = db.connection.cursor()
        fecha = datetime.now()
        fecha_str = fecha.strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO movimiento (NRO_CUENTA, FECHA, TIPO, IMPORTE) VALUES (%s,%s,%s,%s)"
        nuevo_moviemiento = (
            nro_cuenta,
            fecha_str,
            tipo_value,
            importe
        )
        cursor.execute(sql, nuevo_moviemiento)
        db.connection.commit()
        cursor.close()
        self.update_balance(nro_cuenta,tipo_value,importe)
        return "Movement Saved!"

    def create(self, tipo, moneda, nombre):
        saldo = 0
        cursor = db.connection.cursor()
        sql = "INSERT INTO cuenta (NRO_CUENTA,TIPO,MONEDA,NOMBRE,SALDO) VALUES (%s,%s,%s,%s,%s)"
        nro_cuenta = self.create_nro_account(tipo)
        nueva_cuenta = (
            nro_cuenta,
            tipo,
            moneda,
            nombre,
            saldo
        )
        cursor.execute(sql, nueva_cuenta)
        db.connection.commit()
        cursor.close()
        return nro_cuenta


    def create_nro_account(self, tipo):
        seed = self.last_cuenta(tipo)
        if len(seed) > 0:
            nro_cuenta = int(seed)+1
        else:
            if tipo == 'AHO':
                nro_cuenta = '10000000000000'

            elif tipo == 'CTE':
                nro_cuenta = '1000000000000'
        return str(nro_cuenta)

    def last_cuenta(self, tipo):
        cursor = db.connection.cursor()
        sql = f"SELECT nro_cuenta FROM cuenta where tipo = '{tipo}' ORDER BY nro_cuenta DESC LIMIT 1"
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result[0]

    def get_balance(self, nro_cuenta):
        cursor = db.connection.cursor()
        sql = f"SELECT SALDO FROM CUENTA WHERE NRO_CUENTA = '{nro_cuenta}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result[0]

    def get_list_accounts(self):
        cursor = db.connection.cursor()
        sql = "SELECT NRO_CUENTA FROM CUENTA"
        cursor.execute(sql)
        list_account = [account[0] for account in cursor.fetchall()]
        cursor.close()
        return list_account

    def update_balance(self, nro_cuenta, tipo, importe):
        if tipo == 'R':
            importe = float(importe)*(-1)
        old_balance = self.get_balance(nro_cuenta)
        new_balance = float(old_balance)+ float(importe)
        cursor = db.connection.cursor()
        sql = f"UPDATE cuenta SET saldo = {new_balance} where nro_cuenta = '{nro_cuenta}'"
        cursor.execute(sql)
        db.connection.commit()
        cursor.close()

    def account_movements(self, nro_cuenta):
        cursor = db.connection.cursor()
        sql = f"SELECT * FROM movimiento WHERE NRO_CUENTA = '{nro_cuenta}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        print(result)
        return result