import requests
from CONST import *
from mailer import send_email
from twillio_phone import *
import datetime


def create_contacts():
    for i in range(9):
        data = {"add": [
            {
                "name": f"Jason Nash{i}",
                "responsible_user_id": RESPONSIBLE_USER,
                "created_by": RESPONSIBLE_USER,
                "created_at": datetime.datetime.now(),
                "tags": "important, delivery",
                "company_id": COMPANY_ID
            }
        ]
        }

        response = requests.post(
            'https://vestnik700.amocrm.com/api/v2/contacts',
            headers={"Authorization": "Bearer " + access_token},
            json=data)


def get_contacts_id():
    params = {"responsible_user_id": f"{RESPONSIBLE_USER}"}
    id_arr = []
    response = requests.get(
        'https://vestnik700.amocrm.com/api/v2/contacts',
        headers={"Authorization": "Bearer " + access_token},
        params=params)
    for i in range(10):
        id_arr.append(response.json()['_embedded']['items'][i]['id'])
    return id_arr


def create_leds(status_id):
    contacts_id_arr = get_contacts_id()

    for i in contacts_id_arr:
        data = {"add": [
            {
                "name": f"clean house {i}",
                "status_id": status_id,
                "responsible_user_id": RESPONSIBLE_USER,
                "sale": "5000",
                "tags": "clean, house",
                "contacts_id": [
                    i
                ],
                "company_id": COMPANY_ID,
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
                        "updated_at": datetime.datetime.now(),
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




def create_task(elem_id, user_info, elem_type, task_type, complete_till):
    data = {
        'add' : [
            {
                "element_id": elem_id,
                "element_type": elem_type,
                "complete_till_at": complete_till,
                "task_type": task_type,
                "text": f"{user_info[0]}, {user_info[1]}",
                "created_at": datetime.datetime.now(),
                "responsible_user_id": RESPONSIBLE_USER,
                "created_by": RESPONSIBLE_USER
            }
        ]
    }

    response = requests.post(
        'https://vestnik700.amocrm.com/api/v2/tasks',
        headers={"Authorization": "Bearer " + access_token},
        json=data)


def create_notes(user_id, note_text, note_type, elem_type):
    data = {
   "add": [
      {
         "element_id": user_id,
         "element_type": elem_type,
         "text": note_text,
         "note_type": note_type,
         "created_at": datetime.datetime.now(),
         "responsible_user_id": RESPONSIBLE_USER,
         "created_by": RESPONSIBLE_USER
      }
   ],
    }

    response = requests.post(
        'https://vestnik700.amocrm.com/api/v2/notes',
        headers={"Authorization": "Bearer " + access_token},
        json=data)


def letter_text(hello_part, main_text, note, user_name):
    return f'{hello_part} {user_name} {main_text} {note}'

# def leads_update_with_mail():
#     leads_id = get_leads_id()
#     for lds_id in leads_id:
#         update_leads(Contract_discussion_ID, lds_id)
#         lds_users = get_users_id_by_lead(lds_id)
#         for users in lds_users:
#             users_info = get_users_info(users)
#             create_task(lds_id, users_info)
#             letter = letter_text(HELLO_PART, MAIN_MESSAGE, NOTE, users_info[0])
#             send_email(letter,users_info[1])
#             create_notes(users, NOTE)
#
# def leads_with_phone():
#     leads_id = get_leads_id()
#     for lds_id in leads_id:
#         lds_users = get_users_id_by_lead(lds_id)
#         for users in lds_users:
#             users_info = get_users_info(users)
#             make_outbound_call(users_info[2])
#             print('call ok')
#             create_notes(users, NOTE_CALL_OUT)
#             print('note ok')
