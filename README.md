# day-64-movie-project

## Traceback (most recent call last):
  File "C:\Users\eliza\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask\app.py", line 2548, in __call__
    return self.wsgi_app(environ, start_response)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\eliza\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask\app.py", line 2528, in wsgi_app
    response = self.handle_exception(e)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\eliza\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask\app.py", line 2525, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\eliza\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask\app.py", line 1822, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\eliza\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask\app.py", line 1820, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\eliza\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask\app.py", line 1796, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\eliza\PycharmProjects\pythonProject\day-64\Starting+Files+-+movie-project-start\main.py", line 119, in adding_movie
    year=movie_object.year,
         ^^^^^^^^^^^^^^^^^^
AttributeError: 'str' object has no attribute 'year'
