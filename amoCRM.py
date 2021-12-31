import requests
from CONST import *
from mailer import send_email
from twillio_phone import *


def create_contacts():
    for i in range(9):
        data = {"add": [
            {
                "name": f"Jason Nash{i}",
                "responsible_user_id": 7774696,
                "created_by": 7774696,
                "created_at": 1509051600,
                "tags": "important, delivery",
                "company_id": 1115317}
        ]
        }

        response = requests.post(
            'https://vestnik700.amocrm.com/api/v2/contacts',
            headers={"Authorization": "Bearer " + access_token},
            json=data)


def get_contacts_id():
    params = {"responsible_user_id": "7774696"}
    id_arr = []
    response = requests.get(
        'https://vestnik700.amocrm.com/api/v2/contacts',
        headers={"Authorization": "Bearer " + access_token},
        params=params)
    for i in range(10):
        id_arr.append(response.json()['_embedded']['items'][i]['id'])
    return id_arr


def create_leds():
    contacts_id_arr = get_contacts_id()

    for i in contacts_id_arr:
        data = {"add": [
            {
                "name": f"clean house {i}",
                "status_id": "13670637",
                "responsible_user_id": 7774696,
                "sale": "5000",
                "tags": "clean, house",
                "contacts_id": [
                    i
                ],
                "company_id": 1115317,
            }
        ]
        }

        response = requests.post(
            'https://vestnik700.amocrm.com/api/v2/leads',
            headers={"Authorization": "Bearer " + access_token},
            json=data
        )


def get_leads_id():
    params = {"responsible_user_id": "7774696"}
    id_arr = []
    response = requests.get(
        'https://vestnik700.amocrm.com/api/v2/leads',
        headers={"Authorization": "Bearer " + access_token},
        params=params)
    for i in range(10):
        id_arr.append(response.json()['_embedded']['items'][i]['id'])
    return id_arr


def update_leads(stage_id, lead):
    data = {"update": [{"id": lead,
                        "updated_at": 1640980165,
                        "status_id": stage_id
                        }
                       ]
            }

    response = requests.post(
        'https://vestnik700.amocrm.com/api/v2/leads',
        headers={"Authorization": "Bearer " + access_token},
        json=data)


def get_users_id_by_lead(lead_id):
    lead_param = {"id": lead_id}
    response = requests.get(
        'https://vestnik700.amocrm.com/api/v2/leads',
        headers={"Authorization": "Bearer " + access_token},
        params=lead_param)

    contacts_id = []

    for i in response.json()['_embedded']['items'][0]['contacts']['id']:
        contacts_id.append(i)
    return contacts_id


def get_custom_value(data, value):
    for fields in data:
        if fields['code'] == value:
            return fields['values'][0]['value']
    return None


def get_users_info(contact_id):
    lead_param = {"id": contact_id}
    response = requests.get(
        'https://vestnik700.amocrm.com/api/v2/contacts',
        headers={"Authorization": "Bearer " + access_token},
        params=lead_param)
    data = response.json()['_embedded']['items'][0]['custom_fields']
    email = get_custom_value(data, 'EMAIL')
    phone = get_custom_value(data, 'PHONE')
    name = response.json()['_embedded']['items'][0]['name']
    return [name, email, phone]




def create_task(lead_id, user_info):
    data = {
        'add' : [
            {
                "element_id": lead_id,
                "element_type": "2",
                "complete_till_at": "1650897355",
                "task_type": "3",
                "text": f"{user_info[0]}, {user_info[1]}",
                "created_at": "1640897355",
                "responsible_user_id": "7774696",
                "created_by": "7774696"
            }
        ]
    }

    response = requests.post(
        'https://vestnik700.amocrm.com/api/v2/tasks',
        headers={"Authorization": "Bearer " + access_token},
        json=data)


def create_notes(user_id, note_text):
    data = {
   "add": [
      {
         "element_id": user_id,
         "element_type": "1",
         "text": note_text,
         "note_type": 4,
         "created_at": "1650897355",
         "responsible_user_id": "7774696",
         "created_by": "7774696"
      }
   ],
    }

    response = requests.post(
        'https://vestnik700.amocrm.com/api/v2/notes',
        headers={"Authorization": "Bearer " + access_token},
        json=data)


def letter_text(hello_part, main_text, note, user_name):
    return f'{hello_part} {user_name} {main_text} {note}'

def leads_update_with_mail():
    leads_id = get_leads_id()
    for lds_id in leads_id:
        update_leads(Contract_discussion_ID, lds_id)
        lds_users = get_users_id_by_lead(lds_id)
        for users in lds_users:
            users_info = get_users_info(users)
            create_task(lds_id, users_info)
            letter = letter_text(HELLO_PART, MAIN_MESSAGE, NOTE, users_info[0])
            send_email(letter,users_info[1])
            create_notes(users, NOTE)

def leads_with_phone():
    leads_id = get_leads_id()
    for lds_id in leads_id:
        lds_users = get_users_id_by_lead(lds_id)
        for users in lds_users:
            users_info = get_users_info(users)
            make_outbound_call(users_info[2])
            print('call ok')
            create_notes(users, NOTE_CALL_OUT)
            print('note ok')

leads_with_phone()