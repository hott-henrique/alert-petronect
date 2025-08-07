import datetime as dt, hashlib, io, json, logging

import requests

from petronect.persistence.PetronectBiddingPersistence import PetronectBiddingPersistence

from serverless.FunctionInvoker import FunctionInvoker
from serverless.KeyValueStorage import KeyValueStorage


sim_data = {
  "d": {
    "EvXml": '{ "TAB": [ { "OPPORT_NUM": "7004486289", "DOU_NUM": "", "LIMIT_IN_DAYS": 90, "COMPANY": "1000", "COMPANY_DESC": "Petróleo Brasileiro S. A.", "STATUS": "I1011", "STATUS_DESC": "Publicado", "OPPORT_TYPE": "LICT", "POSTING_DATE": "2025-07-15", "OPPORT_DESCR": "Aquisição de Equipamentos e Acessório...", "DOU_PUBL_DATE": "2025-07-16", "START_DATE": "2025-07-16", "START_HOUR": "17:00:00", "END_DATE": "2025-07-28", "END_HOUR": "12:00:00", "OPEN_DATE": "2025-07-28", "OPEN_HOUR": "12:00:00", "SUB_STATUS": "", "DISPUTE_MODE": "02", "ANEXOS": [ { "DESCRIPTION": "EDITAL E ADENDOS.zip", "PHIO_OBJID": "005056AC507E1FE098CF5D1BADB0B2BC" }, { "DESCRIPTION": "SOLICITACAO_DE_COTACAO", "PHIO_OBJID": "005056AC507E1FE098CF5F31265592BC" } ], "ITEMS": [ { "ITEM_NUM": "0000000001", "EXLIN": "0001", "ITEM_DESC": "GLOBAL DE CFTV_CAMERAS SIMPLES", "ITEM_NOTES": [ { "NOTAS": [ { "TDFORMAT": "X", "TDLINE": "MAT.FORNEC: Global de CFTV MAC" } ] } ], "UNIT": "UN", "QUANTITY": 1.0, "DELIV_DATE": "2025-05-30", "GROUPING_LEVEL": "", "ITEM_PROCESS_TYP": "MATL", "FAMILY": "", "FAMILY_DESCR": "Bens corporativo Nova Lei", "NUM_MATERIAL": "", "FAMILY_CLASSIF": "98000" } ], "IS_EQUALIZED": "", "HAS_PREQUALIFIED": "", "IS_PREQUALI": "", "PQ_VENDOR_LIST_DATE": "0000-00-00", "PQ_VENDOR_LIST_HOUR": "00:00:00", "DESC_DETAIL": "", "REGIONS": [ { "COUNTRY": "BR", "REGION": "RJ", "REGION_DESCRIPTION": "Rio de Janeiro" } ], "AUC_START_DATE": "0000-00-00", "AUC_START_TIME": "00:00:00", "NAT_COVERAGE": "N", "DESC_OBJ_CONTRAT": "Aquisição de Equipamentos e Acessórios para CFTV e Segurança Eletrônica, por contrato global" }, { "OPPORT_NUM": "7004486047", "DOU_NUM": "", "LIMIT_IN_DAYS": 90, "COMPANY": "1000", "COMPANY_DESC": "Petróleo Brasileiro S. A.", "STATUS": "I1011", "STATUS_DESC": "Publicado", "OPPORT_TYPE": "LICT", "POSTING_DATE": "2025-07-14", "OPPORT_DESCR": "Aquisição de Analisador de Ponto de E...", "DOU_PUBL_DATE": "2025-07-16", "START_DATE": "2025-07-17", "START_HOUR": "12:00:00", "END_DATE": "2025-07-29", "END_HOUR": "12:00:00", "OPEN_DATE": "2025-07-29", "OPEN_HOUR": "12:00:00", "SUB_STATUS": "", "DISPUTE_MODE": "02", "ANEXOS": [ { "DESCRIPTION": "ADENDO A - Minutas.zip", "PHIO_OBJID": "0050569363001FD0989CE2BEB61FB3D7" }, { "DESCRIPTION": "Edital Requisitos de Habilitação.zip", "PHIO_OBJID": "0050569363001FD0989CE2F1B0AA93D7" }, { "DESCRIPTION": "Anexo Simplificado II - 885 - SMS0092159 Rev.1 2.pdf", "PHIO_OBJID": "0050569363001FD0989CE2F1B0B193D7" }, { "DESCRIPTION": "ET.2025.003-Pontodeentupimento-ASTMD6371-RNEST-vr01_202507141459", "PHIO_OBJID": "0050569363001FD0989CE309E2B193D7" }, { "DESCRIPTION": "ADENDO C - PPU BENS e SERVICOS_Retenção 1.xlsx", "PHIO_OBJID": "005056820C811FD098C6DB726B4CC68F" }, { "DESCRIPTION": "SOLICITACAO_DE_COTACAO", "PHIO_OBJID": "005056820C811FD098C74105B6C8468F" } ], "ITEMS": [ { "ITEM_NUM": "0000000001", "EXLIN": "0001", "ITEM_DESC": "EQUIP. DET.PTO.ENTUPIMENTO", "ITEM_NOTES": [ { "NOTAS": [ { "TDFORMAT": "X", "TDLINE": "Equipamento automático ;determin.ponto de entupimento ;em metal e plástico ;conf.EN116,IP309 ou ASTM D6371 ;" }, { "TDFORMAT": "X", "TDLINE": "Equipamento automático ;determin.ponto de entupimento ;em metal e plástico ;conf.EN116,IP309 ou ASTM D6371 ;Tp: ISL 0118-010-001 \n \n" }, { "TDFORMAT": "X", "TDLINE": "" } ] } ], "UNIT": "UN", "QUANTITY": 1.0, "DELIV_DATE": "2025-12-30", "GROUPING_LEVEL": "", "ITEM_PROCESS_TYP": "MATL", "FAMILY": "98010814", "FAMILY_DESCR": "", "NUM_MATERIAL": "12755683", "FAMILY_CLASSIF": "98010814" } ], "IS_EQUALIZED": "", "HAS_PREQUALIFIED": "", "IS_PREQUALI": "", "PQ_VENDOR_LIST_DATE": "0000-00-00", "PQ_VENDOR_LIST_HOUR": "00:00:00", "DESC_DETAIL": "", "REGIONS": [ { "COUNTRY": "BR", "REGION": "PE", "REGION_DESCRIPTION": "Pernambuco" } ], "AUC_START_DATE": "0000-00-00", "AUC_START_TIME": "00:00:00", "NAT_COVERAGE": "N", "DESC_OBJ_CONTRAT": "Aquisição de Analisador de Ponto de Entupimento com Serviços Associados" }, { "OPPORT_NUM": "7004486043", "DOU_NUM": "", "LIMIT_IN_DAYS": 90, "COMPANY": "1000", "COMPANY_DESC": "Petróleo Brasileiro S. A.", "STATUS": "I1011", "STATUS_DESC": "Publicado", "OPPORT_TYPE": "LICI", "POSTING_DATE": "2025-07-14", "OPPORT_DESCR": "Aquisição de Bomba fundo.", "DOU_PUBL_DATE": "2025-07-16", "START_DATE": "2025-07-16", "START_HOUR": "14:00:00", "END_DATE": "2025-07-24", "END_HOUR": "17:00:00", "OPEN_DATE": "2025-07-24", "OPEN_HOUR": "17:00:00", "SUB_STATUS": "", "DISPUTE_MODE": "02", "ANEXOS": [ { "DESCRIPTION": "Bomba de fundo.zip", "PHIO_OBJID": "00505693CAB21FD098CC19013075E511" }, { "DESCRIPTION": "SOLICITACAO_DE_COTACAO", "PHIO_OBJID": "00505693CAB21FD098CC3765E335A511" } ], "ITEMS": [ { "ITEM_NUM": "0000000001", "EXLIN": "0001", "ITEM_DESC": "BOMBA FUNDO BMF-022 25-225 THC 20-4-2-0", "ITEM_NOTES": [ { "NOTAS": [ { "TDFORMAT": "X", "TDLINE": "Bomba de fundo para bombeio mecânico ;Padrão API SPEC 11AX ;Código petrobras PM-08: BMF-022 ;tipo tubular ;25-225 THC 20-4-2-0 ;Mate" }, { "TDFORMAT": "X", "TDLINE": "rial da camisa: Aço carbono cromado ;folga pistão/camisa: 0,003 pol ;" }, { "TDFORMAT": "X", "TDLINE": "Bomba de fundo para bombeio mecânico ;Padrão API SPEC 11AX ;Código petrobras PM-08: BMF-022 ;tipo tubular ;25-225 THC 20-4-2-0 ;Mate" }, { "TDFORMAT": "X", "TDLINE": "rial da camisa: Aço carbono cromado ;folga pistão/camisa: 0,003 pol ; ---------- REFERÊNCIA: 25225THC20420P22 / FABRICANTE: BOLLAND" }, { "TDFORMAT": "X", "TDLINE": " \n \n" } ] } ], "UNIT": "UN", "QUANTITY": 13.0, "DELIV_DATE": "2025-10-08", "GROUPING_LEVEL": "", "ITEM_PROCESS_TYP": "MATL", "FAMILY": "98011546", "FAMILY_DESCR": "", "NUM_MATERIAL": "12095521", "FAMILY_CLASSIF": "98011546" } ], "IS_EQUALIZED": "", "HAS_PREQUALIFIED": "", "IS_PREQUALI": "", "PQ_VENDOR_LIST_DATE": "0000-00-00", "PQ_VENDOR_LIST_HOUR": "00:00:00", "DESC_DETAIL": "", "REGIONS": [ { "COUNTRY": "BR", "REGION": "BA", "REGION_DESCRIPTION": "Bahia" } ], "AUC_START_DATE": "0000-00-00", "AUC_START_TIME": "00:00:00", "NAT_COVERAGE": "N", "DESC_OBJ_CONTRAT": "Aquisição de Bomba fundo." } ] }',
    "IvTypeOfOpport": "01",
    "__metadata": {
      "id": "https://WWW.PETRONECT.COM.BR:443/sap/opu/odata/SAP/YPCON_GET_XML_SRV/getXMLSet('01')",
      "type": "YPCON_GET_XML_SRV.getXML",
      "uri": "https://WWW.PETRONECT.COM.BR:443/sap/opu/odata/SAP/YPCON_GET_XML_SRV/getXMLSet('01')"
    }
  }
}
sim_data["d"]["EvXml"] = sim_data["d"]["EvXml"].replace("\n", "\\n").replace("\r", "\\r")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    assert isinstance(event, dict)

    logger.info("Executing check on biddings hash.")

    response = requests.get("https://www.petronect.com.br/sap/opu/odata/SAP/YPCON_GET_XML_SRV/getXMLSet('01')?$format=json")

    if not response.ok:
        raise Exception("Could not fetch data from petronect.")

    data = json.dumps(response.json(), sort_keys=True).encode('utf-8')

    # data = json.dumps(sim_data, sort_keys=True).encode('utf-8')

    current_hash = hashlib.sha256(data).hexdigest()

    storage = KeyValueStorage()

    if not storage.exists("PETRONECT_LAST_KNOWN_HASH") or storage.load("PETRONECT_LAST_KNOWN_HASH").decode() != current_hash:
        logger.info("New data detected, updating stored hash and data.")

        storage.save("PETRONECT_LAST_KNOWN_HASH", current_hash.encode('utf-8'))
        storage.save("PETRONECT_LAST_KNOWN_DATA", data)

        logger.info("Triggering processing.")

        biddings_data: dict = json.load(io.BytesIO(data))

        biddings = [ bidding for bidding in json.loads(biddings_data["d"]["EvXml"])["TAB"] ]

        for bidding in biddings:
            if PetronectBiddingPersistence.exists(bidding):
                continue

            FunctionInvoker().trigger("process_new_bidding", dict(bidding=bidding))

    logger.info("Finished executing check on biddings hash.")
