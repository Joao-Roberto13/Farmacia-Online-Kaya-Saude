#Email: farmaciakaya@gmail.com  
#Password: farmaciakaya2024
#App Password: grzclbpnpsmdlrzp
import smtplib
import streamlit as st

HOST = "smtp.gmail.com"
PORT = 587

def enviar_Email(ToMail, info, sub, successo):
    FROM_EMAIL = "farmaciakaya@gmail.com"
    TO_EMAIL = ToMail
    PASSWORD = "grzclbpnpsmdlrzp"

    try:
        # Conectando ao servidor SMTP do Gmail
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()  # Inicia a comunicação criptografada
        servidor.login(FROM_EMAIL, PASSWORD)

        # Criando a mensagem
        mensagem = f"Subject: {sub}\n\n{info}".encode('utf-8')

        # Enviando o e-mail
        servidor.sendmail(FROM_EMAIL, TO_EMAIL, mensagem)
        st.success(f"{successo}. Verifique o seu email!")
    
    except Exception as e:
        #print(f"Erro ao enviar o e-mail: {e}")
        st.error(f"Erro ao enviar o e-mail: {e}")
    
    finally:
        try:
            servidor.quit()
        except:
            pass  # No need to handle this if smtp is not initialized
