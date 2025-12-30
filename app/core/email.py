from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.core.config import settings
from app.core.minio import MinioClient
from app.schemas import (
    EnquiryOptionBody,
    EnquiryOut,
    EnquiryRegistrationBody,
    EnquiryRejectedBody,
    EnquirySentBody,
    EnquiryStatus,
    EnquiryToBeConfirmedBody,
)


async def send_enquiry_email(enquiry: EnquiryOut) -> bool:
    match enquiry.status:
        case EnquiryStatus.SENT:
            await send_enquiry_sent_email(enquiry)
        case EnquiryStatus.TBC:
            await send_enquiry_to_be_confirmed_email(enquiry)
        case EnquiryStatus.REJECTED:
            await send_enquiry_rejected_email(enquiry)
        case EnquiryStatus.OPTION:
            await send_enquiry_option_email(enquiry)
        case EnquiryStatus.REGISTRATION:
            print("Sending enquiry registration email")
            await send_enquiry_registration_email(enquiry)
        case _:
            return False

    return True


async def send_enquiry_sent_email(enquiry: EnquiryOut) -> None:
    file_client = MinioClient()
    school = enquiry.school
    am_location = enquiry.am_location
    pm_location = enquiry.pm_location
    signed_url = file_client.sign_url(school.email_attachment_key)

    email_body = EnquirySentBody(
        home_address=enquiry.home_address,
        pickup_address=am_location.address if am_location else "",
        pickup_time=am_location.time_reach if am_location else "",
        arrival_time=school.arrival_time,
        dropoff_address=pm_location.address if pm_location else "",
        dropoff_time=pm_location.time_reach if pm_location else "",
        departure_time=school.departure_time,
        fare=enquiry.fare,
        signed_url=signed_url,
    )

    await send_email(
        subject="Enquiry Sent",
        recipients=[enquiry.email],
        template_name="enquiry_sent.html",
        template_body=email_body.model_dump(),
        mail_username=school.email,
        mail_password=school.password,
    )
    return None


async def send_enquiry_to_be_confirmed_email(enquiry: EnquiryOut) -> None:
    school = enquiry.school
    email_body = EnquiryToBeConfirmedBody(
        home_address=enquiry.home_address,
    )

    await send_email(
        subject="Enquiry to be Confirmed",
        recipients=[enquiry.email],
        template_name="enquiry_to_be_confirmed.html",
        template_body=email_body.model_dump(),
        mail_username=school.email,
        mail_password=school.password,
    )
    return None


async def send_enquiry_rejected_email(enquiry: EnquiryOut) -> None:
    school = enquiry.school
    email_body = EnquiryRejectedBody(
        home_address=enquiry.home_address,
    )

    await send_email(
        subject="Enquiry Rejected",
        recipients=[enquiry.email],
        template_name="enquiry_rejected.html",
        template_body=email_body.model_dump(),
        mail_username=school.email,
        mail_password=school.password,
    )
    return None


async def send_enquiry_option_email(enquiry: EnquiryOut) -> None:
    school = enquiry.school
    am_location = enquiry.am_location
    pm_location = enquiry.pm_location

    email_body = EnquiryOptionBody(
        home_address=enquiry.home_address,
        pickup_address=am_location.address if am_location else "",
        pickup_time=am_location.time_reach if am_location else "",
        arrival_time=school.arrival_time,
        dropoff_address=pm_location.address if pm_location else "",
        dropoff_time=pm_location.time_reach if pm_location else "",
        departure_time=school.departure_time,
        fare=enquiry.fare,
    )

    await send_email(
        subject="Enquiry Option Available",
        recipients=[enquiry.email],
        template_name="enquiry_option.html",
        template_body=email_body.model_dump(),
        mail_username=school.email,
        mail_password=school.password,
    )
    return None


async def send_enquiry_registration_email(enquiry: EnquiryOut) -> None:
    school = enquiry.school
    registration_url = f"{settings.FE_URL}/registration/{enquiry.id}"
    email_body = EnquiryRegistrationBody(
        home_address=enquiry.home_address,
        registration_url=registration_url,
    )
    print(email_body.model_dump())
    await send_email(
        subject="Enquiry Registration",
        recipients=[enquiry.email],
        template_name="enquiry_registration.html",
        template_body=email_body.model_dump(),
        mail_username=school.email,
        mail_password=school.password,
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
