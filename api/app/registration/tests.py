import json
from datetime import datetime, timedelta
from app import db, LOGGER
from app.utils.testing import ApiTestCase
from app.users.models import AppUser, UserCategory, Country
from app.registration.models import Offer
from app.registration.models import RegistrationSection
from app.registration.models import RegistrationQuestion
from app.registration.models import RegistrationForm
from app.events.models import Event


REGISTRATION_FORM = {
    'event_id': 1,
}

REGISTRATION_SECTION = {
        'registration_form_id': 1,
        'name': "section 2",
        'description': "this is the second section",
        'order': 1,
        'show_for_accommodation_award': True,
        'show_for_travel_award': True,
        'show_for_payment_required': True
}

REGISTRATION_QUESTION = {
        'registration_form_id': 1,
        'section_id': 1,
        'type': "open-ended",
        'description': "just a question",
        'headline': "question headline",
        'placeholder': "answer the this question",
        'validation_regex': "/[a-d]",
        'validation_text': "regex are cool",
        'order': 1,
        'options': "{'a': 'both a and b', 'b': 'none of the above'}",
        'is_required': True
}


class RegistrationTest(ApiTestCase):

    def seed_static_data(self):
        db.session.add(UserCategory('Postdoc'))
        db.session.add(Country('South Africa'))
        db.session.commit()

        test_user = AppUser('something@email.com', 'Some', 'Thing', 'Mr', 1, 1,
                            'Male', 'University', 'Computer Science', 'None', 1,
                            datetime(1984, 12, 12),
                            'Zulu',
                            '123456')
        test_user.verified_email = True
        db.session.add(test_user)
        db.session.commit()

        db.session.commit()

        event = Event(
            name="Tech Talk",
            description="tech talking",
            start_date=datetime(2019, 12, 12, 10, 10, 10),
            end_date=datetime(2020, 12, 12, 10, 10, 10),

        )
        db.session.add(event)
        db.session.commit()

        offer = Offer(
             user_id=test_user.id,
             event_id=event.id,
             offer_date=datetime.now(),
             expiry_date=datetime.now() + timedelta(days=15),
             payment_required='yes',
             travel_award='no award',
             updated_at=datetime.now())
        db.session.add(offer)
        db.session.commit()

        form = RegistrationForm(
            event_id=event.id
        )
        db.session.add(form)
        db.session.commit()

        section = RegistrationSection(
            registration_form_id=form.id,
            name="Section 1",
            description="the section description",
            order=1,
            show_for_travel_award=True,
            show_for_accommodation_award=False,
            show_for_payment_required=False,
        )
        db.session.add(section)
        db.session.commit()

        question = RegistrationQuestion(
            section_id=section.id,
            registration_form_id=form.id,
            description="Question 1",
            type="short-text",
            is_required=True,
            order=1,
            placeholder="the placeholder",
            headline="the headline",
            validation_regex="[]/",
            validation_text=" text"
        )
        db.session.add(question)
        db.session.commit()

        db.session.flush()

    def test_create_registration_form(self):
        self.seed_static_data()
        response = self.app.post(
            '/api/v1/registration-form', data=REGISTRATION_FORM)
        data = json.loads(response.data)
        LOGGER.debug(
            "Reg-form: {}".format(data))
        assert response.status_code == 201
        assert data['registration_form_id'] == 2

    def test_get_form(self):
        self.seed_static_data()
        event_id = 1
        offer_id = 1
        url = "/api/v1/registration-form?offer_id=%d&event_id=%d" % (offer_id, event_id)
        LOGGER.debug(url)
        response = self.app.get(url)
        LOGGER.debug(
            "form: {}".format(json.loads(response.data)))

        form = json.loads(response.data)
        assert form['registration_sections'][0]['registration_questions'][0]['type'] == 'short-text'
        assert form['registration_sections'][0]['name'] == 'Section 1'
        assert response.status_code == 201


