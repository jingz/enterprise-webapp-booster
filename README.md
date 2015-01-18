Webapp Bootstrap for Enterprise
============================
> This project is consist of following projects
> On top of Flask (Python) 
> ExtJS4 (Desktop-Like UI framework) ( manually install in app/static/core )
> Reportlap (PDF generation tool)

Focus On
========
- fast desktop-like screen prototyping using extjsml (my another project)
- fast to build report pages with existing models
- fast for building admin page for a model
- export pdf file from models (use drawing technique which benefits over many records)
- user role permission (API)

Modules
=======

# User Authentication
> the authentication code is a few lines of code, see in controller/main.py
  which contain login/logout and simple authentication by `require_login`
  there is validation of user permissin in `require_login` also

# User Management -- menu / role / api
> Concept
    a user allow to see menu list by their roles which associate with menu-permission
    user-menu and user-permission are separated by design 
    which make it more flexible to manage api permission

    The relationships between User and Menu
    EltUser *-* EltRole *-* EltAppMenu

    in menu model (EltAppMenu)
    > the menu can have a parent or child
    > a record that has url value it will be determined to be link
    > there is a function that build the result of model in tree structure
    > the value of url field will map to the front-end routing system (JS) which can find in static/component/main_controller.js for example
      and to trigger rendering compoments in i.e. static/components/main/ord_deal.ui.js by using render method in javascript
    > we can get menu list from user by `user.get_menu_list`
    > we can build menu tree by call `EltAppMenu.build_menu_tree`

    The relationship between User and Permission (api)
    EltUser *-* EltApiPermission

    in api permssion (EltApiPermission)
    > it seems to be reflect of almost the application routes, route and http_method is one api permission.
    > every client request will is validated by these permissions see in app authentication

# View System
> we use extjs as views
> all initialize scripts is in templates/layout.html
> and there are two main page -- login page (extjs_login.html) and application page (index.html)
> the full front-end routing system should be implemented when render index.html, see (index.html and static/controllers/main_controller.js) for example
> we will map the routes in EltAppMenu in a controller.js the render some components in i.e. static/components/main/comp.js
> ** the url contain `#` to work fine with browser history

# ExtJs compilation
> the extjs view compile by extjsmlc command, install by `gem install extjsml`
> after install it consume config file `.yml` 
> for example run `extjsmlc example.yml --with-requirejs` in order to work with requirejs

# Seeds
> seed directory contains seed scripts that initialize important data
> before start the project espcially user authentication
