from flask import Flask, render_template, request, flash, redirect, url_for
import os
import requests

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Resend API configuration
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
ADMIN_EMAIL = "codnellsmall@gmail.com"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pack')
def packages():
    return render_template('packages.html')


@app.route('/book')
def book():
    return render_template('book.html')


@app.route('/book', methods=['POST'])
def book_submit():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    service = request.form.get('service')
    date = request.form.get('date')
    package = request.form.get('package')
    message = request.form.get('message')

    booking_details = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Booking Confirmed</title>
</head>
<body style="margin:0;padding:0;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;background:#faf9f6;color:#1a1a1a;line-height:1.6;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#faf9f6;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:24px;border:1px solid rgba(0,0,0,0.08);">
          <tr>
            <td style="padding:30px 40px;text-align:center;border-bottom:1px solid rgba(0,0,0,0.08);">
              <h1 style="font-size:28px;letter-spacing:0.15em;color:#b8860b;margin:0;font-family:'Georgia',serif;">CREATIVE STUDIOS</h1>
            </td>
          </tr>
          <tr>
            <td style="padding:40px;">
              <h2 style="font-size:24px;margin:0 0 20px;color:#1a1a1a;font-family:'Georgia',serif;">Booking Confirmed!</h2>
              <p style="color:#5a5a5a;margin-bottom:30px;">Thank you for choosing Creative Studios. Here is a copy of your booking details:</p>
              
              <table width="100%" cellpadding="0" cellspacing="0" style="background:#faf9f6;border-radius:12px;margin-bottom:30px;">
                <tr>
                  <td style="padding:20px;">
                    <p><strong style="color:#b8860b;">Service:</strong> {service}</p>
                    <p><strong style="color:#b8860b;">Date:</strong> {date}</p>
                    <p><strong style="color:#b8860b;">Package:</strong> {package or 'Not specified'}</p>
                    <p><strong style="color:#b8860b;">Name:</strong> {name}</p>
                    <p><strong style="color:#b8860b;">Phone:</strong> {phone}</p>
                    <p><strong style="color:#b8860b;">Email:</strong> {email}</p>
                  </td>
                </tr>
              </table>
              
              <p><strong style="color:#b8860b;">Additional Details:</strong><br>{message or 'None'}</p>
              
              <p style="color:#5a5a5a;font-size:14px;">We will contact you within 24 hours to confirm your booking.</p>
            </td>
          </tr>
          <tr>
            <td style="padding:20px 40px;text-align:center;border-top:1px solid rgba(0,0,0,0.08);">
              <p style="color:#5a5a5a;font-size:12px;margin:0;">© 2026 Creative Studios</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    admin_email_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>New Booking</title>
</head>
<body style="margin:0;padding:0;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;background:#faf9f6;color:#1a1a1a;line-height:1.6;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#faf9f6;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:24px;border:1px solid rgba(0,0,0,0.08);">
          <tr>
            <td style="padding:30px 40px;text-align:center;border-bottom:1px solid rgba(0,0,0,0.08);">
              <h1 style="font-size:28px;letter-spacing:0.15em;color:#b8860b;margin:0;font-family:'Georgia',serif;">CREATIVE STUDIOS</h1>
            </td>
          </tr>
          <tr>
            <td style="padding:40px;">
              <h2 style="font-size:24px;margin:0 0 20px;color:#1a1a1a;font-family:'Georgia',serif;">New Booking Request!</h2>
              
              <table width="100%" cellpadding="0" cellspacing="0" style="background:#faf9f6;border-radius:12px;margin-bottom:30px;">
                <tr>
                  <td style="padding:20px;">
                    <p><strong style="color:#b8860b;">Name:</strong> {name}</p>
                    <p><strong style="color:#b8860b;">Email:</strong> {email}</p>
                    <p><strong style="color:#b8860b;">Phone:</strong> {phone}</p>
                    <p><strong style="color:#b8860b;">Service:</strong> {service}</p>
                    <p><strong style="color:#b8860b;">Date:</strong> {date}</p>
                    <p><strong style="color:#b8860b;">Package:</strong> {package or 'Not specified'}</p>
                  </td>
                </tr>
              </table>
              
              <p><strong style="color:#b8860b;">Additional Details:</strong><br>{message or 'None'}</p>
            </td>
          </tr>
          <tr>
            <td style="padding:20px 40px;text-align:center;border-top:1px solid rgba(0,0,0,0.08);">
              <p style="color:#5a5a5a;font-size:12px;margin:0;">© 2026 Creative Studios</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    try:
        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        }

        # Send customer confirmation email
        customer_email = {
            "from": "Creative Studios <onboarding@resend.dev>",
            "to": [email],
            "subject": f"Booking Confirmed - {service} - Creative Studios",
            "html": booking_details
        }

        customer_response = requests.post(
            "https://api.resend.com/emails",
            headers=headers,
            json=customer_email,
            timeout=10
        )

        # Send admin notification email
        admin_email = {
            "from": "Creative Studios <onboarding@resend.dev>",
            "to": [ADMIN_EMAIL],
            "subject": f"New Booking: {service} - {name}",
            "html": admin_email_body
        }

        admin_response = requests.post(
            "https://api.resend.com/emails",
            headers=headers,
            json=admin_email,
            timeout=10
        )

        if customer_response.status_code in [200, 201] and admin_response.status_code in [200, 201]:
            flash('Thank you for your booking request! A confirmation email has been sent.', 'success')
        else:
            flash('Booking received, but email delivery failed.', 'warning')

    except Exception as e:
        print("EMAIL ERROR:", e)
        flash('Booking received, but email sending failed.', 'warning')

    return redirect(url_for('book'))


if __name__ == '__main__':
    app.run(debug=True)
