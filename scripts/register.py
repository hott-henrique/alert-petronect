from petronect.data.UserData import UserData, AlertData

from petronect.persistence.session import get_sqlalchemy_session

from serverless.functions.ProcessBiddingAttachment.process_bidding_attachment import tokenize_text


def register_user_and_alert(user_name: str, user_email: str, alert_name: str, alert_words: list[str]):
    tokens = tokenize_text(text= "\n".join(alert_words))

    with get_sqlalchemy_session() as session:
        user = UserData(name=user_name, email=user_email)

        alert = AlertData(name=alert_name, words=alert_words, tokens=tokens)

        alert.user = user

        session.add(user)
        session.add(alert)
        session.commit()

        print(f"User '{user_name}' with alert '{alert_name}' registered successfully.")

if __name__ == "__main__":
    register_user_and_alert(
        user_name="FirstName LastName",
        user_email="email@email.com",
        alert_name="Monitoramento OSRV",
        alert_words=["afretamento", "sonda", "embarcações", "osrv"]
    )
