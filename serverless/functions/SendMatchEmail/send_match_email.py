import logging

from petronect.model.PetronectBidding import PetronectBidding

from petronect.persistence.AlertPersistence import AlertPersistence
from petronect.persistence.PetronectBiddingPersistence import PetronectBiddingPersistence, AlertMatching

from serverless.EmailSender import EmailSender
from serverless.KeyValueStorage import KeyValueStorage


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    assert isinstance(event, dict)

    alert_matching = AlertMatching.model_validate(event)

    alert = AlertPersistence.get(alert_matching.alert_id)

    assert alert

    bidding = PetronectBiddingPersistence.get(alert_matching.bidding)

    assert bidding

    bidding_src = PetronectBidding.model_validate(dict(bidding.data)) # type: ignore

    storage = KeyValueStorage()

    attachments = [ (at.DESCRIPTION, storage.load(f"{bidding}:{at.DESCRIPTION}")) for at in bidding_src.ANEXOS]

    region_lines = [ f"- {region.REGION_DESCRIPTION} ({region.REGION.value})" for region in bidding_src.REGIONS ]

    region_html = "".join(f"<p>{line}</p>" for line in region_lines) if region_lines else "<p>N/A</p>"

    alert_html = f"""
        <div class="alert">
            <p class="alert-title">Alerta:</p>
            <p>{alert.name}</p>
            <p class="alert-title">Termos:</p>
            <p>{', '.join(alert.words)}</p>
        </div>
    """

    files_html = '\n'.join(['<p>' + file + '</p>' for file in alert_matching.files ])

    files_section_html = f"""
        <div class="alert">
            <p class="alert-title">Arquivos:</p>
            {files_html}
        </div>
    """
    # HTML body
    html_body = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Alerta de Oportunidade na Petronect</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f6f8;
                margin: 0;
                padding: 0;
                color: #333;
            }}
            .container {{
                max-width: 700px;
                margin: 30px auto;
                background-color: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }}
            .header {{
                background-color: #004785;
                color: white;
                padding: 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 22px;
            }}
            .content {{
                padding: 30px;
            }}
            .content h2 {{
                color: #004785;
                font-size: 18px;
                margin-bottom: 10px;
            }}
            .content p {{
                margin: 6px 0;
            }}
            .alert {{
                margin-bottom: 15px;
            }}
            .alert-title {{
                font-weight: bold;
            }}
            .footer {{
                background-color: #eeeeee;
                text-align: center;
                padding: 20px;
                font-size: 13px;
                color: #666;
            }}
            .divider {{
                border-top: 1px solid #ddd;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Oportunidade Petronect</h1>
            </div>
            <div class="content">
                <h2>Alerta</h2>
                {alert_html}

                <div class="divider"></div>

                <h2>Oportunidade</h2>
                <p><strong>Número:</strong> {bidding_src.OPPORT_NUM}</p>
                <p><strong>Descrição:</strong> {bidding_src.DESC_OBJ_CONTRAT}</p>
                <p><strong>Data de publicação:</strong> {bidding_src.POSTING_DATE.strftime('%d/%m/%Y')}</p>
                <p><strong>Data de abertura:</strong> {bidding_src.START_DATE.strftime('%d/%m/%Y')} às {bidding_src.START_HOUR}</p>
                <p><strong>Data de encerramento:</strong> {bidding_src.END_DATE.strftime('%d/%m/%Y')} às {bidding_src.END_HOUR}</p>

                <div class="divider"></div>

                <h2>Regiões</h2>
                {region_html}

                <div class="divider"></div>

                <h2>Arquivos</h2>
                {files_section_html}
            </div>
            <div class="footer">
                Este é um e-mail automático enviado pelo sistema de monitoramento de oportunidades da Petronect.
            </div>
        </div>
    </body>
    </html>
    """

    EmailSender().send_email(
        to_email=alert.user.email,
        subject="Aviso de oportunidade na plataforma Petronect.",
        body=html_body,
        attachments=attachments,
        html=True
    )

    logger.info(f"Email sent to {alert.user.email}.")
