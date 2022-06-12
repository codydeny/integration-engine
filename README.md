# Altan Internship Task Readme
* [Design Diagrams](design_docs.md)
* [integration docs](integration-docs.md)
* [design explaination](design-explaination.md)

## Langauge Used
* Python
## Technologies Used
* Django 
* Django Rest Framework
## setup
### requirements
```Python 3.10```
### install packages
``` pip install -r requirements.txt```
### run server
```python manage.py runserver```

### Folder Structure
* `atlan_task` - Django Related Folder
* `collect` - Django App to simulate collect(Form, Response, Questions, Answers)
* `core` - Integration Processor/Engine
* `integrations` - Integrations built in a plug and play fashion.
*  `utils` - utility file to create google 0auth token details.

## Tutorial
After running the server, go to `http://127.0.0.1:8000/admin` and login with username `admin` & password `admin@123`.

## quickstart to test google-sheet integration
### get your auth token
As to generate 0Auth tokens required to run this, I have created a small script you can use to generate your google 0auth tokens, it resides in `utility/authorize.py`. 
to run the file:
```cd utility```
```python authorize.py```
after successful authentication it creates a `token.json`, copy its content.
### link integration to a form
visit `http://127.0.0.1:8000/collect/integration/`
![test](https://user-images.githubusercontent.com/22274195/173249172-7d69988f-6c45-4502-8d27-ec2d81291b4c.PNG)
paste the contents of `token.json` in the `input` field as follows: 
```
{
    "google_auth" : <PASTE-IT-HERE>
}
```
after request completes, integration will be linked to the form

### integration triggers on form submission:
visit `http://127.0.0.1:8000/collect/form/submit/`
![test2](https://user-images.githubusercontent.com/22274195/173249429-b9752b20-c156-48b6-b17f-0d5c4a9a0766.PNG)
use demo response object as input with `id=2` by pasting the following in the content
```
{
"response" : 2
}
```

a successful response should show all the integration details.


## Additional APIs 
### create a form
go to `collect->form->add` or simply visit `http://127.0.0.1:8000/admin/collect/form/add/` in the browser.

### create a response
go to `collect->response->add` or simply visit `http://127.0.0.1:8000/admin/collect/response/add/` in the browser.

