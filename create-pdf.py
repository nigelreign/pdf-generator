from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import qrcode
import os

def create_pdf(
    carbon_date: str,
    payment_date: str,
    beneficiary_name: str,
    transaction_amount: str,
    beneficiary_institution: str,
    beneficiary_reference: str,
    transaction_reference: str,
    beneficiary_account: str,
):
    packet = io.BytesIO()

    img = qrcode.make(transaction_reference)
    img.save(f"qr-codes/{transaction_reference}.png")

    can = canvas.Canvas(packet, pagesize=letter)

    # can.setFillColorRGB(255, 255, 255) #
    can.setFont("Helvetica", 11) 
    can.drawString(450, 930, carbon_date)
    can.drawString(50, 870, "Date Of Payment:")
    can.drawString(450, 870, payment_date)
    can.drawString(50, 820, "Transaction Reference:")
    can.drawString(450, 820, transaction_reference)
    can.drawString(50, 770, "Transaction Amount:")
    can.drawString(450, 770, transaction_amount)
    can.drawString(50, 670, "Beneficiary Name")
    can.drawString(450, 670, beneficiary_name)
    can.drawString(50, 625, "Destination Account No")
    can.drawString(450, 625, beneficiary_account)
    can.drawString(50, 583, "Beneficiary Institution")
    can.drawString(450, 583, beneficiary_institution)
    can.drawString(50, 540, "Beneficiary Reference")
    can.drawString(450, 540, beneficiary_reference)
    can.drawImage(
        f"qr-codes/{transaction_reference}.png",
        250,
        180,
        width=120,
        preserveAspectRatio=True,
        mask="auto",
    )

    can.save()

    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # getting the existing pdf file
    existing_pdf = PdfFileReader(open("assets/original.pdf", "rb"))
    output = PdfFileWriter()

    # add our text to the pdf
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    # genertate a new pdf
    outputStream = open("generated-pdf/" + transaction_reference + ".pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    os.remove(f"qr-codes/{transaction_reference}.png")

    # email_controller.send_pop_as_email(transaction_reference)


carbon_date = "6/9/22 12:55 PM"
payment_date = "3/6/22 9:42 AM"
transaction_reference = "413110430H000274"
beneficiary_name = "Nigel Bongani Zulu"
transaction_amount = "$RTGS110898.58"
beneficiary_institution = "Midlands State University"
beneficiary_reference = "Reign"
beneficiary_account = "3213304781001"

# i = 0
# while i < 100:
create_pdf(
    carbon_date=carbon_date,
    payment_date=payment_date,
    transaction_reference=transaction_reference,
    transaction_amount=transaction_amount,
    beneficiary_name=beneficiary_name,
    beneficiary_institution=beneficiary_institution,
    beneficiary_reference=beneficiary_reference,
    beneficiary_account=beneficiary_account,
)

# i += 1
