# -*- coding: latin-1 -*- 
import config

from datetime import datetime, date
from calendar import Calendar
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
import os
import sqlite3

def init_db():
    """Initializes database and returns Connection Object."""
    conn = sqlite3.connect(pwd + "/" + config.DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(training)")
    if not cur.fetchall():
        print "No table found: Create new sqlite table in database"
        cur.execute("CREATE TABLE training (place text, description text, date datetime)")

    return conn

pwd = os.path.dirname(__file__)
db = init_db()

class DateButton(Button):
    """Button to represent a date in the CalendarWidget.

    The button gets the date he represents and has a method press which changes the screen
    to the DayScreen of the Buttons date"""

    def __init__(self, date, **kwargs):
        """Constructor of DateButton.

        Gets a date for the button to represent. Binds press method to on_press event"""
        
        super(DateButton, self).__init__(**kwargs)
        self.date = date
        self.bind(on_press = self.press)

    def press(self, instance):
        """Handles a press event for the DateButton.

        Changes Screen to DayScreen of the through this button representated date"""

        sm.switch_to(DayScreen(self.date))

#Builder.load_file(os.path.join(pwd, 'calendar.kv'))

class CalendarWidget(BoxLayout):
    """Widget to represent a calendar.

    Look also in atraman.kv for additional information"""
    
    month = StringProperty('')
    year = StringProperty('')
    calendar_layout = ObjectProperty(GridLayout(cols=7,id="cal"))
    calendar_btns = ListProperty([])
    calendar = ObjectProperty(Calendar())
    date = ObjectProperty(date.today())

    def __init__(self, **kwargs):
        """Constructor of CalendarWidget.

        Sets the shown calendar to the actual month and year"""

        super(CalendarWidget, self).__init__(**kwargs)
        self.month = self.date.strftime('%B')
        self.year = str(self.date.year)

    def on_calendar_layout(self, instance, value):
        """Called when calendar_layout itself is changed.

        It's only needed because at start of the application there wouldn't be any
        date buttons without it and I did not find any more beautiful way to work around it."""
        self.create_calendar()

    def on_date(self, instance, value):
        """Updates the calendar to the new date.

        Gets called when self.date is assigned a new value. Creates buttons and changes
        strings for year and month"""

        self.create_calendar()
        self.month = self.date.strftime('%B')
        self.year = str(self.date.year)

    def create_calendar(self):
        """Creates buttons for the actual month of year of calendar.date().
        
        Used to create and update the DayButton. Gets called automatically at date change
        or layout change."""

        #delete old buttons
        self.calendar_layout.clear_widgets()

        #reset button list
        self.calendar_btns = []

        #Creates all buttons for given month
        for week in self.calendar.monthdatescalendar(self.date.year, self.date.month):
            self.calendar_btns.extend([DateButton(date, text=str(date.day), name=str(date))
                             for date in week])

        #add buttons to Layout
        for btn in self.calendar_btns:
            self.calendar_layout.add_widget(btn)

    def do_month_before(self):
        """Changes to previous month"""

        if (self.date.month == 1):
            self.date = date(self.date.year -1, 12, 1)
        else:
            self.date = date(self.date.year, self.date.month - 1, 1)

    def do_month_next(self):
        """Changes to next month"""

        if (self.date.month == 12):
            self.date = date(self.date.year + 1, 1, 1)
        else:
            self.date = date(self.date.year, self.date.month +1, 1)

class DayScreen(Screen):
    """Shows entry for specified day on Screen"""

    #string to representate given day
    datestr = StringProperty('')

    def __init__(self, day, **kwargs):
        """Constructor of DayScreen"""
 
        super(DayScreen, self).__init__(**kwargs)
        datestr = day.strftime('%A, den %d. %B %Y')
        entrylist = getEntries(day) #TODO write getEntries
        
        scroll = ScrollView()

        layout = BoxLayout(orientation='vertical')

        layout.add_widget(Label(text=datestr, size_hint_y=None, height=50))
        
        for entry in entrylist:
            layout.add_widget(entry)

        layout.add_widget(Button(text='Neuer Eintrag', on_press=lambda inst: sm.switch_to(FormScreen(day)), size_hint=(None,None), size=(200,40), pos_hint={'center_x': 0.5}))

        layout.add_widget(Button(text='Zurück', on_press=lambda inst: sm.switch_to(CalendarScreen(name='calendar')), size_hint=(None,None), size=(200,40), pos_hint={'center_x': 0.5}))
        
        scroll.add_widget(layout)
        self.add_widget(scroll)

class FormScreen(Screen):
    
    def __init__(self, day, **kwargs):
        """Constructor of FormScreen"""

        super(FormScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        form = GridLayout(cols=2, size_hint_x=.7)
        form.add_widget(Label(text='Ort:', size_hint=(.3, None), height=40))
        placeInput = TextInput(multiline=False, size_hint_y=None, height=40)
        form.add_widget(placeInput)
        form.add_widget(Label(text='Datum:', size_hint=(.3,None), height=40))
        dateInput = TextInput(multiline=False, text=day.strftime('%d.%m.%Y'), size_hint_y=None, height=40)        
        form.add_widget(dateInput)
        form.add_widget(Label(text='Uhrzeit:', size_hint=(.3,None), height=40))
        timeInput = TextInput(multiline=False, size_hint_y=None, height=40)
        form.add_widget(timeInput)
        
        layout.add_widget(form)
        desc = TextInput()
        layout.add_widget(desc)
        
        def submit(instance):
            if not (placeInput.text and dateInput.text and timeInput.text and desc.text):
                print 'Some input was empty :('
                return
            place = unicode(placeInput.text, encoding='utf-8')
            date = datetime.strptime(dateInput.text + ' ' + timeInput.text, '%d.%m.%Y %H:%M')
            description = unicode(desc.text, encoding='utf-8')
            setEntries(place, date, description)
            print 'Successfully added entry :)'
            sm.switch_to(DayScreen(day))

        layout.add_widget(Button(text='Eintragen', on_press=submit, size_hint=(None,None),
            size=(200,40), pos_hint={'center_x': 0.5}))
        
        layout.add_widget(Button(text='Zurück', 
            on_press=lambda inst: sm.switch_to(DayScreen(day)), 
            size_hint=(None,None), size=(200,40), pos_hint={'center_x': 0.5}))

        self.add_widget(layout)

def setEntries(place, date, training):
    """Creates an entry into the database."""
    cur = db.cursor()    
    cur.execute('INSERT INTO training VALUES(?,?,?)', (place, training, date))
    db.commit()

def getEntries(day):
    """Gets data for given day, returns list of Widgets"""

    cur = db.cursor()
    return [createLogEntry(entry[0], datetime.strptime(entry[2], '%Y-%m-%d %H:%M:%S'), entry[1]) for entry in cur.execute('SELECT * FROM training WHERE date(date) = date(?)', (day,) )]

def createLogEntry(place, date, description):
    
    layout = BoxLayout(orientation='vertical')
    placeLabel = Label(text=place, size_hint_y=None, height=40)
    timeLabel = Label(text=date.time().strftime("%H:%M"), size_hint_y=None, height=40)
    trainingLabel = Label(text=description)
    layout.add_widget(placeLabel)
    layout.add_widget(timeLabel)
    layout.add_widget(trainingLabel)
        
    return layout

#will be used later when there is more than the calendar
class MenuScreen(Screen):
    """Shows main-menu for application."""
    pass

class CalendarScreen(Screen):
    """Dummy object for CalendarScreen. See atraman.kv for implementation"""
    pass

sm = ScreenManager()

class AtramanApp(App):
    """main app class for the atraman App"""

    def build(self):
        sm.switch_to(CalendarScreen(name='calendar'))
        return sm

if __name__ == '__main__':
    AtramanApp().run()
