from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from app.core.minio import MinioClient
from app.models.enquiry import Enquiry
from app.schemas.enquiry import EnquiryStatus
from app.schemas.email_body import (
    EnquirySentBody,
    EnquiryToBeConfirmedBody,
    EnquiryRejectedBody,
    EnquiryOptionBody,
)
from app.core.security import decrypt_reversible


async def send_enquiry_email(enquiry: Enquiry) -> bool:
    match enquiry.status:
        case EnquiryStatus.SENT:
            await send_enquiry_sent_email(enquiry)
        case EnquiryStatus.TBC:
            await send_enquiry_to_be_confirmed_email(enquiry)
        case EnquiryStatus.REJECTED:
            await send_enquiry_rejected_email(enquiry)
        case EnquiryStatus.OPTION:
            await send_enquiry_option_email(enquiry)
        case _:
            return False

    return True


async def send_enquiry_sent_email(enquiry: Enquiry) -> None:
    file_client = MinioClient()
    school = enquiry.school
    am_location = enquiry.am_location
    pm_location = enquiry.pm_location
    signed_url = file_client.sign_url(school.email_attachment_key)

    email_body = EnquirySentBody(
        home_address=enquiry.home_address,
        pickup_address=am_location.address if am_location else "",
        pickup_time=am_location.time if am_location else "",
        arrival_time=school.arrival_time,
        dropoff_address=pm_location.address if pm_location else "",
        dropoff_time=pm_location.time if pm_location else "",
        departure_time=school.departure_time,
        fare=enquiry.fare,
        signed_url=signed_url,
    )

    await send_email(
        subject="Enquiry Sent",
        recipients=[enquiry.email],
        template_name="enquiry_sent.html",
        template_body=email_body.model_dump(),
        mail_username=school.email if school.email else "",
        mail_password=decrypt_reversible(school.password) if school.password else "",
    )
    return None


async def send_enquiry_to_be_confirmed_email(enquiry: Enquiry) -> None:
    school = enquiry.school
    email_body = EnquiryToBeConfirmedBody(
        home_address=enquiry.home_address,
    )

    await send_email(
        subject="Enquiry to be Confirmed",
        recipients=[enquiry.email],
        template_name="enquiry_to_be_confirmed.html",
        template_body=email_body.model_dump(),
        mail_username=school.email if school.email else "",
        mail_password=decrypt_reversible(school.password) if school.password else "",
    )
    return None


async def send_enquiry_rejected_email(enquiry: Enquiry) -> None:
    school = enquiry.school
    email_body = EnquiryRejectedBody(
        home_address=enquiry.home_address,
    )

    await send_email(
        subject="Enquiry Rejected",
        recipients=[enquiry.email],
        template_name="enquiry_rejected.html",
        template_body=email_body.model_dump(),
        mail_username=school.email if school.email else "",
        mail_password=decrypt_reversible(school.password) if school.password else "",
    )
    return None


async def send_enquiry_option_email(enquiry: Enquiry) -> None:
    school = enquiry.school
    am_location = enquiry.am_location
    pm_location = enquiry.pm_location

    email_body = EnquiryOptionBody(
        home_address=enquiry.home_address,
        pickup_address=am_location.address if am_location else "",
        pickup_time=am_location.time if am_location else "",
        arrival_time=school.arrival_time,
        dropoff_address=pm_location.address if pm_location else "",
        dropoff_time=pm_location.time if pm_location else "",
        departure_time=school.departure_time,
        fare=enquiry.fare,
    )

    await send_email(
        subject="Enquiry Option Available",
        recipients=[enquiry.email],
        template_name="enquiry_option.html",
        template_body=email_body.model_dump(),
        mail_username=school.email if school.email else "",
        mail_password=decrypt_reversible(school.password) if school.password else "",
    )
    return None


async def send_email(
    subject: str,
    recipients: list[str],
    template_name: str,
    template_body: dict,
    mail_username: str,
    mail_password: str,
) -> None:
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=template_body,
        subtype=MessageType.html,
    )

    config = ConnectionConfig(
        MAIL_USERNAME=mail_username,
        MAIL_PASSWORD=mail_password,
        MAIL_FROM=mail_username,
        MAIL_PORT=587,
        MAIL_SERVER="smtp.gmail.com",
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
        TEMPLATE_FOLDER="app/email_templates",
    )

    fm = FastMail(config)
    await fm.send_message(message, template_name=template_name)
    return None
