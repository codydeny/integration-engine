from collect.models import Response
from core.Integration import Integration
from core.execution import Execution
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError, Error
from google.oauth2.credentials import Credentials


def to_row(response: Response):
    rows = []
    for answer in response.answer_set.all().order_by("question__order"):
        rows.append(answer.answer)

    return [rows]


def get_header(form):
    rows = []
    for question in form.question_set.all():
        rows.append(question.name)

    return [rows]


class GoogleDocsIntegration(Integration):
    service = None
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def execute(self, processed_data) -> Execution:
        try:
            response: Response = processed_data["response"]
            creds = Credentials.from_authorized_user_info(self.integration_instance.input["google_auth"], self.SCOPES)
            service = build('sheets', 'v4', credentials=creds)
            # The ID of the spreadsheet to update.
            spreadsheet_id = self.integration_instance.input["init_data"]["data"]["spreadsheetId"]

            body = {
                "majorDimension": "ROWS",
                "values": to_row(response)
            }

            request = service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                body=body,
                range="Sheet1!A:Z",
                insertDataOption="INSERT_ROWS",
                valueInputOption="USER_ENTERED"
            )
            spreadsheet = request.execute()
            return Execution(
                success=True,
                message="Success",
                data=spreadsheet
            )

        except Error as e:
            return Execution(
                success=False,
                message=str(e)
            )

        except Exception as e:
            return Execution(
                success=False,
                message=str(e)
            )

    def initialize(self, init_data, form):
        try:

            creds = Credentials.from_authorized_user_info(init_data["google_auth"], self.SCOPES)
            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            spreadsheet = service.spreadsheets().create(body={}).execute()

            header_body = {
                "majorDimension": "ROWS",
                "values": get_header(form)
            }
            request = service.spreadsheets().values().append(
                spreadsheetId=spreadsheet["spreadsheetId"],
                body=header_body,
                range="Sheet1!A:Z",
                insertDataOption="INSERT_ROWS",
                valueInputOption="USER_ENTERED"
            )
            spreadsheet = request.execute()

            return Execution(
                success=True,
                message="Success",
                data=spreadsheet
            )

        except HttpError as err:
            return Execution(
                success=False,
                message=err
            )
