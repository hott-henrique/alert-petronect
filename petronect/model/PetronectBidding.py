import datetime as dt, pathlib, typing as t

import pydantic
import requests

from petronect.base.BaseModel import BaseModel

from petronect.model.PetronectCountry import PetronectCountry
from petronect.model.PetronectState import PetronectState


class Attachment(BaseModel):
    DESCRIPTION: str
    PHIO_OBJID: str

    def download(self) -> bytes:
        DOWNLOAD_FORMAT_URL = "https://www.petronect.com.br/sap/opu/odata/SAP/YPCON_PUB_ATTACHMENT_DOWNLOAD_SRV/attachmentSet('{file_id}')/$value"

        response = requests.get(DOWNLOAD_FORMAT_URL.format(file_id=self.PHIO_OBJID))

        if response.ok:
            return response.content

        response.raise_for_status()

        assert False

class Note(BaseModel):
    TDFORMAT: str
    TDLINE: str

class ItemNote(BaseModel):
    NOTAS: t.List[Note]

class Item(BaseModel):
    ITEM_NUM: str
    EXLIN: str
    ITEM_DESC: str
    ITEM_NOTES: t.List[ItemNote]
    UNIT: str
    QUANTITY: float
    DELIV_DATE: t.Optional[dt.date]
    GROUPING_LEVEL: t.Optional[str]
    ITEM_PROCESS_TYP: str
    FAMILY: t.Optional[str]
    FAMILY_DESCR: t.Optional[str]
    NUM_MATERIAL: t.Optional[str]
    FAMILY_CLASSIF: t.Optional[str]

    @pydantic.field_validator("DELIV_DATE", mode="before")
    @classmethod
    def parse_optional_date(cls, v: str | dt.date | None) -> t.Optional[dt.date]:
        if isinstance(v, dt.date):
            return v

        if v in ("0000-00-00", "", None):
            return None

        return dt.datetime.strptime(v, "%Y-%m-%d").date()

class Region(BaseModel):
    COUNTRY: PetronectCountry
    REGION: PetronectState
    REGION_DESCRIPTION: str

class PetronectBidding(BaseModel):
    OPPORT_NUM: str
    DOU_NUM: t.Optional[str]
    LIMIT_IN_DAYS: int
    COMPANY: str
    COMPANY_DESC: str
    STATUS: str
    STATUS_DESC: str
    OPPORT_TYPE: str
    POSTING_DATE: dt.date
    OPPORT_DESCR: str
    DOU_PUBL_DATE: dt.date
    START_DATE: dt.date
    START_HOUR: dt.time
    END_DATE: dt.date
    END_HOUR: dt.time
    OPEN_DATE: dt.date
    OPEN_HOUR: dt.time
    SUB_STATUS: t.Optional[str]
    DISPUTE_MODE: str
    ANEXOS: t.List[Attachment]
    ITEMS: t.List[Item]
    IS_EQUALIZED: t.Optional[str]
    HAS_PREQUALIFIED: t.Optional[str]
    IS_PREQUALI: t.Optional[str]
    PQ_VENDOR_LIST_DATE: t.Optional[dt.date]
    PQ_VENDOR_LIST_HOUR: t.Optional[dt.time]
    DESC_DETAIL: t.Optional[str]
    REGIONS: t.List[Region]
    AUC_START_DATE: t.Optional[dt.date]
    AUC_START_TIME: t.Optional[dt.time]
    NAT_COVERAGE: str
    DESC_OBJ_CONTRAT: str

    @pydantic.field_validator("PQ_VENDOR_LIST_DATE", "AUC_START_DATE", mode="before")
    @classmethod
    def parse_optional_date(cls, v: str | dt.date | None) -> t.Optional[dt.date]:
        if isinstance(v, dt.date):
            return v

        if v in ("0000-00-00", "", None):
            return None

        return dt.datetime.strptime(v, "%Y-%m-%d").date()

    @pydantic.field_validator("PQ_VENDOR_LIST_HOUR", "AUC_START_TIME", mode="before")
    @classmethod
    def parse_optional_time(cls, v: str | dt.time | None) -> t.Optional[dt.time]:
        if isinstance(v, dt.time):
            return v

        if v in ("00:00:00", "", None):
            return None
        return dt.datetime.strptime(v, "%H:%M:%S").time()
