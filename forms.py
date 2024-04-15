from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange


class CreateAccountForm(FlaskForm):
    nombre = StringField(label='Nombre', validators=[
        DataRequired(message='Name is required, please type a Name'),
        Length(min=8, max=40, message='Min is 8, and 40 is max Name length')
    ])
    crear_cuenta = SubmitField(label='Crear Cuenta')


class AbonoRetiroForm(FlaskForm):
    monto = DecimalField(label='Monto', validators=[
        DataRequired(),
        NumberRange(
            min=0.00,
            max=10000,
            message='Out of Range'
        )
    ])
    deposito = SubmitField(label='Deposito')
    retiro = SubmitField(label='Retiro')


class TransferenciaForm(FlaskForm):
    monto = DecimalField(label='Monto', validators=[
        DataRequired(),
        NumberRange(
            min=0.00,
            max=10000,
            message='Out of Range'
        )
    ])
    transferir = SubmitField(label='Transferir')
