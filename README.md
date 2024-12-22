### Description of files in framework

##### 1 - What is structure?
In our framework, we use Page Object pattern, which means all page elements and actions are stored separately from test
steps and a class is created for any page. Main folders you will have are:
  * Framework - common framework for all journeys. Ideally, there should be no changes (if you need anything in addition,
please contact n.pleshkun or d.ananyev and we will solve this out)
  * browser - BrowserFactory class returns a browser based on configurations in config.py. Browser class provides actions
 like closing, quitting, navigating between pages. Those browsers are initialized in conftest.py file (stored in tests
 folder for each journey)
  * configuration - folder with basic configurations (you can just copy it into your journey configurations)
  * constants - folder with global constants like browser names, file extensions etc
  * elements - folder with all elements like Buttons, labels etc. It contains BaseElement class in base subfolder, from
which all elements are inherited.
  * forms - a folder with base form (form is a group of elements which is used in several places in the app). So whenever
 you'd like to create a form inherit it from BaseForm
  * pages - a folder with base page, from which all pages in your journey should inherit. It has some basic methods
inside like waiting for page to load, refreshing etc
  * scripts - a folder with some basic js scripts for actions like scrolling, which cannot be performed using selenium.
  * utils - a folder with classes-helpers. Any common actions like reading filed, taking screenshots, working with
database should be stored there
  * waits - classes-helpers which provide common functionality of waiting for conditions (ready state complete, condition
is true)

##### 2 - Folder with journey contains the following:
  * configuration - contains browser, environment, locale etc
  * pages - all pages related to your tests. 1 file - 1 class, each class describes 1 page (contains page elements and
actions to perform)
  * tests - a folder with tests, contains subfolders for different features (e.g. Search for Home, apply for Loan etc)