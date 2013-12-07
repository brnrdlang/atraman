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
import os
import sqlite3

pwd = os.path.dirname(__file__)

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

        layout = BoxLayout(orientation='vertical')

        layout.add_widget(Label(text=datestr))
        
        for entry in entrylist:
            layout.add_widget(entry)

            def click_it(instance):
                sm.switch_to(CalendarScreen(name='calendar'))

        layout.add_widget(Button(text='zurück', on_press=click_it))

        self.add_widget(layout)

def getEntries(day):
    """Gets data for given day, returns list of Widgets"""

    layout = BoxLayout(orientation='vertical')
    place = Label(text='Stadion Kieselhumes')
    time = Label(text='18:00')
    training = Label(text='some random text with little bit of adsölfjdaslfjvkjhflj')
    layout.add_widget(place)
    layout.add_widget(time)
    layout.add_widget(training)
    return [layout]

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
