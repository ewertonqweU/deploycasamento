from flask import render_template, url_for, redirect
from requests import session

from ConviteDigital import app, database
from ConviteDigital.models import Usuario,Foto,Pagamento_Simplificado
from flask_login import login_required, login_user, logout_user, current_user
from ConviteDigital.forms import  FormLogin, FormCriarConta, FormFoto,FormPGF
import os
from werkzeug.utils import secure_filename
from Pix import GerarQrcode

@app.route("/", methods=["GET","POST"])
def homepage():
    formPfacil = FormPGF()
    if formPfacil.validate_on_submit():
        pagamentosimplificado = Pagamento_Simplificado(convidados=formPfacil.convidados.data,
                                          quantidade=formPfacil.qtd.data)
        qrcodecop = GerarQrcode(formPfacil.convidados.data,float(formPfacil.qtd.data))[0]
        qrcodeimg = GerarQrcode(formPfacil.convidados.data,float(formPfacil.qtd.data))[1]
        statusPag = GerarQrcode(formPfacil.convidados.data,float(formPfacil.qtd.data))[2]
        database.session.add(pagamentosimplificado)
        database.session.commit()
        script_to_run = True
        return render_template("homepage.html", form=formPfacil, qrcodecop=qrcodecop, qrcodeimg=qrcodeimg,
                               statusPag=statusPag,script_to_run=script_to_run)
    else:
        return render_template("homepage.html", form=formPfacil)



@app.route("/criarconta", methods=["GET","POST"])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        usuario = Usuario(username=form_criarconta.user.data,
                          senha=form_criarconta.senha.data)

        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("confirma",user=usuario.username))

    return render_template("criarconta.html",form = form_criarconta)



@app.route("/confirma/<user>", methods=["GET","POST"])
@login_required
def confirma(user):
    if user == current_user.username:
        qrcodecop = GerarQrcode(current_user.username)[0]
        qrcodeimg = GerarQrcode(current_user.username)[1]
        statusPag = GerarQrcode(current_user.username)[2]
        formfoto = FormFoto()
        #pgto = Usuario(pagamento = statusPag)
        item = database.session.query(Usuario).filter_by(username=current_user.username).first()
        item.pagamento=statusPag
        database.session.commit()
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            nome_arq = secure_filename(arquivo.filename)
            nome_arquivo = arquivo.filename
            extensao_arquivo = os.path.splitext(nome_arquivo)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__))
                              ,app.config["UPLOAD_FOLDER"],f"Comprovante de {current_user.username}{extensao_arquivo[1]}")
            arquivo.save(caminho)
            foto = Foto(imagem = nome_arq, id_usuario = current_user.id )
            database.session.add(foto)
            database.session.commit()



        return render_template("pagamento.html", user=user, form=formfoto, qrcodecop = qrcodecop,qrcodeimg = qrcodeimg,statusPag = statusPag)
    else:

        return render_template("pagamento.html",user=user, form=None)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))