To enable CORS (Cross-Origin Resource Sharing) in your Django API, you will need to follow these steps:

Install the django-cors-headers package:
To install the django-cors-headers package, run the following command:

Copy code
pip install django-cors-headers
Add corsheaders to your INSTALLED_APPS:
In your Django settings file (usually settings.py), add corsheaders to the INSTALLED_APPS list:

Copy code
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]
Add CorsMiddleware to your MIDDLEWARE:
In your Django settings file (usually settings.py), add CorsMiddleware to the MIDDLEWARE list, placing it before CommonMiddleware:

Copy code
MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]
Set the CORS_ORIGIN_ALLOW_ALL setting to True:
In your Django settings file (usually settings.py), set the CORS_ORIGIN_ALLOW_ALL setting to True to allow all origins:

Copy code
CORS_ORIGIN_ALLOW_ALL = True
Alternatively, you can specify a list of specific origins to allow by setting the CORS_ORIGIN_WHITELIST setting:

Copy code
CORS_ORIGIN_WHITELIST = [
    'https://example.com',
    'https://subdomain.example.com',
]
Test your API:
To test your API with CORS enabled, start the Django development server by running the following command:

Copy code
python manage.py runserver
You should now be able to access your API from a different origin without encountering any CORS errors.

I hope this helps! Let me know if you have any questions.



https://stackoverflow.com/questions/58388869/how-to-generate-one-time-password-when-creating-user-and-send-the-same-to-users




CREATE PROCEDURE multiply_amount()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE amount FLOAT;
    DECLARE pk INT;
    DECLARE cur1 CURSOR FOR SELECT pk, amount FROM old_table;
    DECLARE cur2 CURSOR FOR SELECT pk FROM new_table;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur1;
    OPEN cur2;

    read_loop: LOOP
        FETCH cur1 INTO pk, amount;
        IF done THEN
            LEAVE read_loop;
        END IF;

        SET amount = amount * 3;

        INSERT INTO new_table (pk, amount) VALUES (pk, amount);
    END LOOP;

    CLOSE cur1;
    CLOSE cur2;
END


pip install virtualenv
virtualenv myenv


******
1. Loan Calculaor
