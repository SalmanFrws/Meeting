from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_SSL_VERSION'] = 'TLSv1'
app.config['MAIL_USERNAME'] = 'salmanfurniturewala888@gmail.com'
app.config['MAIL_PASSWORD'] = 'htgj thbh mhow uudc'
app.config['MAIL_DEBUG'] = True

mail = Mail(app)
app.config['MAIL_DEFAULT_SENDER'] = 'salmanfurniturewala888@gmail.com'

booked_slots = {}
meeting_history = []

def reset_slots():
    global booked_slots
    global meeting_history

    older_than_24_hours = datetime.utcnow() - timedelta(hours=24)
    booked_slots = {slot: info for slot, info in booked_slots.items() if info['timestamp'] >= older_than_24_hours}
    meeting_history = [meeting for meeting in meeting_history if meeting['timestamp'] >= older_than_24_hours]

@app.before_request
def before_request():
    reset_slots()

participant_emails_dict = {
    'salman': 'salman.furniturewala@starzventures.in',
    'ashish': 'ashish.sawant@starzventures.in',
    # Add the email addresses of the remaining participants
}

available_slots = ['09:00 AM - 10:00 AM', '10:00 AM - 11:00 AM', '11:00 AM - 12:00 PM', '12:00 PM - 1:00 PM',
                   '1:00 PM - 2:00 PM', '2:00 PM - 3:00 PM', '3:00 PM - 4:00 PM', '4:00 PM - 5:00 PM',
                   '5:00 PM - 6:00 PM', '6:00 PM - 7:00 PM']

@app.route('/', methods=['GET', 'POST'])
def schedule_meeting():
    scheduler_names = ['Raj', 'Vaibhav', 'Sajit', 'Shakti']

    if request.method == 'POST':
        scheduler_name = request.form['scheduler_names']
        selected_slot = request.form['selected_slot']
        selected_participants = request.form.getlist('participant_names')

        subject = 'Meeting Scheduled'
        participant_emails = [participant_emails_dict[name] for name in participant_emails_dict]

        body = f"Hello Folks,\n\nThe meeting has been scheduled by {scheduler_name} for the time slot {selected_slot} for {', '.join(selected_participants)}"
        with app.app_context():
            for participant_email in participant_emails:
                msg = Message(subject, recipients=[participant_email], body=body, sender='salmanfurniturewala888@gmail.com')
                mail.send(msg)

        meeting_time = datetime.utcnow()
        booked_slots[selected_slot] = {'scheduler_name': scheduler_name, 'participant_names': selected_participants, 'timestamp': meeting_time}
        flash('Meeting scheduled successfully!', 'success')

    return render_template(
        'index.html',
        available_slots=available_slots,
        booked_slots=booked_slots,
        meeting_history=meeting_history,
        available_participants=list(participant_emails_dict.keys()),
        scheduler_names=scheduler_names
    )

if __name__ == '__main__':
    app.run(debug=True)


