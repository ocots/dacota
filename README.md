# Ternary univolatility diagram generator

## General description

This web application allows users to draw a Ternary univolatility diagram of a ternary mixtures in termodynamics. The user selects three compounds then click on run to view the chart that will be displayed by default in a rectangle triangle, user can then switch between equilateral/rectangle triangle. Users can add new compounds and relations that are not predefined in the database and can also edit the values of the added elements. A session is created for each client and elements added by the client will remain available in the website as long as the session is not expired yet. The expiry duration is set in settings.py. To generate a diragram, the compounds of the mixture selected should be distinct and defined, meaning that binary relations between compound 1 and compound 2, compound 2 and compound 3 and compound 1 and compound 3 sould be defined.

This web application is developped with Python using the Django framework.

## Set up your project directory :

To contribute in this project follow these steps to set up your project :

- Clone this github repository.
- Install the prerequisities and requirements :

  ### Prerequisites

  - Python 3.10
  - Docker installed in your system.

  ### Installation

    <!-- https://www.architecture-performance.fr/ap_blog/some-pre-commit-git-hooks-for-python/ -->
    <!-- https://marcobelo.medium.com/setting-up-python-black-on-visual-studio-code-5318eba4cd00 -->

  ```
  python3 -m pip install -r requirements.txt
  python3 -m pip install -r requirements-dev.txt
  python3 -m pre-commit install
  ```

- Load the database :

  ```
  python3 manage.py migrate
  python3 managy.py load_component_data
  ```

- Create your admin page by running this command and choosing your username and password:

  ```
  python3 manage.py createsuperuser
  ```

- To start the server on your local host :

  ```
  python managy.py runserver
  ```

- To open the web application, paste the server link : http://127.0.0.1:8000/ in your browser

## Database of the web application

The database register compounds and relations that are available to the users. The predefined elements that are available to all users do not depend on sessions. An element that was added by one or multiple users will have the session keys in its chosen sessions list and an element with an empty chosen sessions means that the element is predefined.

To edit these predefined elements or add new elements. you have two options :

- option 1 with the admin page :
  Open the admin page with this link : http://127.0.0.1:8000/admin then connect with credentials you used while creating the admin. Once connected you can see all tables of the database. As an administrator, you can view, add, edit or delete compounds and binary relations. To do so, click on a table, click on add and enter values then save. Or click on the id of the element to edit, edit its values then save.

- option 2 with csv files :
  you can edit directly the csv files `binary_relations_data.csv` and `component_data.csv` then run the command `python3 manage load_component_data`

## Sessions

When a new client opens the website, a new session will be created for them. The expiry duration is set in the `SESSION_EXPIRY_DURATION` variable in `settings.py`. This variable can be changed but when the session is expired the user will no longer have access to its added elements and will be considered as a new client. When the session is expired, all added elements will be removed from the database once a new client opens the web application. If you want to manually remove expired data you can run the following command `python3 manage.py clear_expired_data`

## Tests

For the majority of the functionnalities implemented, unit tests were added inside the directory `test`. For additional tests, you can create a new file in this folder and add your tests. To run these tests, you can use `python3 manage.py test` an OK should displayed at the end to indicate that all tests were passed.
