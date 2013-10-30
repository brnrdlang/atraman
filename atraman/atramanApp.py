# -*- coding: latin-1 -*- 

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
import os

pwd = os.path.dirname(__file__)

class DateButton(Button):
    def __init__(self, date, callback, **kwargs):
        super(DateButton, self).__init__(**kwargs)
        self.date = date
        self.bind(on_press = self.press)

    def press(self, instance):
        sm.switch_to(DayWidget(date))

#Builder.load_file(os.path.join(pwd, 'calendar.kv'))

class CalendarWidget(BoxLayout):
    
    month = StringProperty('')
    year = StringProperty('')
    calendar_layout = ObjectProperty(None)
    calendar_btns = ListProperty([])
    calendar = ObjectProperty(Calendar())
    date = ObjectProperty(date.today())

    def __init__(self, **kwargs):
        super(CalendarWidget, self).__init__(**kwargs)

        #self.date = date.today()
        self.month = self.date.strftime('%B')
        self.year = str(self.date.year)

    def on_calendar_layout(self, instance, value):
        self.create_calendar()

    def on_date(self, instance, value):
        self.create_calendar()
        self.month = self.date.strftime('%B')
        self.year = str(self.date.year)

    def create_calendar(self):
        self.calendar_layout.clear_widgets()

        self.calendar_btns = []

        for week in self.calendar.monthdatescalendar(self.date.year, self.date.month):
            self.calendar_btns.extend([DateButton(date, text=str(date.day), name=str(date))
                             for date in week])

        for btn in self.calendar_btns:
            self.calendar_layout.add_widget(btn)

    def do_month_before(self):
        if (self.date.month == 1):
            self.date = date(self.date.year -1, 12, 1)
        else:
            self.date = date(self.date.year, self.date.month - 1, 1)

    def do_month_next(self):
        if (self.date.month == 12):
            self.date = date(self.date.year + 1, 1, 1)
        else:
            self.date = date(self.date.year, self.date.month +1, 1)

class DayWidget(BoxLayout):
    datestr = StringProperty('')

    def __init__(self, day, **kwargs): 
        super(DayWidget, self).__init__(**kwargs)
        datestr = day.strftime('%A, den %d. %B %Y')
        entrylist = getEntries(day) #TODO write getEntries
        for entry in entrylist:
            self.add_widget(entry)

def getEntries(day):
    layout = BoxLayout()
    ort = Label(text='Stadion Kieselhumes')
    time = Label(text='18:00')
    training = Label(text='some random text with little bit of adsölfjdaslfjvkjhflj')
    layout.add_widget(ort)
    layout.add_widget(time)
    layout.add_widget(training)

#will be used later when there is more than the calendar
class MenuScreen(Screen):
    pass

class CalendarScreen(Screen):
    pass

sm = ScreenManager()

class AtramanApp(App):

    def build(self):
        sm.switch_to(CalendarScreen(name='calendar'))
        return sm

if __name__ == '__main__':
    AtramanApp().run()
